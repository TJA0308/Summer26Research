"""
Leave-one-(DOC x speed)-condition-out CV for End Milling's 32x3/32x12
scalogram pipelines -- mirrors Shoulder Milling's cv_evaluate.py methodology,
adapted from its 8 leave-one-side-out folds to End Milling's 15 (DOC, speed)
condition groups (see build_residual_scalograms.py's docstring: exactly 15
groups of 3 runs each, one run per feed_coarse-adjacent point on the fine
6-class feed scale).

Why this exists instead of just using cnn_train_32x3.py's --kfold
------------------------------------------------------------------
1. cnn_train_32x3.py's checkpoint selection used to be test-accuracy-driven
   (`if te_acc > best_acc: save`, in both its main() path and --kfold's
   run_kfold()) -- exactly the leakage mechanism Shoulder Milling's
   residual_preprocessing_readme.md flags as bias source #2 behind their
   now-debunked feed numbers (fixed in this same session -- both paths now
   just take the final-epoch checkpoint, no test-driven comparison). But
   even with that fixed, --kfold's stratified_kfold() splits by CLASS
   LABEL, not by condition -- a test run can share its (DOC, speed)
   condition with several training runs, so the model can still learn to
   recognise the *condition* and shortcut to whatever class is common
   there, same failure mode Shoulder Milling diagnosed.
2. Retraining the big ImageNet-pretrained backbones 15x per config (once
   per left-out condition) is slow and prone to overfitting on ~42-run
   folds. Shoulder Milling used two cheap, fast-to-retrain alternatives
   instead, both used here:
     - "hgb": StandardScaler -> PCA(20) -> HistGradientBoostingClassifier
       on raw native-resolution pixels (no resize, no ImageNet
       normalization) -- window-level samples, run-level vote pooling
       applied after.
     - "tiny_cnn": ~40K-param from-scratch CNN (2 conv blocks + global avg
       pool), trained for a FIXED epoch count per fold -- no early
       stopping / checkpoint comparison against test accuracy at all.
     - "residual_hgb": same as hgb, but subtracts each condition's mean
       BEFORE classifying -- computed PER FOLD from training-fold windows
       only (grouped by the other 14 conditions present in training); the
       held-out fold's own mean is estimated unsupervised from its own
       windows, no labels used. This is the leakage-free version of
       build_residual_scalograms.py's global (pre-built) residual, which
       has a small documented self-leakage (~1/9, each image contributes
       to its own group mean) that's acceptable for the pre-built training
       directories but not for this CV number.

Grouping: each of End Milling's 15 (DOC, speed) condition groups has exactly
3 runs. Leaving one group out yields a held-out fold containing 3 whole
runs' worth of windows (9 or 27 window images depending on --n_windows),
none of which appear in any form during that fold's training -- true
run-and-condition-level holdout, not just held-out windows of a run whose
sibling windows are in the training set.

Caveat (documented, matching Shoulder Milling's own caveat in cv_evaluate.py,
not silently ignored): if --img_dir is a *opt/_raw*w variant, its top-32
CWT scale-row selection was fit ONCE on all 45 runs upstream, in
build_32x3_features.py / build_rawwindow_features.py's select_cwt_rows().
This is cross-validation of the CLASSIFIER stage only, not a fully
leakage-free end-to-end pipeline -- re-running scale selection per fold
from raw signal data would be a larger follow-up, not attempted here.

Usage:
    python cv_evaluate_32x3.py --img_dir scalograms_32x3_feedopt_residual --target feed_coarse
    python cv_evaluate_32x3.py --img_dir scalograms_32x3_residual_roughness --target roughness --models hgb tiny_cnn residual_hgb
    python cv_evaluate_32x3.py --img_dir scalograms_32x3 --target speed --models hgb
"""
import argparse
import importlib.util
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

ROOT = Path(__file__).parent


def _load_cnn_train_32x3_module():
    spec = importlib.util.spec_from_file_location(
        "cnn_train_32x3", ROOT / "cnn_model" / "cnn_train_32x3.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── native-resolution dataset (no resize, no ImageNet normalization) ───────────
class NativeScalogramDataset(Dataset):
    def __init__(self, arrays, labels, transform):
        self.arrays, self.labels, self.transform = arrays, labels, transform

    def __len__(self):
        return len(self.arrays)

    def __getitem__(self, idx):
        img = Image.fromarray(self.arrays[idx])
        return self.transform(img), self.labels[idx]


def native_transforms(noise_std, add_noise_cls):
    train_tf = transforms.Compose([
        transforms.ToTensor(), add_noise_cls(noise_std), transforms.Normalize([0.5], [0.5]),
    ])
    val_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])
    return train_tf, val_tf


# ── tiny from-scratch CNN (same design as Shoulder Milling's cv_evaluate.py) ──
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


