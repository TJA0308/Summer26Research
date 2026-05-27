"""
Train a CNN on 4-channel SES (Squared Envelope Spectrum) CWT scalograms.

Scalograms must be generated first:
    python cnn_model/scalogram_hilbert.py --input_dir data --output_dir scalograms_ses_10w --n_windows 10

Channel layout (produced by scalogram_hilbert.py):
    ch 0: ai4 raw CWT
    ch 1: ai6 raw CWT
    ch 2: SES(ai4) CWT  [squared envelope |H{x}|^2]
    ch 3: SES(ai6) CWT  [squared envelope |H{x}|^2]

Larger test sets than cnn_train.py — each class has full DOC-level coverage:
    Speed : 15 test (3/class × 5 classes, one per DOC)  | 30 train
    DOC   : 14 test (5+5+4 across all speeds)            | 31 train
"""

import argparse
import random
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import models

sys.path.insert(0, str(Path(__file__).parent))
from cnn_train import (
    SPEED_LABELS, SPEED_NAMES,
    FEED_TEST_RUNS,
    FEED_COARSE_LABELS, FEED_COARSE_NAMES,
    DOC_LABELS,   DOC_NAMES,
    RA_LABELS,    RA_NAMES, RA_TEST_RUNS,
    build_scheduler,
)

SEED = 42

# ── Speed: 15 test (3 per RPM class, one per DOC level), 30 train ─────────
SPEED_TEST_RUNS_H = {
    "run9",  "run22", "run37",   # 1500 rpm: DOC 0.030, 0.060, 0.015
    "run12", "run27", "run40",   # 2000 rpm: DOC 0.030, 0.060, 0.015
    "run15", "run28", "run43",   # 3000 rpm: DOC 0.030, 0.060, 0.015
    "run2",  "run16", "run31",   # 4000 rpm: DOC 0.015, 0.030, 0.060
    "run5",  "run19", "run36",   # 5000 rpm: DOC 0.015, 0.030, 0.060
}

# ── DOC: 14 test (5+5+4 across all speeds), 31 train ──────────────────────
DOC_TEST_RUNS_H = {
    "run1",  "run5",  "run43", "run38", "run41",  # 0.015 mm: 4000,5000,3000,1500,2000 rpm
    "run7",  "run14", "run19", "run11", "run16",  # 0.030 mm: 1500,3000,5000,2000,4000 rpm
    "run22", "run29", "run36", "run25",           # 0.060 mm: 1500,3000,5000,2000 rpm
}

# ── Feed coarse: unchanged (6 test, 39 train) ─────────────────────────────
FEED_COARSE_TEST_RUNS_H = FEED_TEST_RUNS


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


# ── Dataset ────────────────────────────────────────────────────────────────

class NpyScalogramDataset(Dataset):
    """Loads (4, H, W) float32 .npy arrays."""

    def __init__(self, paths, labels):
        self.paths  = paths
        self.labels = labels

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        arr = torch.from_numpy(np.load(self.paths[idx]))  # (4, H, W) float32 [0,1]
        return arr, self.labels[idx]


def load_smote_npy(img_dir, csv_name):
    """Load synthetic .npy paths and labels listed in smote_hilbert CSV."""
    import csv as _csv
    smote_csv = img_dir / csv_name
    if not smote_csv.exists():
        return [], []
    paths, labels = [], []
    with open(smote_csv) as f:
        for row in _csv.DictReader(f):
            for npy in sorted(img_dir.glob(f"{row['run']}_w*.npy")):
                paths.append(npy)
                labels.append(int(row["label"]))
    return paths, labels


def load_split_npy(img_dir, label_map, test_runs):
    """Split .npy files (no smote_ prefix) into train/test lists."""
    train_paths, train_labels = [], []
    test_paths,  test_labels  = [], []
    train_runs = set(label_map.keys()) - test_runs
    for npy in sorted(img_dir.glob("*.npy")):
        stem = npy.stem          # e.g. "run5_w3"
        run  = stem.split("_w")[0]
        label = label_map.get(run)
        if label is None:
            continue
        if run in test_runs:
            test_paths.append(npy);  test_labels.append(label)
        elif run in train_runs:
            train_paths.append(npy); train_labels.append(label)
    return (train_paths, train_labels), (test_paths, test_labels)


# ── Model ──────────────────────────────────────────────────────────────────

