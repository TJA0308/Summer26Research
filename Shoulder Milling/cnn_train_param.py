"""
CNN training for Shoulder Milling -- process parameter prediction
(speed, feed, or depth-of-cut) from Option C (32x12) or Option D (32x3)
scalograms, using the fixed train/test splits documented in README.md
("Three Model Splits").

Targets (--target):
    speed  -- 2-class: 2500 RPM vs 3500 RPM
    feed   -- 3-class: f3 vs f5 vs f7
    doc    -- 4-class: one of the 4 (Y-doc, Z-doc) combinations

Scalogram folder (--img_dir, relative to this script):
    scalograms_32x12   (Option C, all 12 feature columns)
    scalograms_32x3    (Option D, FFT / 64mexican / 64coif only)

Architectures (--arch): resnet18, resnet50, efficientnet_b0, convnext_tiny

Each target uses its own fixed 48-train/24-test run-level split, not an
arbitrary held-out side, because each split is specifically designed so
the test set isolates the target parameter as the only varying factor
(see README.md). Run membership is identified by run_id = side + feed
letter (e.g. "1a" = side 1, f3), matching the labels.csv "side"/"feed"
columns -- the same convention used to name the scalogram PNGs.

Usage examples:
    python cnn_train_param.py --target speed --img_dir scalograms_32x12 --arch resnet18      --lr 1e-3
    python cnn_train_param.py --target feed  --img_dir scalograms_32x3  --arch convnext_tiny --lr 1e-4 --no_smote
"""

import argparse
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from imblearn.over_sampling import SMOTE
from PIL import Image
from sklearn.metrics import classification_report, f1_score
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms

SEED = 42
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

FEED_TO_LETTER = {"f3": "a", "f5": "b", "f7": "c"}
FEED_TO_CLASS  = {"f3": 0, "f5": 1, "f7": 2}
SIDE_TO_SPEED  = {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1}   # 0=2500rpm 1=3500rpm
SIDE_TO_DOC    = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3}   # 4 Y/Z-doc combos

TARGETS = {
    "speed": {
        "num_classes": 2,
        "class_names": ["2500rpm", "3500rpm"],
        "test_runs":  ["1a", "2a", "3b", "4b", "5c", "6c", "7a", "8a"],
        "train_runs": ["1b", "1c", "2b", "2c", "3a", "3c", "4a", "4c",
                        "5a", "5b", "6a", "6b", "7b", "7c", "8b", "8c"],
    },
    "feed": {
        "num_classes": 3,
        "class_names": ["f3", "f5", "f7"],
        "test_runs":  ["1a", "1b", "1c", "3c", "6a", "8a", "8b", "8c"],
        "train_runs": ["2a", "2b", "2c", "3a", "3b", "4a", "4b", "4c",
                        "5a", "5b", "5c", "6b", "6c", "7a", "7b", "7c"],
    },
    "doc": {
        "num_classes": 4,
        "class_names": ["Y50Z250", "Y25Z250", "Y50Z125", "Y25Z125"],
        "test_runs":  ["1a", "2b", "3a", "4b", "5a", "6b", "7a", "8b"],
        "train_runs": ["1b", "1c", "2a", "2c", "3b", "3c", "4a", "4c",
                        "5b", "5c", "6a", "6c", "7b", "7c", "8a", "8c"],
    },
}


def label_for(target: str, side: int, feed: str) -> int:
    if target == "speed":
        return SIDE_TO_SPEED[side]
    if target == "feed":
        return FEED_TO_CLASS[feed]
    if target == "doc":
        return SIDE_TO_DOC[side]
    raise ValueError(target)


def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ── dataset ────────────────────────────────────────────────────────────────────
class ScalogramDataset(Dataset):
    def __init__(self, paths, labels, transform=None):
        self.paths, self.labels, self.transform = paths, labels, transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]


class SyntheticDataset(Dataset):
    def __init__(self, tensors, labels):
        self.tensors, self.labels = tensors, labels

    def __len__(self):
        return len(self.tensors)

    def __getitem__(self, idx):
        return self.tensors[idx], self.labels[idx]


