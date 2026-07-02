"""
Multi-task CNN training for Shoulder Milling: ONE shared backbone with three
parallel classifier heads (speed, doc, feed), trained jointly, as an
alternative to the speed->doc->feed cascade in cnn_train_param.py.

Motivation (see experiments_writeup.md and the multitask proposal that
prompted this script): the cascade's ConditionedModel conditions each stage
on the PREDICTED label of its parent, concatenated as a small one-hot vector
just before the final linear layer. After fixing a predict_conditioning.py
bug that silently broke that predicted-label pathway, feed's real ceiling on
the cascade turned out to be ~62.5% run accuracy / ~41-46% window accuracy --
no better than not conditioning at all. Multi-task learning removes that
fragile predicted-label pathway entirely: speed/doc information reaches the
feed head implicitly through a SHARED backbone representation, supervised by
speed's and doc's own ground-truth labels (not predictions) as auxiliary
losses. Speed and doc are near-100%-learnable targets (experiments_writeup.md
S2), so their clean gradients should also anchor/stabilize the shared
representation relative to feed's single-task training, which showed large
epoch-to-epoch test-loss spikes in history.json logs.

All three heads are trained and evaluated on the SAME held-out split (feed's
own split, or --split_id exp11/exp12), so speed/doc accuracy reported here is
diagnostic (are the auxiliary tasks being learned at all?), not a comparison
against their own dedicated single-task splits.

No SMOTE (same rationale as conditioned mode in cnn_train_param.py: synthetic
windows have no real speed/doc ground truth to supervise the auxiliary
heads with).

Usage:
    python cnn_train_multitask.py --img_dir scalograms_32x3_feedopt \
        --arch efficientnet_b0 --lr 1e-4 --seed 43 --split_id exp11
"""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader, Dataset
from torchvision import models

from cnn_train_param import (
    COND_FROM_SIDE_FEED, EXP_SPLITS, TARGETS, build_transforms, label_for,
    seed_everything,
)

HEADS = ["speed", "doc", "feed"]   # fixed head order used throughout this script


# ── data loading ───────────────────────────────────────────────────────────────
def load_multitask_split(img_dir: Path, split_id: str = ""):
    """Single shared split for all three heads: feed's own test_runs, or the
    exp11/exp12 unified split when --split_id is set. Excludes those runs
    entirely from training, so evaluating speed/doc heads on them is a valid
    (if non-standard) held-out read, not leakage."""
    df = pd.read_csv(img_dir / "labels.csv")
    df["run_id"] = df.apply(lambda r: COND_FROM_SIDE_FEED[(int(r["side"]), r["feed"])], axis=1)
    for h in HEADS:
        df[f"{h}_label"] = df.apply(lambda r: label_for(h, r["side"], r["feed"]), axis=1)

    if split_id in EXP_SPLITS:
        test_runs = EXP_SPLITS[split_id]["test_runs"]
    else:
        test_runs = TARGETS["feed"]["test_runs"]
    all_runs   = df["run_id"].unique().tolist()
    train_runs = [r for r in all_runs if r not in test_runs]

    train_df = df[df["run_id"].isin(train_runs)].reset_index(drop=True)
    test_df  = df[df["run_id"].isin(test_runs)].reset_index(drop=True)

    def to_dict(sub):
        return {
            "paths":   [img_dir / row.filename for _, row in sub.iterrows()],
            "labels":  {h: sub[f"{h}_label"].tolist() for h in HEADS},
            "run_ids": sub["run_id"].tolist(),
        }

    return to_dict(train_df), to_dict(test_df)


class MultiTaskScalogramDataset(Dataset):
    def __init__(self, paths, labels: dict, transform=None):
        self.paths, self.labels, self.transform = paths, labels, transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels["speed"][idx], self.labels["doc"][idx], self.labels["feed"][idx]