def _patch_first_conv(old_conv, new_conv):
    """Copy pretrained 3-ch weights into new_conv; seed 4th channel from their average."""
    with torch.no_grad():
        new_conv.weight[:, :3] = old_conv.weight
        new_conv.weight[:, 3]  = old_conv.weight.mean(dim=1)
        if old_conv.bias is not None and new_conv.bias is not None:
            new_conv.bias.copy_(old_conv.bias)


def build_model_4ch(backbone, num_classes, freeze_backbone=False, dropout=0.0):
    """
    Build a pretrained backbone with its first conv patched to accept 4 channels.
    The first 3 channels keep their ImageNet weights; the 4th channel is seeded
    from the channel-wise average of those weights so the full network starts warm.
    """
    def _head(in_features):
        return (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_features, num_classes))
                if dropout > 0 else nn.Linear(in_features, num_classes))

    if backbone == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        new_conv = nn.Conv2d(4, 64, kernel_size=7, stride=2, padding=3, bias=False)
        _patch_first_conv(model.conv1, new_conv)
        model.conv1 = new_conv
        model.fc = _head(model.fc.in_features)

    elif backbone == "resnet50":
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        new_conv = nn.Conv2d(4, 64, kernel_size=7, stride=2, padding=3, bias=False)
        _patch_first_conv(model.conv1, new_conv)
        model.conv1 = new_conv
        model.fc = _head(model.fc.in_features)

    elif backbone == "efficientnet_b0":
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        c = model.features[0][0]
        new_conv = nn.Conv2d(4, c.out_channels, kernel_size=c.kernel_size,
                             stride=c.stride, padding=c.padding, bias=False)
        _patch_first_conv(c, new_conv)
        model.features[0][0] = new_conv
        model.classifier[1] = _head(model.classifier[1].in_features)

    elif backbone == "convnext_tiny":
        model = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
        c = model.features[0][0]
        new_conv = nn.Conv2d(4, c.out_channels, kernel_size=c.kernel_size,
                             stride=c.stride, padding=c.padding)
        _patch_first_conv(c, new_conv)
        model.features[0][0] = new_conv
        model.classifier[2] = _head(model.classifier[2].in_features)

    else:
        raise ValueError(f"Unsupported backbone: {backbone}")

    if freeze_backbone:
        for name, p in model.named_parameters():
            if not any(k in name for k in ("fc", "classifier")):
                p.requires_grad = False

    return model


# ── Training helpers ───────────────────────────────────────────────────────

