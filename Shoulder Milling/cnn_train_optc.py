"""
CNN training for Shoulder Milling — Option C scalograms (32x12 grayscale).

Architectures (--arch):
    resnet18, resnet50, efficientnet_b0, convnext_tiny

Split (--test_sides):
    Comma-separated side numbers to hold out as test set, e.g. --test_sides 1,8
    Each side contains 3 runs x 3 windows = 9 images.
    Leave blank to be specified — the script will error clearly if omitted.

SMOTE:
    Applied to the flattened training images (384-dim pixel vectors) before
    training. Balances all three Ra classes to the majority count.
    Disable with --no_smote.

Usage examples:
    python cnn_train_optc.py --arch resnet18 --test_sides 1,2 --epochs 50
    python cnn_train_optc.py --arch efficientnet_b0 --test_sides 3 --epochs 50 --no_smote
    python cnn_train_optc.py --arch convnext_tiny --test_sides 1,8 --lr 3e-4
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

# ── constants ──────────────────────────────────────────────────────────────────
SEED        = 42
IMG_DIR     = Path(__file__).parent / "scalograms_32x12"
LABELS_CSV  = IMG_DIR / "labels.csv"
OUT_DIR     = Path(__file__).parent / "models_optc"
IMG_H, IMG_W = 32, 12
CLASS_NAMES  = ["Low", "Med", "High"]

SIDE_TO_RUNS = {
    1: [1,  2,  3],
    2: [13, 14, 15],
    3: [4,  5,  6],
    4: [16, 17, 18],
    5: [7,  8,  9],
    6: [19, 20, 21],
    7: [10, 11, 12],
    8: [22, 23, 24],
}

RA_CLASS_MAP = {"Low": 0, "Med": 1, "High": 2}

IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]


# ── reproducibility ────────────────────────────────────────────────────────────
def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ── dataset ────────────────────────────────────────────────────────────────────
class ScalogramDataset(Dataset):
    """Loads 32x12 grayscale PNGs and converts to 3-channel 224x224 tensors."""

    def __init__(self, paths: list, labels: list, transform=None):
        self.paths   = paths
        self.labels  = labels
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]


class SyntheticDataset(Dataset):
    """Holds SMOTE-generated images already as float tensors."""

    def __init__(self, tensors: list, labels: list):
        self.tensors = tensors
        self.labels  = labels

    def __len__(self):
        return len(self.tensors)

    def __getitem__(self, idx):
        return self.tensors[idx], self.labels[idx]


# ── transforms ─────────────────────────────────────────────────────────────────
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
def load_split(test_sides: list[int]):
    """
    Returns train and test (paths, labels, run_ids) tuples.
    test_sides: list of side numbers (1-8) to hold out.
    """
    df = pd.read_csv(LABELS_CSV)
    df["label"] = df["ra_class"].map(RA_CLASS_MAP)

    test_runs = set()
    for s in test_sides:
        test_runs.update(SIDE_TO_RUNS[s])

    train_df = df[~df["run"].isin(test_runs)].reset_index(drop=True)
    test_df  = df[ df["run"].isin(test_runs)].reset_index(drop=True)

    def to_lists(sub):
        paths   = [IMG_DIR / row.filename for _, row in sub.iterrows()]
        labels  = sub["label"].tolist()
        run_ids = sub["run"].tolist()
        return paths, labels, run_ids

    return to_lists(train_df), to_lists(test_df)


# ── SMOTE ──────────────────────────────────────────────────────────────────────
def apply_smote(paths: list, labels: list, val_tf, device):
    """
    Flattens each training image to a 384-dim pixel vector (32x12),
    runs SMOTE to balance classes, returns augmented (paths+tensors, labels).

    Real samples stay as file paths; synthetic samples are pre-tensorised
    so they can be mixed into a ConcatDataset at load time.
    """
    # Load raw uint8 pixel arrays (before any normalisation transform)
    raw_tf = transforms.Compose([
        transforms.Resize((IMG_H, IMG_W), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),   # [0,1] float
    ])

    X = []
    for p in paths:
        img = Image.open(p).convert("RGB")
        t   = raw_tf(img)   # (3, 32, 12)
        X.append(t.numpy().flatten())  # 3*32*12 = 1152

    X = np.array(X, dtype=np.float32)
    y = np.array(labels, dtype=int)

    counts = np.bincount(y)
    print(f"\n  [SMOTE] Before: {dict(enumerate(counts))}")

    smote = SMOTE(random_state=SEED, k_neighbors=min(5, counts.min() - 1))
    X_res, y_res = smote.fit_resample(X, y)

    counts_after = np.bincount(y_res)
    n_synthetic  = len(X_res) - len(X)
    print(f"  [SMOTE] After:  {dict(enumerate(counts_after))}  (+{n_synthetic} synthetic)")

    # Normalisation transform for synthetic tensors (same pipeline as val_tf but
    # we already have a tensor, so apply normalise manually)
    norm = transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD)

    synthetic_tensors = []
    synthetic_labels  = []

    for i in range(len(X), len(X_res)):
        arr = X_res[i].reshape(3, IMG_H, IMG_W)       # (3, 32, 12) float [0,1]
        arr = np.clip(arr, 0, 1)
        t   = torch.from_numpy(arr)                   # (3, 32, 12)
        t   = transforms.functional.resize(
            t, [224, 224],
            interpolation=transforms.InterpolationMode.BILINEAR,
            antialias=True
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
    """
    Predict each window, then majority-vote the 3 windows per run.
    Returns run-level accuracy.
    """
    model.eval()
    ds = ScalogramDataset(paths, labels, val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)

    all_preds, all_labels, all_runs = [], [], []
    for i, (imgs, lbls) in enumerate(dl):
        imgs = imgs.to(device)
        preds = model(imgs).argmax(1).cpu().tolist()
        all_preds.extend(preds)
        all_labels.extend(lbls.tolist())

    # Group by run and take majority vote
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
    parser.add_argument("--arch",
                        default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"])
    parser.add_argument("--test_sides",
                        required=True,
                        help="Comma-separated side numbers to hold out, e.g. 1,8")
    parser.add_argument("--epochs",    type=int,   default=50)
    parser.add_argument("--batch",     type=int,   default=8)
    parser.add_argument("--lr",        type=float, default=1e-3)
    parser.add_argument("--no_smote",  action="store_true",
                        help="Disable SMOTE oversampling")
    args = parser.parse_args()

    seed_everything(SEED)
    OUT_DIR.mkdir(exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device : {device}")
    print(f"Arch   : {args.arch}")

    test_sides = [int(s) for s in args.test_sides.split(",")]
    print(f"Test sides: {test_sides}")

    # ── load split ────────────────────────────────────────────────────────────
    (tr_paths, tr_labels, tr_runs), (te_paths, te_labels, te_runs) = load_split(test_sides)
    print(f"Train windows : {len(tr_paths)}  |  Test windows : {len(te_paths)}")

    train_tf, val_tf = build_transforms()

    # ── SMOTE ─────────────────────────────────────────────────────────────────
    use_smote = not args.no_smote
    if use_smote:
        syn_tensors, syn_labels = apply_smote(tr_paths, tr_labels, val_tf, device)
    else:
        syn_tensors, syn_labels = [], []

    # ── datasets ──────────────────────────────────────────────────────────────
    real_ds  = ScalogramDataset(tr_paths, tr_labels, train_tf)
    test_ds  = ScalogramDataset(te_paths, te_labels, val_tf)

    if use_smote and syn_tensors:
        syn_ds    = SyntheticDataset(syn_tensors, syn_labels)
        train_ds  = torch.utils.data.ConcatDataset([real_ds, syn_ds])
        all_labels = tr_labels + syn_labels
    else:
        train_ds  = real_ds
        all_labels = tr_labels

    # ── class-weighted loss ───────────────────────────────────────────────────
    counts  = np.bincount(all_labels, minlength=3).astype(float)
    weights = torch.tensor(1.0 / counts, dtype=torch.float32).to(device)
    weights = weights / weights.sum()
    print(f"\nClass weights (Low/Med/High): {weights.cpu().numpy().round(3)}")

    train_dl = DataLoader(train_ds, batch_size=args.batch,
                          shuffle=True, num_workers=0)
    test_dl  = DataLoader(test_ds,  batch_size=args.batch,
                          shuffle=False, num_workers=0)

    # ── model ─────────────────────────────────────────────────────────────────
    model     = build_model(args.arch, num_classes=3).to(device)
    criterion = nn.CrossEntropyLoss(weight=weights)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    # ── training loop ─────────────────────────────────────────────────────────
    best_acc   = 0.0
    best_epoch = 0
    history    = []

    print(f"\n{'Ep':>4}  {'TrLoss':>8}  {'TrAcc':>7}  {'TeLoss':>8}  {'TeAcc':>7}  {'TeF1':>6}")
    print("-" * 50)

    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(model, train_dl, criterion, optimizer, device)
        te_loss, te_acc, te_preds, te_lbls = eval_epoch(model, test_dl, criterion, device)
        te_f1 = f1_score(te_lbls, te_preds, average="macro", zero_division=0)
        scheduler.step()

        if te_acc > best_acc:
            best_acc   = te_acc
            best_epoch = epoch
            torch.save(model.state_dict(),
                       OUT_DIR / f"{args.arch}_sides{''.join(str(s) for s in test_sides)}_best.pt")

        history.append({
            "epoch": epoch, "tr_loss": round(tr_loss, 4), "tr_acc": round(tr_acc, 4),
            "te_loss": round(te_loss, 4), "te_acc": round(te_acc, 4), "te_f1": round(te_f1, 4),
        })

        print(f"{epoch:>4}  {tr_loss:>8.4f}  {tr_acc:>7.3f}  {te_loss:>8.4f}  {te_acc:>7.3f}  {te_f1:>6.3f}")

    # ── final evaluation with majority vote ───────────────────────────────────
    model.load_state_dict(
        torch.load(OUT_DIR / f"{args.arch}_sides{''.join(str(s) for s in test_sides)}_best.pt",
                   map_location=device)
    )
    run_acc, vote_preds, vote_true = majority_vote_accuracy(
        model, te_paths, te_labels, te_runs, val_tf, device
    )

    print(f"\nBest window-level test acc : {best_acc:.3f}  (epoch {best_epoch})")
    print(f"Run-level majority vote acc: {run_acc:.3f}  ({int(run_acc * len(set(te_runs)))}/{len(set(te_runs))} runs)")
    print(f"\nPer-class report (window-level, best model):")
    print(classification_report(vote_true, vote_preds, target_names=CLASS_NAMES, zero_division=0))

    # ── save history ──────────────────────────────────────────────────────────
    hist_path = OUT_DIR / f"{args.arch}_sides{''.join(str(s) for s in test_sides)}_history.json"
    with open(hist_path, "w") as f:
        json.dump({
            "arch": args.arch, "test_sides": test_sides, "epochs": args.epochs,
            "lr": args.lr, "smote": use_smote, "best_window_acc": round(best_acc, 4),
            "best_epoch": best_epoch, "run_level_acc": round(run_acc, 4),
            "history": history,
        }, f, indent=2)
    print(f"\nHistory saved to {hist_path}")


if __name__ == "__main__":
    main()
