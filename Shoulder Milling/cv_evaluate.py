"""
Leave-one-side-out (8-fold) cross-validation for the feed target -- the
highest-leverage structural change identified after reviewing the project's
existing results (baseline_classical_summary.csv, experiments_writeup.md,
pca_readme.md). Every headline feed number so far rests on ONE fixed 8-run
test split (12.5pp granularity per run), and best-of-8-arch/lr configs get
picked ON that same test set (pure selection bias) -- exactly how the
now-debunked 87.5% figure happened. Pooling predictions across all 8
leave-one-side-out folds instead gives one run-accuracy estimate over all 24
runs (4.2pp granularity), with no test-set-driven model/checkpoint selection.

"Side" (labels.csv column, 1-8) is the natural fold unit: each side has
exactly one run per feed class (f3/f5/f7), so leaving one side out yields a
perfectly class-balanced 3-run test fold every time -- no class weighting
needed.

Two candidate models, both at NATIVE scalogram resolution (no 224x224
upsample, no ImageNet pretraining -- baseline_classical.py already showed
PCA+HGB on raw pixels ties the ImageNet-backbone CNNs' feed ceiling, and
pca_readme.md Phase B planned but never built a small from-scratch CNN):
  - "hgb":      StandardScaler + PCA(20) + HistGradientBoostingClassifier,
                the same recipe as baseline_classical.py's best feed model.
  - "tiny_cnn": ~40K-param from-scratch CNN (2 conv blocks + global average
                pool), trained fresh per fold for a FIXED epoch count (no
                test-set-driven checkpoint selection, unlike
                cnn_train_param.py's `if te_acc > best_acc: save` -- that
                pattern is itself a mild form of the same test-set leakage
                this script exists to avoid).

Caveat (documented, not silently ignored): the feedopt scale-row selection
baked into scalograms_*_feedopt/*.png was fit ONCE on all 24 runs upstream
of this script, in build_option_d_scalograms.py's select_cwt_rows(). This is
cross-validation of the CLASSIFIER stage only, not a fully leakage-free
end-to-end pipeline. A fully clean version would re-run scale selection per
fold from raw signal data in data/Side*.xlsx -- a larger follow-up, not
attempted here.

Usage:
    python cv_evaluate.py --img_dir scalograms_32x3_feedopt
    python cv_evaluate.py --img_dir scalograms_32x3_feedopt --models hgb tiny_cnn --seeds 42 43 44
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from cnn_train_param import AddGaussianNoise, FEED_TO_CLASS, TARGETS, seed_everything

ROOT = Path(__file__).parent
FEED_CLASSES = TARGETS["feed"]["num_classes"]


# ── native-resolution dataset (no resize, no ImageNet normalization) ───────────
class NativeScalogramDataset(Dataset):
    def __init__(self, paths, labels, transform):
        self.paths, self.labels, self.transform = paths, labels, transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("L")   # single grayscale channel
        return self.transform(img), self.labels[idx]


def native_transforms(noise_std=0.02):
    train_tf = transforms.Compose([
        transforms.ToTensor(), AddGaussianNoise(noise_std), transforms.Normalize([0.5], [0.5]),
    ])
    val_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])
    return train_tf, val_tf


# ── tiny from-scratch CNN ───────────────────────────────────────────────────────
class TinyCNN(nn.Module):
    """~40K params. No pretraining, no resize -- operates at whatever native
    H x W the scalogram PNGs already are (e.g. 32x3 or 32x12)."""
    def __init__(self, num_classes, dropout=0.2):
        super().__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(1, 16, 3, padding=1), nn.BatchNorm2d(16), nn.ReLU())
        self.conv2 = nn.Sequential(nn.Conv2d(16, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU())
        self.pool  = nn.AdaptiveAvgPool2d(1)
        self.head  = nn.Sequential(nn.Dropout(dropout), nn.Linear(32, num_classes))

    def forward(self, x):
        x = self.conv2(self.conv1(x))
        x = self.pool(x).flatten(1)
        return self.head(x)


def train_tiny_cnn(train_paths, train_labels, epochs, batch, lr, noise_std, seed, device):
    seed_everything(seed)
    train_tf, val_tf = native_transforms(noise_std)
    ds = NativeScalogramDataset(train_paths, train_labels, train_tf)
    dl = DataLoader(ds, batch_size=min(batch, len(ds)), shuffle=True, num_workers=0,
                     drop_last=len(ds) > batch)

    model = TinyCNN(FEED_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    model.train()
    for _ in range(epochs):
        for imgs, labels in dl:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = criterion(model(imgs), labels)
            loss.backward()
            optimizer.step()
        scheduler.step()
    return model, val_tf


@torch.no_grad()
def predict_tiny_cnn(model, val_tf, paths, device):
    model.eval()
    ds = NativeScalogramDataset(paths, [0] * len(paths), val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    probs = []
    for imgs, _ in dl:
        probs.extend(torch.softmax(model(imgs.to(device)), dim=1).cpu().numpy())
    return np.array(probs)


# ── HGB (native pixels -> PCA -> HistGradientBoosting) ─────────────────────────
def load_pixels(paths):
    return np.stack([np.asarray(Image.open(p).convert("L"), dtype=np.float32).ravel() for p in paths])


def predict_hgb(train_paths, train_labels, test_paths, seed):
    Xtr, Xte = load_pixels(train_paths), load_pixels(test_paths)
    n_components = min(20, Xtr.shape[0] - 1)
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=n_components, random_state=seed)),
        ("clf", HistGradientBoostingClassifier(max_iter=150, random_state=seed)),
    ])
    pipe.fit(Xtr, train_labels)
    return pipe.predict_proba(Xte)


# ── voting + fold loop ──────────────────────────────────────────────────────────
def vote(probs, labels, run_ids):
    """Returns (window_acc, run_acc_hard, run_acc_soft) from per-window softmax probs."""
    preds = probs.argmax(axis=1)
    window_acc = float((preds == labels).mean())

    run_probs, run_hard, run_true = {}, {}, {}
    for p, prob, true, run in zip(preds, probs, labels, run_ids):
        run_probs.setdefault(run, []).append(prob)
        run_hard.setdefault(run, []).append(int(p))
        run_true[run] = true

    hard_correct = sum(
        int(max(set(run_hard[r]), key=run_hard[r].count) == run_true[r]) for r in run_true
    )
    soft_correct = sum(
        int(int(np.argmax(np.mean(run_probs[r], axis=0))) == run_true[r]) for r in run_true
    )
    n = len(run_true)
    return window_acc, hard_correct / n, soft_correct / n


def run_cv(img_dir: Path, model_name: str, seed: int, epochs: int, batch: int, lr: float,
           noise_std: float, device):
    df = pd.read_csv(img_dir / "labels.csv")
    df["label"] = df["feed"].map(FEED_TO_CLASS)
    sides = sorted(df["side"].unique())

    all_probs, all_labels, all_runs = [], [], []
    for side in sides:
        test_df  = df[df["side"] == side].reset_index(drop=True)
        train_df = df[df["side"] != side].reset_index(drop=True)
        train_paths = [img_dir / fn for fn in train_df["filename"]]
        test_paths  = [img_dir / fn for fn in test_df["filename"]]
        train_labels = train_df["label"].to_numpy()
        test_labels  = test_df["label"].to_numpy()
        test_runs    = test_df["run_id"].tolist()

        if model_name == "hgb":
            probs = predict_hgb(train_paths, train_labels, test_paths, seed)
        elif model_name == "tiny_cnn":
            model, val_tf = train_tiny_cnn(train_paths, train_labels, epochs, batch, lr,
                                            noise_std, seed, device)
            probs = predict_tiny_cnn(model, val_tf, test_paths, device)
        else:
            raise ValueError(model_name)

        all_probs.append(probs)
        all_labels.extend(test_labels.tolist())
        all_runs.extend(test_runs)

    all_probs = np.concatenate(all_probs, axis=0)
    all_labels = np.array(all_labels)
    window_acc, run_hard, run_soft = vote(all_probs, all_labels, all_runs)
    return window_acc, run_hard, run_soft, len(set(all_runs))


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--img_dir", default="scalograms_32x3_feedopt")
    parser.add_argument("--models", nargs="+", default=["hgb", "tiny_cnn"],
                        choices=["hgb", "tiny_cnn"])
    parser.add_argument("--seeds", type=int, nargs="+", default=[42])
    parser.add_argument("--epochs", type=int, default=30, help="tiny_cnn only")
    parser.add_argument("--batch", type=int, default=8, help="tiny_cnn only")
    parser.add_argument("--lr", type=float, default=1e-3, help="tiny_cnn only")
    parser.add_argument("--noise_std", type=float, default=0.02, help="tiny_cnn only")
    args = parser.parse_args()

    img_dir = ROOT / args.img_dir
    device  = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}   Scalogram: {img_dir.name}   8-fold leave-one-side-out")

    rows = []
    for model_name in args.models:
        for seed in args.seeds:
            window_acc, run_hard, run_soft, n_runs = run_cv(
                img_dir, model_name, seed, args.epochs, args.batch, args.lr,
                args.noise_std, device,
            )
            print(f"  {model_name:10s} seed={seed:<4d} window_acc={window_acc:.3f}  "
                  f"run_acc_hard={run_hard:.3f}  run_acc_soft={run_soft:.3f}  "
                  f"(pooled over {n_runs} runs)")
            rows.append({
                "scalogram": img_dir.name.replace("scalograms_", ""), "model": model_name,
                "seed": seed, "window_acc": round(window_acc, 4),
                "run_acc_hard": round(run_hard, 4), "run_acc_soft": round(run_soft, 4),
                "n_runs": n_runs,
            })

    out = pd.DataFrame(rows)
    out_path = ROOT / "cv_summary.csv"
    if out_path.exists():
        out = pd.concat([pd.read_csv(out_path), out], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"\nWrote {len(rows)} rows -> {out_path.name}")

    print("\n--- Mean +/- std across seeds ---")
    for (scalo, model), g in out.groupby(["scalogram", "model"]):
        print(f"  {scalo:<20s} {model:<10s} n={len(g)}  "
              f"window={g['window_acc'].mean():.3f}+/-{g['window_acc'].std():.3f}  "
              f"run_hard={g['run_acc_hard'].mean():.3f}+/-{g['run_acc_hard'].std():.3f}  "
              f"run_soft={g['run_acc_soft'].mean():.3f}+/-{g['run_acc_soft'].std():.3f}")


if __name__ == "__main__":
    main()