def train_tiny_cnn(train_arrays, train_labels, num_classes, epochs, batch, lr, noise_std,
                    seed, device, seed_fn, add_noise_cls):
    seed_fn(seed)
    train_tf, val_tf = native_transforms(noise_std, add_noise_cls)
    ds = NativeScalogramDataset(train_arrays, train_labels, train_tf)
    dl = DataLoader(ds, batch_size=min(batch, len(ds)), shuffle=True, num_workers=0,
                     drop_last=len(ds) > batch)

    model = TinyCNN(num_classes).to(device)
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
def predict_tiny_cnn(model, val_tf, arrays, device):
    model.eval()
    ds = NativeScalogramDataset(arrays, [0] * len(arrays), val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    probs = []
    for imgs, _ in dl:
        probs.extend(torch.softmax(model(imgs.to(device)), dim=1).cpu().numpy())
    return np.array(probs)


# ── HGB (native pixels -> PCA -> HistGradientBoosting) ─────────────────────────
def predict_hgb(train_arrays, train_labels, test_arrays, seed):
    Xtr = np.stack([a.reshape(-1) for a in train_arrays]).astype(np.float64)
    Xte = np.stack([a.reshape(-1) for a in test_arrays]).astype(np.float64)
    n_components = min(20, Xtr.shape[0] - 1)
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=n_components, random_state=seed)),
        ("clf", HistGradientBoostingClassifier(max_iter=150, random_state=seed)),
    ])
    pipe.fit(Xtr, train_labels)
    return pipe.predict_proba(Xte)


def _subtract_condition_means(arrays_raw, conditions):
    """Groups rows of arrays_raw by `conditions` (one entry per row) and
    subtracts each group's own mean -- unsupervised, no labels used. Works
    identically whether given a training partition (many conditions) or a
    single held-out LOCO fold (one repeated condition) or a fixed test split
    (however many distinct conditions happen to appear in it)."""
    out = np.empty_like(arrays_raw)
    for cond in set(conditions):
        mask = np.array([c == cond for c in conditions])
        out[mask] = arrays_raw[mask] - arrays_raw[mask].mean(axis=0)
    return out


def predict_residual_hgb(train_arrays, train_labels, train_conditions, test_arrays,
                          test_conditions, seed):
    """Condition-prototype subtraction HGB, computed PER FOLD/SPLIT (see
    module docstring). Both train and test windows have their own
    condition's mean subtracted, using only windows visible within that same
    partition -- unsupervised, no labels used, no cross-partition leakage."""
    Xtr_raw = np.stack([a.reshape(-1) for a in train_arrays]).astype(np.float64)
    Xte_raw = np.stack([a.reshape(-1) for a in test_arrays]).astype(np.float64)

    Xtr = _subtract_condition_means(Xtr_raw, train_conditions)
    Xte = _subtract_condition_means(Xte_raw, test_conditions)

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


def load_window_index(img_dir: Path):
    """Glob real run{N}_w{K}.png files (excludes smote*/synthetic samples --
    those don't start with 'run'). Returns list of (run, window, path)."""
    entries = []
    for p in sorted(img_dir.glob("run*_w*.png")):
        run = p.stem.split("_w")[0]
        window = int(p.stem.split("_w")[1])
        entries.append((run, window, p))
    return entries


def build_folds(split: str, label_map: dict, condition_of: dict, spec: dict):
    """Returns a list of (train_runs, test_runs) partitions.
    'loco'     -- 15 folds, one per (DOC, speed) condition left out (default,
                  what the module docstring's methodology is built around).
    'standard' -- ONE fixed fold, using this target's existing fixed
                  train/test split (TARGETS[target]['test_runs_standard'],
                  the same split cnn_train_32x3.py's non-kfold path uses) --
                  the Shoulder-Milling-style single-split comparison point,
                  analogous to baseline_classical.py's fixed split rather
                  than cv_evaluate.py's leave-one-side-out CV."""
    if split == "loco":
        conditions = sorted(set(condition_of.values()))
        return [
            (set(label_map.keys()) - {r for r, c in condition_of.items() if c == cond},
             {r for r, c in condition_of.items() if c == cond})
            for cond in conditions
        ]
    if split == "standard":
        test_runs = set(spec["test_runs_standard"]) & set(label_map.keys())
        train_runs = set(label_map.keys()) - test_runs
        return [(train_runs, test_runs)]
    raise ValueError(split)