# ── model ──────────────────────────────────────────────────────────────────────
class MultiTaskModel(nn.Module):
    """One backbone, three heads (speed:2, doc:4, feed:3 classes)."""
    def __init__(self, arch: str, dropout: float = 0.15):
        super().__init__()
        if arch == "resnet18":
            base = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
            feat_dim = base.fc.in_features
            base.fc = nn.Identity()
        elif arch == "resnet50":
            base = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
            feat_dim = base.fc.in_features
            base.fc = nn.Identity()
        elif arch == "efficientnet_b0":
            base = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
            feat_dim = base.classifier[1].in_features
            base.classifier = nn.Identity()
        elif arch == "convnext_tiny":
            base = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
            feat_dim = base.classifier[2].in_features
            base.classifier = nn.Sequential(base.classifier[0], base.classifier[1])  # LN2d + Flatten
        else:
            raise ValueError(f"Unknown arch: {arch}")

        self.backbone = base

        def make_head(num_classes):
            return nn.Sequential(nn.Dropout(dropout), nn.Linear(feat_dim, num_classes)) if dropout > 0 \
                else nn.Linear(feat_dim, num_classes)

        self.head_speed = make_head(TARGETS["speed"]["num_classes"])
        self.head_doc   = make_head(TARGETS["doc"]["num_classes"])
        self.head_feed  = make_head(TARGETS["feed"]["num_classes"])

    def forward(self, img):
        feats = self.backbone(img)
        return self.head_speed(feats), self.head_doc(feats), self.head_feed(feats)


# ── class weights ─────────────────────────────────────────────────────────────
def class_weights(labels: list, num_classes: int, device) -> torch.Tensor:
    counts = np.bincount(labels, minlength=num_classes).astype(float)
    counts[counts == 0] = 1.0
    w = torch.tensor(1.0 / counts, dtype=torch.float32, device=device)
    return w / w.sum()


# ── train / eval loops ────────────────────────────────────────────────────────
def train_epoch(model, loader, criteria, w_speed, w_doc, optimizer, device):
    model.train()
    totals = {"loss": 0.0, "n": 0, "correct_speed": 0, "correct_doc": 0, "correct_feed": 0}
    for imgs, speed_lbl, doc_lbl, feed_lbl in loader:
        imgs = imgs.to(device)
        speed_lbl, doc_lbl, feed_lbl = speed_lbl.to(device), doc_lbl.to(device), feed_lbl.to(device)

        optimizer.zero_grad()
        speed_out, doc_out, feed_out = model(imgs)
        loss_feed  = criteria["feed"](feed_out, feed_lbl)
        loss_speed = criteria["speed"](speed_out, speed_lbl)
        loss_doc   = criteria["doc"](doc_out, doc_lbl)
        loss = loss_feed + w_speed * loss_speed + w_doc * loss_doc
        loss.backward()
        optimizer.step()

        bs = len(feed_lbl)
        totals["loss"]          += loss.item() * bs
        totals["n"]             += bs
        totals["correct_speed"] += (speed_out.argmax(1) == speed_lbl).sum().item()
        totals["correct_doc"]   += (doc_out.argmax(1) == doc_lbl).sum().item()
        totals["correct_feed"]  += (feed_out.argmax(1) == feed_lbl).sum().item()

    n = totals["n"]
    return {
        "loss": totals["loss"] / n,
        "acc_speed": totals["correct_speed"] / n,
        "acc_doc": totals["correct_doc"] / n,
        "acc_feed": totals["correct_feed"] / n,
    }


@torch.no_grad()
def eval_epoch(model, loader, criteria, w_speed, w_doc, device):
    model.eval()
    totals = {"loss": 0.0, "n": 0, "correct_speed": 0, "correct_doc": 0, "correct_feed": 0}
    feed_preds, feed_labels = [], []
    for imgs, speed_lbl, doc_lbl, feed_lbl in loader:
        imgs = imgs.to(device)
        speed_lbl, doc_lbl, feed_lbl = speed_lbl.to(device), doc_lbl.to(device), feed_lbl.to(device)

        speed_out, doc_out, feed_out = model(imgs)
        loss_feed  = criteria["feed"](feed_out, feed_lbl)
        loss_speed = criteria["speed"](speed_out, speed_lbl)
        loss_doc   = criteria["doc"](doc_out, doc_lbl)
        loss = loss_feed + w_speed * loss_speed + w_doc * loss_doc

        bs = len(feed_lbl)
        totals["loss"]          += loss.item() * bs
        totals["n"]             += bs
        totals["correct_speed"] += (speed_out.argmax(1) == speed_lbl).sum().item()
        totals["correct_doc"]   += (doc_out.argmax(1) == doc_lbl).sum().item()
        totals["correct_feed"]  += (feed_out.argmax(1) == feed_lbl).sum().item()
        feed_preds.extend(feed_out.argmax(1).cpu().tolist())
        feed_labels.extend(feed_lbl.cpu().tolist())

    n = totals["n"]
    return {
        "loss": totals["loss"] / n,
        "acc_speed": totals["correct_speed"] / n,
        "acc_doc": totals["correct_doc"] / n,
        "acc_feed": totals["correct_feed"] / n,
        "f1_feed": f1_score(feed_labels, feed_preds, average="macro", zero_division=0),
    }