def build_transforms():
    train_tf = transforms.Compose([
        transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.15, contrast=0.15),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    return train_tf, val_tf


# ── model factory ──────────────────────────────────────────────────────────────
def build_model(arch: str, num_classes: int) -> nn.Module:
    if arch == "resnet18":
        m = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        m.fc = nn.Linear(m.fc.in_features, num_classes)
    elif arch == "resnet50":
        m = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        m.fc = nn.Linear(m.fc.in_features, num_classes)
    elif arch == "efficientnet_b0":
        m = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        m.classifier[1] = nn.Linear(m.classifier[1].in_features, num_classes)
    elif arch == "convnext_tiny":
        m = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
        m.classifier[2] = nn.Linear(m.classifier[2].in_features, num_classes)
    else:
        raise ValueError(f"Unknown arch: {arch}")
    return m


# ── data loading ───────────────────────────────────────────────────────────────
def load_split(img_dir: Path, target: str):
    df = pd.read_csv(img_dir / "labels.csv")
    df["run_id"] = df["side"].astype(str) + df["feed"].map(FEED_TO_LETTER)
    df["label"]  = df.apply(lambda r: label_for(target, r["side"], r["feed"]), axis=1)

    spec     = TARGETS[target]
    train_df = df[df["run_id"].isin(spec["train_runs"])].reset_index(drop=True)
    test_df  = df[df["run_id"].isin(spec["test_runs"])].reset_index(drop=True)

    def to_lists(sub):
        paths   = [img_dir / row.filename for _, row in sub.iterrows()]
        labels  = sub["label"].tolist()
        run_ids = sub["run"].tolist()
        return paths, labels, run_ids

    return to_lists(train_df), to_lists(test_df)


# ── SMOTE ──────────────────────────────────────────────────────────────────────
def apply_smote(paths: list, labels: list, img_h: int, img_w: int):
    """Flattens each training image to a pixel vector, balances classes with
    SMOTE, returns pre-tensorised (224x224, normalised) synthetic samples."""
    raw_tf = transforms.Compose([
        transforms.Resize((img_h, img_w), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
    ])

    X = []
    for p in paths:
        img = Image.open(p).convert("RGB")
        t   = raw_tf(img)
        X.append(t.numpy().flatten())
    X = np.array(X, dtype=np.float32)
    y = np.array(labels, dtype=int)

    counts = np.bincount(y)
    print(f"\n  [SMOTE] Before: {dict(enumerate(counts))}")

    min_count = counts[counts > 0].min()
    if min_count < 2:
        print("  [SMOTE] Skipped -- a class has fewer than 2 samples")
        return [], []

    smote = SMOTE(random_state=SEED, k_neighbors=min(5, min_count - 1))
    X_res, y_res = smote.fit_resample(X, y)

    counts_after = np.bincount(y_res)
    n_synthetic  = len(X_res) - len(X)
    print(f"  [SMOTE] After:  {dict(enumerate(counts_after))}  (+{n_synthetic} synthetic)")

    norm = transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)
    synthetic_tensors, synthetic_labels = [], []
    for i in range(len(X), len(X_res)):
        arr = np.clip(X_res[i].reshape(3, img_h, img_w), 0, 1)
        t   = torch.from_numpy(arr)
        t   = transforms.functional.resize(
            t, [224, 224], interpolation=transforms.InterpolationMode.BILINEAR, antialias=True
        )
        t   = norm(t)
        synthetic_tensors.append(t)
        synthetic_labels.append(int(y_res[i]))
    return synthetic_tensors, synthetic_labels


# ── training / evaluation ──────────────────────────────────────────────────────
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        out  = model(imgs)
        loss = criterion(out, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    all_preds, all_labels  = [], []
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        out  = model(imgs)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        preds = out.argmax(1)
        correct    += (preds == labels).sum().item()
        n          += len(labels)
        all_preds.extend(preds.cpu().tolist())
        all_labels.extend(labels.cpu().tolist())
    return total_loss / n, correct / n, all_preds, all_labels


@torch.no_grad()
def majority_vote_accuracy(model, paths, labels, run_ids, val_tf, device):
    """Predict each window, then majority-vote the 3 windows per run."""
    model.eval()
    ds = ScalogramDataset(paths, labels, val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)

    all_preds = []
    for imgs, _ in dl:
        imgs = imgs.to(device)
        all_preds.extend(model(imgs).argmax(1).cpu().tolist())

    run_preds, run_true = {}, {}
    for pred, true, run in zip(all_preds, labels, run_ids):
        run_preds.setdefault(run, []).append(pred)
        run_true[run] = true

    correct = 0
    vote_preds, vote_true = [], []
    for run in run_true:
        voted = max(set(run_preds[run]), key=run_preds[run].count)
        vote_preds.append(voted)
        vote_true.append(run_true[run])
        if voted == run_true[run]:
            correct += 1

    return correct / len(run_true), vote_preds, vote_true


# ── main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, choices=list(TARGETS.keys()))
    parser.add_argument("--img_dir", required=True,
                        help="scalograms_32x12 or scalograms_32x3 (relative to this script)")
    parser.add_argument("--arch", default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"])
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch",  type=int, default=8)
    parser.add_argument("--lr",     type=float, default=1e-3)
    parser.add_argument("--no_smote", action="store_true",
                        help="Disable SMOTE oversampling")
    args = parser.parse_args()

    seed_everything(SEED)

    img_dir   = Path(__file__).parent / args.img_dir
    scalo_tag = img_dir.name.replace("scalograms_", "")   # "32x12" or "32x3"
    out_dir   = Path(__file__).parent / f"models_{args.target}_{scalo_tag}"
    out_dir.mkdir(exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    spec   = TARGETS[args.target]
    print(f"Device    : {device}")
    print(f"Target    : {args.target}  ({spec['num_classes']} classes: {spec['class_names']})")
    print(f"Scalogram : {scalo_tag}")
    print(f"Arch      : {args.arch}   LR: {args.lr}")

    (tr_paths, tr_labels, tr_runs), (te_paths, te_labels, te_runs) = load_split(img_dir, args.target)
    print(f"Train windows : {len(tr_paths)}  |  Test windows : {len(te_paths)}")

    with Image.open(tr_paths[0]) as im0:
        img_w, img_h = im0.size   # PIL reports (width, height)

    train_tf, val_tf = build_transforms()

    use_smote = not args.no_smote
    if use_smote:
        syn_tensors, syn_labels = apply_smote(tr_paths, tr_labels, img_h, img_w)
    else:
        syn_tensors, syn_labels = [], []

    real_ds = ScalogramDataset(tr_paths, tr_labels, train_tf)
    test_ds = ScalogramDataset(te_paths, te_labels, val_tf)

    if use_smote and syn_tensors:
        syn_ds     = SyntheticDataset(syn_tensors, syn_labels)
        train_ds   = torch.utils.data.ConcatDataset([real_ds, syn_ds])
        all_labels = tr_labels + syn_labels
    else:
        train_ds   = real_ds
        all_labels = tr_labels

    counts = np.bincount(all_labels, minlength=spec["num_classes"]).astype(float)
    counts[counts == 0] = 1.0
    weights = torch.tensor(1.0 / counts, dtype=torch.float32).to(device)
    weights = weights / weights.sum()
    print(f"\nClass weights {spec['class_names']}: {weights.cpu().numpy().round(3)}")

    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=0)
    test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

    model     = build_model(args.arch, num_classes=spec["num_classes"]).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    tag = f"{args.arch}_lr{args.lr:g}"
    best_acc, best_epoch, history = 0.0, 0, []

    print(f"\n{'Ep':>4}  {'TrLoss':>8}  {'TrAcc':>7}  {'TeLoss':>8}  {'TeAcc':>7}  {'TeF1':>6}")
    print("-" * 50)

    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(model, train_dl, criterion, optimizer, device)
        te_loss, te_acc, te_preds, te_lbls = eval_epoch(model, test_dl, criterion, device)
        te_f1 = f1_score(te_lbls, te_preds, average="macro", zero_division=0)
        scheduler.step()

        if te_acc > best_acc:
            best_acc, best_epoch = te_acc, epoch
            torch.save(model.state_dict(), out_dir / f"{tag}_best.pt")

        history.append({
            "epoch": epoch, "tr_loss": round(tr_loss, 4), "tr_acc": round(tr_acc, 4),
            "te_loss": round(te_loss, 4), "te_acc": round(te_acc, 4), "te_f1": round(te_f1, 4),
        })
        print(f"{epoch:>4}  {tr_loss:>8.4f}  {tr_acc:>7.3f}  {te_loss:>8.4f}  {te_acc:>7.3f}  {te_f1:>6.3f}")

    model.load_state_dict(torch.load(out_dir / f"{tag}_best.pt", map_location=device))
    run_acc, vote_preds, vote_true = majority_vote_accuracy(
        model, te_paths, te_labels, te_runs, val_tf, device
    )

    print(f"\nBest window-level test acc : {best_acc:.3f}  (epoch {best_epoch})")
    print(f"Run-level majority vote acc: {run_acc:.3f}  "
          f"({int(round(run_acc * len(set(te_runs))))}/{len(set(te_runs))} runs)")
    print(f"\nPer-class report (run-level, best model):")
    print(classification_report(vote_true, vote_preds, target_names=spec["class_names"], zero_division=0))

    hist_path = out_dir / f"{tag}_history.json"
    with open(hist_path, "w") as f:
        json.dump({
            "target": args.target, "scalogram": scalo_tag, "arch": args.arch,
            "epochs": args.epochs, "lr": args.lr, "smote": use_smote,
            "best_window_acc": round(best_acc, 4), "best_epoch": best_epoch,
            "run_level_acc": round(run_acc, 4), "history": history,
        }, f, indent=2)
    print(f"\nHistory saved to {hist_path}")


if __name__ == "__main__":
    main()