def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        out  = model(imgs)
        loss = criterion(out, labels)
        optimizer.zero_grad()
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
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        out  = model(imgs)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Train on 4-channel Hilbert scalograms (.npy).",
    )
    parser.add_argument("--img_dir",      required=True,
                        help="Directory of .npy scalogram files (from scalogram_hilbert.py)")
    parser.add_argument("--target",       default="speed",
                        choices=["speed", "doc", "feed_coarse", "roughness"])
    parser.add_argument("--backbone",     default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"])
    parser.add_argument("--epochs",       type=int,   default=20)
    parser.add_argument("--lr",           type=float, default=1e-3)
    parser.add_argument("--batch",        type=int,   default=16)
    parser.add_argument("--weight_decay", type=float, default=1e-4)
    parser.add_argument("--scheduler",    default="cosine",
                        choices=["cosine", "cosine_warm", "step", "none"])
    parser.add_argument("--optimizer",    default="adamw", choices=["adam", "adamw"])
    parser.add_argument("--dropout",      type=float, default=0.0)
    parser.add_argument("--weighted_loss", action="store_true")
    parser.add_argument("--freeze",       action="store_true",
                        help="Freeze backbone, train head only")
    parser.add_argument("--save",         default=None,
                        help="Path to save best model (auto-named if omitted)")
    parser.add_argument("--smote",        action="store_true",
                        help="Load synthetic .npy files generated by smote_hilbert.py")
    args = parser.parse_args()

    seed_everything(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── Target config ──────────────────────────────────────────────────────
    if args.target == "speed":
        label_map, class_names, test_runs, num_classes = (
            SPEED_LABELS, SPEED_NAMES, SPEED_TEST_RUNS_H, 5)
        default_save = f"hilbert_speed_{args.backbone}.pt"
    elif args.target == "doc":
        label_map, class_names, test_runs, num_classes = (
            DOC_LABELS, DOC_NAMES, DOC_TEST_RUNS_H, 3)
        default_save = f"hilbert_doc_{args.backbone}.pt"
    elif args.target == "feed_coarse":
        label_map, class_names, test_runs, num_classes = (
            FEED_COARSE_LABELS, FEED_COARSE_NAMES, FEED_COARSE_TEST_RUNS_H, 3)
        default_save = f"hilbert_feed_coarse_{args.backbone}.pt"
    else:  # roughness
        label_map, class_names, test_runs, num_classes = (
            RA_LABELS, RA_NAMES, RA_TEST_RUNS, 3)
        default_save = f"hilbert_roughness_{args.backbone}.pt"

    save_path = args.save or default_save

    smote_csv_names = {
        "speed":       "smote_h_speed_labels.csv",
        "doc":         "smote_h_doc_labels.csv",
        "feed_coarse": "smote_h_feed_coarse_labels.csv",
        "roughness":   "smote_h_roughness_labels.csv",
    }

    img_dir = Path(args.img_dir)
    (train_paths, train_labels), (test_paths, test_labels) = load_split_npy(
        img_dir, label_map, test_runs)

    if not train_paths:
        print("No .npy training files found. Run scalogram_hilbert.py first.")
        return

    if args.smote:
        s_paths, s_labels = load_smote_npy(img_dir, smote_csv_names[args.target])
        if s_paths:
            train_paths  = train_paths  + s_paths
            train_labels = train_labels + s_labels
            print(f"  SMOTE: +{len(s_paths)} synthetic windows loaded")
        else:
            print("  SMOTE: no synthetic files found — run smote_hilbert.py first")

    print(f"\nTarget: {args.target}  |  Train: {len(train_paths)} images | "
          f"Test: {len(test_paths)} images")
    for c, name in class_names.items():
        print(f"  class {c} ({name}): {train_labels.count(c)} train / "
              f"{test_labels.count(c)} test")

    print(f"\nConfig: backbone={args.backbone}  lr={args.lr}  wd={args.weight_decay}"
          f"  batch={args.batch}  epochs={args.epochs}"
          f"  optimizer={args.optimizer}  scheduler={args.scheduler}"
          f"  dropout={args.dropout}  freeze={args.freeze}")

    train_ds = NpyScalogramDataset(train_paths, train_labels)
    test_ds  = NpyScalogramDataset(test_paths,  test_labels)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
    test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

    model = build_model_4ch(args.backbone, num_classes,
                            freeze_backbone=args.freeze,
                            dropout=args.dropout).to(device)

    if args.weighted_loss:
        counts  = np.bincount(train_labels, minlength=num_classes).astype(np.float32)
        weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
        weights = weights / weights.sum() * num_classes
        criterion = nn.CrossEntropyLoss(weight=weights)
        print(f"Class weights: {weights.cpu().numpy().round(3)}")
    else:
        criterion = nn.CrossEntropyLoss()

    opt_cls   = torch.optim.AdamW if args.optimizer == "adamw" else torch.optim.Adam
    optimizer = opt_cls(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr, weight_decay=args.weight_decay,
    )
    scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

    print(f"\n{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} "
          f"{'Test Loss':>10} {'Test Acc':>10}")
    print("-" * 52)

    best_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(model, train_dl, criterion, optimizer, device)
        te_loss, te_acc = eval_epoch(model, test_dl,  criterion, device)
        scheduler.step()
        if te_acc > best_acc:
            best_acc = te_acc
            torch.save(model.state_dict(), save_path)
        print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} "
              f"{te_loss:>10.4f} {te_acc:>10.3f}", flush=True)

    print(f"\nBest test accuracy: {best_acc:.3f}")
    print(f"Model saved to {save_path}")

    # Per-class breakdown on best model
    model.load_state_dict(torch.load(save_path, map_location=device, weights_only=True))
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for imgs, labels in test_dl:
            preds = model(imgs.to(device)).argmax(1).cpu().tolist()
            all_preds.extend(preds)
            all_labels.extend(labels.tolist())

    print("\nPer-class test results (best model):")
    for c, name in class_names.items():
        idx = [i for i, l in enumerate(all_labels) if l == c]
        if idx:
            correct  = sum(all_preds[i] == all_labels[i] for i in idx)
            wrong_as = [all_preds[i] for i in idx if all_preds[i] != all_labels[i]]
            detail   = f"  predicted as {wrong_as}" if wrong_as else ""
            print(f"  class {c} ({name}): {correct}/{len(idx)}{detail}")


if __name__ == "__main__":
    main()