@torch.no_grad()
def feed_run_level_accuracy(model, paths, feed_labels, run_ids, val_tf, device):
    """Hard-vote (majority over per-window argmax) and soft-vote (argmax of
    mean softmax over windows) run-level feed accuracy from the same model."""
    model.eval()
    dummy_labels = {"speed": [0] * len(paths), "doc": [0] * len(paths), "feed": feed_labels}
    ds = MultiTaskScalogramDataset(paths, dummy_labels, val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)

    all_probs = []
    for imgs, _s, _d, _f in dl:
        imgs = imgs.to(device)
        _, _, feed_out = model(imgs)
        all_probs.extend(torch.softmax(feed_out, dim=1).cpu().tolist())

    run_probs, run_hard_votes, run_true = {}, {}, {}
    for probs, true, run in zip(all_probs, feed_labels, run_ids):
        run_probs.setdefault(run, []).append(probs)
        run_hard_votes.setdefault(run, []).append(int(np.argmax(probs)))
        run_true[run] = true

    hard_correct, soft_correct = 0, 0
    for run in run_true:
        hard_pred = max(set(run_hard_votes[run]), key=run_hard_votes[run].count)
        soft_pred = int(np.argmax(np.mean(run_probs[run], axis=0)))
        hard_correct += int(hard_pred == run_true[run])
        soft_correct += int(soft_pred == run_true[run])

    n_runs = len(run_true)
    return hard_correct / n_runs, soft_correct / n_runs, n_runs