def run_cv(img_dir: Path, target: str, model_name: str, seed: int, epochs: int, batch: int,
           lr: float, noise_std: float, device, mod, split: str):
    spec = mod.TARGETS[target]
    label_map = spec["label_map"]
    num_classes = spec["num_classes"]

    entries = load_window_index(img_dir)
    if not entries:
        raise FileNotFoundError(f"No run*_w*.png files found in {img_dir}")

    condition_of = {run: (mod.DOC_LABELS[run], mod.SPEED_LABELS[run]) for run in label_map}
    folds = build_folds(split, label_map, condition_of, spec)
    print(f"  split={split}  {len(folds)} fold(s), {len(label_map)} runs, "
          f"{len(entries)} window images")

    all_arrays = {}
    for run, window, p in entries:
        all_arrays[(run, window)] = np.asarray(Image.open(p).convert("L"), dtype=np.float32)

    all_probs, all_labels, all_runs = [], [], []
    for train_runs, test_runs in folds:
        train_entries = [(r, w) for r, w, _ in entries if r in train_runs]
        test_entries  = [(r, w) for r, w, _ in entries if r in test_runs]
        if not train_entries or not test_entries:
            print(f"  Skipping fold -- empty train or test partition")
            continue

        train_arrays = [all_arrays[e] for e in train_entries]
        test_arrays  = [all_arrays[e] for e in test_entries]
        train_labels = np.array([label_map[r] for r, w in train_entries])
        test_labels  = np.array([label_map[r] for r, w in test_entries])
        train_conditions = [condition_of[r] for r, w in train_entries]
        test_conditions  = [condition_of[r] for r, w in test_entries]
        test_runs_list = [r for r, w in test_entries]

        if model_name == "hgb":
            probs = predict_hgb(train_arrays, train_labels, test_arrays, seed)
        elif model_name == "residual_hgb":
            probs = predict_residual_hgb(train_arrays, train_labels, train_conditions,
                                          test_arrays, test_conditions, seed)
        elif model_name == "tiny_cnn":
            model, val_tf = train_tiny_cnn(train_arrays, train_labels, num_classes, epochs, batch,
                                            lr, noise_std, seed, device, mod.seed_everything,
                                            mod.AddGaussianNoise)
            probs = predict_tiny_cnn(model, val_tf, test_arrays, device)
        else:
            raise ValueError(model_name)

        all_probs.append(probs)
        all_labels.extend(test_labels.tolist())
        all_runs.extend(test_runs_list)

    all_probs = np.concatenate(all_probs, axis=0)
    all_labels = np.array(all_labels)
    window_acc, run_hard, run_soft = vote(all_probs, all_labels, all_runs)
    return window_acc, run_hard, run_soft, len(set(all_runs))


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--img_dir", required=True)
    parser.add_argument("--target", required=True,
                        choices=["speed", "doc", "feed_coarse", "roughness"])
    parser.add_argument("--split", default="loco", choices=["loco", "standard"],
                        help="'loco': 15-fold leave-one-condition-out (default). "
                             "'standard': one fixed train/test split (this target's "
                             "existing TEST_RUNS set), for comparison against the "
                             "fixed-split CNN sweep numbers -- no leave-one-out.")
    parser.add_argument("--models", nargs="+", default=["hgb", "tiny_cnn"],
                        choices=["hgb", "tiny_cnn", "residual_hgb"])
    parser.add_argument("--seeds", type=int, nargs="+", default=[42])
    parser.add_argument("--epochs", type=int, default=30, help="tiny_cnn only")
    parser.add_argument("--batch", type=int, default=8, help="tiny_cnn only")
    parser.add_argument("--lr", type=float, default=1e-3, help="tiny_cnn only")
    parser.add_argument("--noise_std", type=float, default=0.02, help="tiny_cnn only")
    args = parser.parse_args()

    img_dir = ROOT / args.img_dir
    if not img_dir.exists():
        raise FileNotFoundError(f"{img_dir} not found")

    mod = _load_cnn_train_32x3_module()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    split_desc = "15-fold leave-one-condition-out" if args.split == "loco" else \
                 "single fixed train/test split (no leave-one-out)"
    print(f"Device: {device}   Scalogram: {img_dir.name}   Target: {args.target}   {split_desc}")

    rows = []
    for model_name in args.models:
        for seed in args.seeds:
            window_acc, run_hard, run_soft, n_runs = run_cv(
                img_dir, args.target, model_name, seed, args.epochs, args.batch, args.lr,
                args.noise_std, device, mod, args.split,
            )
            print(f"  {model_name:14s} seed={seed:<4d} window_acc={window_acc:.3f}  "
                  f"run_acc_hard={run_hard:.3f}  run_acc_soft={run_soft:.3f}  "
                  f"(pooled over {n_runs} runs)")
            rows.append({
                "target": args.target, "img_dir": img_dir.name, "model": model_name,
                "split": args.split, "seed": seed, "window_acc": round(window_acc, 4),
                "run_acc_hard": round(run_hard, 4), "run_acc_soft": round(run_soft, 4),
                "n_runs": n_runs,
            })

    out = pd.DataFrame(rows)
    out_path = ROOT / "cv_summary.csv"
    if out_path.exists():
        prev = pd.read_csv(out_path)
        if "split" not in prev.columns:
            prev["split"] = "loco"   # all pre-existing rows predate --split, were LOCO-only
        out = pd.concat([prev, out], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"\nWrote {len(rows)} rows -> {out_path.name}")

    print("\n--- Mean +/- std across seeds ---")
    for (target, img_name, model, split), g in out.groupby(["target", "img_dir", "model", "split"]):
        print(f"  {target:<12s} {img_name:<40s} {model:<14s} {split:<10s} n={len(g)}  "
              f"window={g['window_acc'].mean():.3f}+/-{g['window_acc'].std():.3f}  "
              f"run_hard={g['run_acc_hard'].mean():.3f}+/-{g['run_acc_hard'].std():.3f}  "
              f"run_soft={g['run_acc_soft'].mean():.3f}+/-{g['run_acc_soft'].std():.3f}")


if __name__ == "__main__":
    main()
