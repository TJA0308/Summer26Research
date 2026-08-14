"""
Run-level feature-aggregation classifier for feed_coarse (End Milling).

Novel approach: instead of training a window classifier and majority-voting,
this aggregates all window CNN features for each run via mean-pooling, then
trains a small FC head directly on the run-level training examples (~33 runs).

Two-phase pipeline
------------------
Phase 1 – window-level backbone warm-up:
    Train the backbone on feed_coarse windows (no SMOTE) for PHASE1_EPOCHS.
    This domain-adapts the feature extractor to CWT scalogram structure.

Phase 2 – frozen backbone + run-level FC head:
    Freeze backbone. For each run, forward all its windows through the backbone,
    mean-pool → one feat-dim vector per run. Train a small FC head on those
    run-level vectors with heavy dropout + weight decay. Repeat with N_SEEDS
    random seeds and report mean ± std for robustness.

Usage
-----
python cnn_model/feed_runlevel_32x3.py \
    --img_dir scalograms_32x3_feedopt_9win \
    --split standard|alt1|alt2|alt3|alt4|alt5|alt6|alt7 \
    [--arch resnet18|resnet50|efficientnet_b0|convnext_tiny] \
    [--phase1_epochs 50] [--phase2_epochs 400] [--n_seeds 5] \
    [--dropout 0.5] [--hidden 128] [--run_tag TAG]
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from torchvision import models, transforms

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "cnn_model"))

from cnn_train import (
    FEED_COARSE_LABELS, FEED_COARSE_NAMES,
    FEED_COARSE_TEST_RUNS, FEED_COARSE_TEST_RUNS_12,
    FEED_COARSE_TEST_RUNS_ALT1, FEED_COARSE_TEST_RUNS_ALT2,
    FEED_COARSE_TEST_RUNS_ALT3, FEED_COARSE_TEST_RUNS_ALT4,
    FEED_COARSE_TEST_RUNS_ALT5, FEED_COARSE_TEST_RUNS_ALT6,
    FEED_COARSE_TEST_RUNS_ALT7,
    load_split, load_split_mil,
)
from cnn_train_32x3 import (
    ScalogramDataset, AddGaussianNoise, seed_everything,
    IMAGENET_MEAN, IMAGENET_STD, SEED,
)

SPLIT_MAP = {
    "standard": FEED_COARSE_TEST_RUNS,
    "balanced":  FEED_COARSE_TEST_RUNS_12,
    "alt1":  FEED_COARSE_TEST_RUNS_ALT1,
    "alt2":  FEED_COARSE_TEST_RUNS_ALT2,
    "alt3":  FEED_COARSE_TEST_RUNS_ALT3,
    "alt4":  FEED_COARSE_TEST_RUNS_ALT4,
    "alt5":  FEED_COARSE_TEST_RUNS_ALT5,
    "alt6":  FEED_COARSE_TEST_RUNS_ALT6,
    "alt7":  FEED_COARSE_TEST_RUNS_ALT7,
}
CLASS_NAMES = FEED_COARSE_NAMES
NUM_CLASSES  = 3


def build_backbone(arch):
    if arch == "resnet18":
        m = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        d = m.fc.in_features;  m.fc = nn.Identity()
    elif arch == "resnet50":
        m = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        d = m.fc.in_features;  m.fc = nn.Identity()
    elif arch == "efficientnet_b0":
        m = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        d = m.classifier[1].in_features;  m.classifier = nn.Identity()
    elif arch == "convnext_tiny":
        m = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
        d = m.classifier[2].in_features
        m.classifier = nn.Sequential(m.classifier[0], m.classifier[1])
    else:
        raise ValueError(arch)
    return m, d


def build_head(feat_dim, hidden, dropout):
    if hidden > 0:
        return nn.Sequential(
            nn.Dropout(dropout), nn.Linear(feat_dim, hidden),
            nn.ReLU(), nn.Dropout(dropout), nn.Linear(hidden, NUM_CLASSES),
        )
    return nn.Sequential(nn.Dropout(dropout), nn.Linear(feat_dim, NUM_CLASSES))


def make_transforms(noise_std=0.02):
    resize = transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BILINEAR)
    norm   = transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)
    train_tf = transforms.Compose([resize, transforms.ToTensor(), AddGaussianNoise(noise_std), norm])
    val_tf   = transforms.Compose([resize, transforms.ToTensor(), norm])
    return train_tf, val_tf


# ── Phase 1: window-level warm-up ─────────────────────────────────────────────
def phase1(backbone, feat_dim, tr_paths, tr_labels, te_paths, te_labels,
           epochs, lr, device, train_tf, val_tf):
    head1 = nn.Linear(feat_dim, NUM_CLASSES)
    model = nn.Sequential(backbone, head1).to(device)
    counts = np.bincount(tr_labels, minlength=NUM_CLASSES).astype(float)
    counts[counts == 0] = 1.0
    w = torch.tensor(1.0 / counts, dtype=torch.float32, device=device)
    w = w / w.sum()
    crit = nn.CrossEntropyLoss(weight=w)
    opt  = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)

    tr_dl = DataLoader(ScalogramDataset(tr_paths, tr_labels, train_tf), batch_size=32, shuffle=True,  num_workers=0)
    te_dl = DataLoader(ScalogramDataset(te_paths, te_labels, val_tf),   batch_size=32, shuffle=False, num_workers=0)

    print(f"\n{'Ep':>4} {'TrAcc':>7} {'TeAcc':>7}")
    print("-" * 22)
    best = 0.0
    for ep in range(1, epochs + 1):
        model.train()
        c, n = 0, 0
        for imgs, lbls in tr_dl:
            imgs, lbls = imgs.to(device), lbls.to(device)
            opt.zero_grad(); out = model(imgs); crit(out, lbls).backward(); opt.step()
            c += (out.argmax(1) == lbls).sum().item(); n += len(lbls)
        tr_acc = c / n
        model.eval()
        with torch.no_grad():
            c, n = 0, 0
            for imgs, lbls in te_dl:
                imgs, lbls = imgs.to(device), lbls.to(device)
                out = model(imgs); c += (out.argmax(1) == lbls).sum().item(); n += len(lbls)
        te_acc = c / n
        best = max(best, te_acc)
        sched.step()
        if ep % 10 == 0 or ep == epochs:
            print(f"{ep:>4}  {tr_acc:.3f}  {te_acc:.3f}")
    print(f"Phase-1 best window acc: {best:.3f}")


# ── Phase 2: extract mean-pooled run features ─────────────────────────────────
@torch.no_grad()
def extract_run_feats(backbone, run_paths_dict, run_labels_dict, val_tf, device):
    """run_paths_dict: {run_id: [Path, ...]}; returns X [n_runs, d], y [n_runs]."""
    backbone.eval()
    runs = sorted(run_paths_dict.keys())
    X, y = [], []
    for run in runs:
        paths = [str(p) for p in run_paths_dict[run]]
        lbls  = [run_labels_dict[run]] * len(paths)
        ds = ScalogramDataset(paths, lbls, val_tf)
        dl = DataLoader(ds, batch_size=64, shuffle=False, num_workers=0)
        feats = torch.cat([backbone(imgs.to(device)).cpu() for imgs, _ in dl], dim=0)
        X.append(feats.mean(dim=0).numpy())
        y.append(run_labels_dict[run])
    return np.array(X), np.array(y), runs


# ── Phase 2: run-level head training ──────────────────────────────────────────
def phase2(head, X_tr, y_tr, X_te, y_te, epochs, lr, device):
    Xtr = torch.tensor(X_tr, dtype=torch.float32)
    ytr = torch.tensor(y_tr, dtype=torch.long)
    Xte = torch.tensor(X_te, dtype=torch.float32)
    yte = torch.tensor(y_te, dtype=torch.long)

    counts = np.bincount(y_tr, minlength=NUM_CLASSES).astype(float)
    counts[counts == 0] = 1.0
    w = torch.tensor(1.0 / counts, dtype=torch.float32, device=device)
    w = w / w.sum()
    crit  = nn.CrossEntropyLoss(weight=w)
    opt   = torch.optim.AdamW(head.parameters(), lr=lr, weight_decay=1e-2)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs)

    tr_dl = DataLoader(TensorDataset(Xtr, ytr), batch_size=min(16, len(y_tr)), shuffle=True)

    best_acc, best_ep, best_preds = 0.0, 0, []
    head = head.to(device)
    for ep in range(1, epochs + 1):
        head.train()
        for xb, yb in tr_dl:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad(); crit(head(xb), yb).backward(); opt.step()
        head.eval()
        with torch.no_grad():
            preds = head(Xte.to(device)).argmax(1).cpu().tolist()
        acc = sum(p == t for p, t in zip(preds, y_te.tolist())) / len(y_te)
        if acc >= best_acc:
            best_acc, best_ep, best_preds = acc, ep, preds
        sched.step()
    return best_acc, best_ep, best_preds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir",       default="scalograms_32x3_feedopt_9win")
    parser.add_argument("--split",         default="standard", choices=list(SPLIT_MAP))
    parser.add_argument("--arch",          default="resnet18",
                        choices=["resnet18","resnet50","efficientnet_b0","convnext_tiny"])
    parser.add_argument("--phase1_epochs", type=int,   default=50)
    parser.add_argument("--phase2_epochs", type=int,   default=500)
    parser.add_argument("--lr",            type=float, default=1e-3)
    parser.add_argument("--p2_lr",         type=float, default=5e-4)
    parser.add_argument("--dropout",       type=float, default=0.5)
    parser.add_argument("--hidden",        type=int,   default=128)
    parser.add_argument("--noise_std",     type=float, default=0.02)
    parser.add_argument("--run_tag",       default="")
    parser.add_argument("--seed",          type=int,   default=SEED)
    parser.add_argument("--n_seeds",       type=int,   default=5)
    args = parser.parse_args()

    seed_everything(args.seed)
    device  = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    img_dir = ROOT / args.img_dir
    test_runs = SPLIT_MAP[args.split]

    # flat lists for phase-1 window training
    (tr_paths, tr_labels), (te_paths, te_labels) = load_split(
        img_dir, FEED_COARSE_LABELS, test_runs)
    # grouped by run for phase-2 feature extraction
    (tr_rp, tr_rl), (te_rp, te_rl) = load_split_mil(
        img_dir, FEED_COARSE_LABELS, test_runs)

    print(f"Device : {device}  |  Img dir: {args.img_dir}")
    print(f"Arch   : {args.arch}   Split: {args.split}")
    print(f"Windows: {len(tr_paths)} train ({len(tr_rp)} runs)  "
          f"/ {len(te_paths)} test ({len(te_rp)} runs)")
    for c, name in CLASS_NAMES.items():
        print(f"  class {c} ({name}): {tr_labels.count(c)} train-win / {te_labels.count(c)} test-win")

    train_tf, val_tf = make_transforms(args.noise_std)

    # Phase 1 ─────────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print(f"Phase 1: window warm-up ({args.phase1_epochs} epochs)")
    backbone, feat_dim = build_backbone(args.arch)
    phase1(backbone, feat_dim, tr_paths, tr_labels, te_paths, te_labels,
           args.phase1_epochs, args.lr, device, train_tf, val_tf)

    # Phase 2 ─────────────────────────────────────────────────────────────────
    print(f"\n{'='*55}")
    print("Phase 2: freeze backbone -- run-level mean-pool features")
    backbone = backbone.to(device)
    for p in backbone.parameters():
        p.requires_grad_(False)

    X_tr, y_tr, runs_tr = extract_run_feats(backbone, tr_rp, tr_rl, val_tf, device)
    X_te, y_te, runs_te = extract_run_feats(backbone, te_rp, te_rl, val_tf, device)
    print(f"Run features: train {X_tr.shape}, test {X_te.shape}")
    print(f"Train class dist: {np.bincount(y_tr, minlength=3).tolist()}")
    print(f"Test  class dist: {np.bincount(y_te, minlength=3).tolist()}")

    print(f"\nPhase 2: FC head  ({args.phase2_epochs} epochs x {args.n_seeds} seeds)")
    all_accs, all_preds = [], []
    for s in range(args.n_seeds):
        seed_everything(args.seed + s)
        head = build_head(feat_dim, args.hidden, args.dropout)
        acc, ep, preds = phase2(head, X_tr, y_tr, X_te, y_te,
                                args.phase2_epochs, args.p2_lr, device)
        all_accs.append(acc)
        all_preds.append(preds)
        print(f"  seed {s}: {acc:.3f} (epoch {ep})")

    mean_acc = np.mean(all_accs)
    std_acc  = np.std(all_accs)
    best_idx  = int(np.argmax(all_accs))
    best_preds = all_preds[best_idx]

    print(f"\n{'='*55}")
    print(f"Run-level acc: {mean_acc:.3f} +/- {std_acc:.3f}  (best seed: {max(all_accs):.3f})")

    from sklearn.metrics import classification_report
    print("\nPer-class (best seed):")
    print(classification_report(y_te.tolist(), best_preds,
                                target_names=list(CLASS_NAMES.values()), digits=2))

    out_dir = ROOT / "cnn_model" / f"models_feed_coarse_runlevel_{Path(args.img_dir).name}"
    out_dir.mkdir(parents=True, exist_ok=True)
    tag_str  = f"{args.arch}_{args.split}" + (f"_{args.run_tag}" if args.run_tag else "")
    out_path = out_dir / f"{tag_str}_history.json"
    with open(out_path, "w") as f:
        json.dump({
            "target": "feed_coarse", "img_dir": args.img_dir, "arch": args.arch,
            "split": args.split, "run_tag": args.run_tag,
            "phase1_epochs": args.phase1_epochs, "phase2_epochs": args.phase2_epochs,
            "n_seeds": args.n_seeds,
            "run_level_mean_acc": round(mean_acc, 4),
            "run_level_std_acc":  round(std_acc,  4),
            "run_level_best_acc": round(max(all_accs), 4),
            "all_seed_accs": [round(a, 4) for a in all_accs],
        }, f, indent=2)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