# ── main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--img_dir", required=True,
                        help="scalogram dir relative to this script, e.g. scalograms_32x3_feedopt")
    parser.add_argument("--arch", default="efficientnet_b0",
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"])
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--dropout", type=float, default=0.15)
    parser.add_argument("--label_smooth", type=float, default=0.05)
    parser.add_argument("--noise_std", type=float, default=0.02)
    parser.add_argument("--w_speed", type=float, default=0.3,
                        help="Auxiliary loss weight for the speed head")
    parser.add_argument("--w_doc", type=float, default=0.3,
                        help="Auxiliary loss weight for the doc head")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--split_id", default="", choices=["", "exp11", "exp12"],
                        help="Experimental unified split (see experimental_splits.md). "
                             "Empty string uses feed's own split from README.md.")
    args = parser.parse_args()

    seed_everything(args.seed)

    img_dir   = Path(__file__).parent / args.img_dir
    scalo_tag = img_dir.name.replace("scalograms_", "")
    out_dir   = Path(__file__).parent / f"models_multitask_feed_{scalo_tag}"
    out_dir.mkdir(exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device    : {device}")
    print(f"Scalogram : {scalo_tag}   Split: {args.split_id or 'feed base'}")
    print(f"Arch      : {args.arch}   LR: {args.lr}   Seed: {args.seed}   "
          f"w_speed={args.w_speed}  w_doc={args.w_doc}")

    train, test = load_multitask_split(img_dir, args.split_id)
    print(f"Train windows : {len(train['paths'])}  |  Test windows : {len(test['paths'])}  "
          f"({len(set(test['run_ids']))} test runs)")

    train_tf, val_tf = build_transforms(args.noise_std)
    train_ds = MultiTaskScalogramDataset(train["paths"], train["labels"], train_tf)
    test_ds  = MultiTaskScalogramDataset(test["paths"], test["labels"], val_tf)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=0)
    test_dl  = DataLoader(test_ds, batch_size=args.batch, shuffle=False, num_workers=0)

    criteria = {}
    for h in HEADS:
        w = class_weights(train["labels"][h], TARGETS[h]["num_classes"], device)
        print(f"Class weights {h} {TARGETS[h]['class_names']}: {w.cpu().numpy().round(3)}")
        criteria[h] = nn.CrossEntropyLoss(weight=w, label_smoothing=args.label_smooth)

    model     = MultiTaskModel(args.arch, dropout=args.dropout).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    tag = f"{args.arch}_lr{args.lr:g}_seed{args.seed}_{args.split_id or 'base'}"
    best_feed_acc, best_epoch, history = 0.0, 0, []

    print(f"\n{'Ep':>4}  {'TrLoss':>8}  {'TrFeed':>7}  {'TeLoss':>8}  {'TeFeed':>7}  "
          f"{'TeSpeed':>8}  {'TeDoc':>6}  {'TeF1':>6}")
    print("-" * 66)

    for epoch in range(1, args.epochs + 1):
        tr = train_epoch(model, train_dl, criteria, args.w_speed, args.w_doc, optimizer, device)
        te = eval_epoch(model, test_dl, criteria, args.w_speed, args.w_doc, device)
        scheduler.step()

        if te["acc_feed"] > best_feed_acc:
            best_feed_acc, best_epoch = te["acc_feed"], epoch
            torch.save(model.state_dict(), out_dir / f"{tag}_best.pt")

        history.append({
            "epoch": epoch,
            "tr_loss": round(tr["loss"], 4), "tr_acc_feed": round(tr["acc_feed"], 4),
            "tr_acc_speed": round(tr["acc_speed"], 4), "tr_acc_doc": round(tr["acc_doc"], 4),
            "te_loss": round(te["loss"], 4), "te_acc_feed": round(te["acc_feed"], 4),
            "te_acc_speed": round(te["acc_speed"], 4), "te_acc_doc": round(te["acc_doc"], 4),
            "te_f1_feed": round(te["f1_feed"], 4),
        })
        print(f"{epoch:>4}  {tr['loss']:>8.4f}  {tr['acc_feed']:>7.3f}  {te['loss']:>8.4f}  "
              f"{te['acc_feed']:>7.3f}  {te['acc_speed']:>8.3f}  {te['acc_doc']:>6.3f}  "
              f"{te['f1_feed']:>6.3f}")

    # Reload the best-feed-epoch checkpoint for run-level and final diagnostics.
    model.load_state_dict(torch.load(out_dir / f"{tag}_best.pt", map_location=device))
    hard_acc, soft_acc, n_runs = feed_run_level_accuracy(
        model, test["paths"], test["labels"]["feed"], test["run_ids"], val_tf, device
    )
    te_final = eval_epoch(model, test_dl, criteria, args.w_speed, args.w_doc, device)

    print(f"\nBest feed window-level test acc : {best_feed_acc:.3f}  (epoch {best_epoch})")
    print(f"Feed run-level hard-vote acc    : {hard_acc:.3f}  ({int(round(hard_acc * n_runs))}/{n_runs})")
    print(f"Feed run-level soft-vote acc    : {soft_acc:.3f}  ({int(round(soft_acc * n_runs))}/{n_runs})")
    print(f"Aux-head window acc (best-feed-epoch ckpt): speed={te_final['acc_speed']:.3f}  "
          f"doc={te_final['acc_doc']:.3f}")

    hist_path = out_dir / f"{tag}_history.json"
    with open(hist_path, "w") as f:
        json.dump({
            "task": "multitask_feed", "scalogram": scalo_tag, "arch": args.arch,
            "epochs": args.epochs, "lr": args.lr, "seed": args.seed,
            "w_speed": args.w_speed, "w_doc": args.w_doc, "dropout": args.dropout,
            "label_smooth": args.label_smooth, "noise_std": args.noise_std,
            "split_id": args.split_id,
            "best_epoch": best_epoch, "best_feed_window_acc": round(best_feed_acc, 4),
            "final_te_acc_speed": round(te_final["acc_speed"], 4),
            "final_te_acc_doc": round(te_final["acc_doc"], 4),
            "feed_run_acc_hard": round(hard_acc, 4),
            "feed_run_acc_soft": round(soft_acc, 4),
            "n_test_runs": n_runs,
            "history": history,
        }, f, indent=2)
    print(f"\nHistory saved to {hist_path}")


if __name__ == "__main__":
    main()
