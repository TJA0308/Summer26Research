"""
Leave-one-(DOC x speed)-condition-out CV for End Milling's 32x3/32x12
scalogram pipelines -- mirrors Shoulder Milling's cv_evaluate.py methodology,
adapted from its 8 leave-one-side-out folds to End Milling's 15 (DOC, speed)
condition groups (see build_residual_scalograms.py's docstring: exactly 15
groups of 3 runs each, one run per feed_coarse-adjacent point on the fine
6-class feed scale).

Why condition-residual correction doesn't transfer cleanly from Shoulder
Milling, and what "cond_*" models do about it
-----------------------------------------------------------------------
Shoulder Milling's design holds exactly one run per feed class at every
side, making feed conditionally independent of condition by construction --
subtracting the per-condition mean removes ONLY the condition's DC offset,
never the target's own signal (proven algebraically in
residual_preprocessing_readme.md). End Milling's design does not have this
property: feed_coarse is (empirically, checked directly against
cnn_train.py's label maps) almost a clean function of SPEED ALONE, identical
across all 3 DOC levels (e.g. speed=0 or 1 -> mostly class 0; speed=3 or 4 ->
mostly class 2). Roughness is a smooth, monotonic function of (DOC, speed)
jointly (DOC=0 is 100% one class; DOC=2 is 90%+ classes 1-2). In both cases
the "nuisance condition" is not independent of the target -- it's *causally
upstream* of it (feed scales with speed for chip-load reasons; roughness
scales with depth for cutting-mechanics reasons). Subtracting the per-
condition mean here removes real target signal along with the condition
offset, which is why residual_hgb's LOCO numbers don't consistently beat
plain hgb (see cv_summary.csv).

Quantifying this: majority-vote-by-condition alone (a per-condition lookup
table, ZERO vibration signal) gets 30/45=66.7% for feed_coarse and
38/45=84.4% for roughness -- because DOC and speed are KNOWN, CONTROLLED
machining parameters (you set them on the machine), not something that
needs to be inferred from vibration. Three additional model options exploit
this directly, evaluated under the same strict LOCO protocol (the held-out
condition is never seen during training, so the model must generalize the
speed/DOC -> target trend from the other 14 conditions, not memorize a
per-condition table):
  - "cond_only": HGB on the (DOC, speed) one-hot alone, NO image data --
    sanity-checks how much of the LOCO-honest ceiling condition alone
    achieves when the model must generalize the trend to an unseen
    condition (may fall short of the naive 66.7%/84.4% lookup ceiling,
    since that number assumes the condition is already in the lookup table).
  - "cond_hgb": condition one-hot CONCATENATED (after PCA, so the low-
    dimensional condition signal isn't diluted by ~100-400 pixel
    dimensions) with the raw-pixel PCA components -- lets HGB use both the
    condition trend AND whatever vibration signal helps disambiguate runs
    that are the minority class within their condition.
  - "cond_residual_hgb": same as cond_hgb, but pixels are condition-mean-
    subtracted first (per fold, unsupervised) before PCA -- combines the
    condition trend with the RESIDUAL (condition-signal-removed) vibration
    features, rather than raw pixels that still contain the (now redundant,
    since it's already in the one-hot) condition signal.

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
     - "cnn": the REAL big ImageNet-pretrained backbone (--arch, same
       choices as cnn_train_32x3.py: resnet18/resnet50/efficientnet_b0/
       convnext_tiny/mobilenet_v3_large), added because a 2026-08-12 check
       found hgb/tiny_cnn do NOT reach the standard-split ceiling
       ResNet-18/ConvNeXt-Tiny hit for speed (66.7%/40.0% vs the
       standard-split ResNet-18's 86.7%) and doc (83.3%/66.7% vs 100%) --
       unlike feed_coarse/roughness, where tiny_cnn ties the big backbones
       (see cv_summary.csv), so for speed/doc the cheap models understate
       what's achievable and can't be used to conclude whether the
       standard-split ceiling is real signal or a lucky split. Reuses
       cnn_train_32x3.py's build_model/build_transforms/ScalogramDataset/
       train_epoch verbatim (224x224 resize, ImageNet normalization,
       weighted CE, cosine LR schedule) -- same FIXED-epoch-count, no
       test-driven checkpoint selection discipline as tiny_cnn/run_kfold
       (see that function's "Fixed-epoch-count result" comment). This is
       the expensive option: 15 fresh ImageNet fine-tunes per --arch per
       --seed, likely CPU-infeasible for a full sweep -- run on a GPU
       machine, one target/arch/seed combination at a time.

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

    # Real-backbone LOCO check for speed/doc (GPU strongly recommended -- 15
    # fresh ResNet-18 fine-tunes at 50 epochs each; run one target at a time):
    python cv_evaluate_32x3.py --img_dir scalograms_32x3_speedopt_perdoc --target speed --models cnn --arch resnet18 --epochs 50
    python cv_evaluate_32x3.py --img_dir scalograms_32x3_docopt_raw3w --target doc --models cnn --arch resnet18 --epochs 50
    # Sanity-check against the known standard-split ceiling first (single fold, minutes not hours):
    python cv_evaluate_32x3.py --img_dir scalograms_32x3_speedopt_perdoc --target speed --split standard --models cnn --arch resnet18 --epochs 50
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

import cond_prior

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


# ── real ImageNet-pretrained backbone (resnet18/50, convnext_tiny, etc.) ──────
def train_backbone_cnn(train_paths, train_labels, num_classes, arch, dropout, epochs, batch, lr,
                        weight_decay, label_smooth, seed, device, mod):
    """Fine-tunes one of cnn_train_32x3.py's real backbones (224x224 resize +
    ImageNet normalization via mod.build_transforms/mod.ScalogramDataset,
    same architecture factory as the standard-split training that produced
    the 86.7%/100% speed/doc headline numbers). FIXED epoch count, no
    test-accuracy-driven checkpoint selection -- mirrors train_tiny_cnn's
    and run_kfold's anti-leakage discipline exactly; the only difference from
    those is architecture size and the ImageNet-pretrained starting point."""
    mod.seed_everything(seed)
    train_tf, val_tf = mod.build_transforms(noise_std=0.02)
    train_ds = mod.ScalogramDataset(train_paths, train_labels, train_tf)
    train_dl = DataLoader(train_ds, batch_size=min(batch, len(train_ds)), shuffle=True,
                           num_workers=0, drop_last=len(train_ds) > batch)

    model = mod.build_model(arch, num_classes, dropout=dropout).to(device)
    counts = np.bincount(train_labels, minlength=num_classes).astype(float)
    counts[counts == 0] = 1.0
    weights = torch.tensor(1.0 / counts, dtype=torch.float32).to(device)
    weights = weights / weights.sum()
    criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=label_smooth)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    for _ in range(epochs):
        mod.train_epoch(model, train_dl, criterion, optimizer, device)
        scheduler.step()
    return model, val_tf


@torch.no_grad()
def predict_backbone_cnn(model, val_tf, test_paths, device, mod):
    model.eval()
    ds = mod.ScalogramDataset(test_paths, [0] * len(test_paths), val_tf)
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


def predict_cond_stack(train_arrays, train_labels, train_conditions, test_arrays,
                        test_conditions, num_classes, seed, cond_weight=0.7, use_residual=True):
    """Probability-average of predict_cond_only and predict_hgb/residual_hgb,
    rather than flat feature concatenation (cond_hgb/cond_residual_hgb) --
    tried because concatenation let HGB's tree splits get distracted by noisy
    pixel PCA components, actively HURTING the otherwise-clean condition
    signal (see cv_summary.csv: cond_hgb/cond_residual_hgb score below
    cond_only alone, both targets). Averaging probabilities keeps the two
    signal sources from interfering with each other's decision boundaries."""
    cond_probs = predict_cond_only(train_labels, train_conditions, test_conditions, num_classes, seed)
    if use_residual:
        pixel_probs = predict_residual_hgb(train_arrays, train_labels, train_conditions,
                                            test_arrays, test_conditions, seed)
    else:
        pixel_probs = predict_hgb(train_arrays, train_labels, test_arrays, seed)
    return cond_prior.stack_probs(cond_probs, pixel_probs, cond_weight)


def predict_cond_only(train_labels, train_conditions, test_conditions, num_classes, seed):
    """Condition-only baseline: NO image data at all -- just the (DOC, speed)
    one-hot -> HGB. Quantifies how much of feed_coarse/roughness is already
    explained by the machining condition alone (a KNOWN, controlled
    parameter, not something that needs to be inferred from vibration) --
    see cv_evaluate_32x3.py's module docstring addendum on why this matters
    here specifically (unlike Shoulder Milling, where feed is independent of
    condition by design). Delegates to cond_prior.py (shared with
    stack_conditioning_32x3.py and cnn_train_32x3.py's main()), which also
    fixes a latent width bug: HGB.predict_proba only emits columns for
    classes present in this fold's train_labels, silently misaligning when
    averaged against a full-width pixel-model output under LOCO/imbalanced
    folds."""
    clf, classes_ = cond_prior.fit_condition_prior(train_conditions, train_labels, num_classes, seed)
    return cond_prior.predict_condition_prior(clf, classes_, test_conditions, num_classes)


def predict_cond_hgb(train_arrays, train_labels, train_conditions, test_arrays,
                      test_conditions, seed, use_residual):
    """Condition one-hot CONCATENATED (after PCA, not before -- PCA is fit on
    pixels only, so the low-dimensional condition signal doesn't get diluted
    among ~100-400 pixel dimensions) with the (optionally residual-corrected)
    pixel PCA components. Lets HGB use both: the strong condition->target
    trend (see predict_cond_only) AND whatever additional vibration-derived
    signal helps disambiguate the runs that are the minority class within
    their condition."""
    Xtr_raw = np.stack([a.reshape(-1) for a in train_arrays]).astype(np.float64)
    Xte_raw = np.stack([a.reshape(-1) for a in test_arrays]).astype(np.float64)
    if use_residual:
        Xtr_raw = _subtract_condition_means(Xtr_raw, train_conditions)
        Xte_raw = _subtract_condition_means(Xte_raw, test_conditions)

    n_components = min(20, Xtr_raw.shape[0] - 1)
    scaler = StandardScaler()
    Xtr_scaled = scaler.fit_transform(Xtr_raw)
    Xte_scaled = scaler.transform(Xte_raw)
    pca = PCA(n_components=n_components, random_state=seed)
    Xtr_pca = pca.fit_transform(Xtr_scaled)
    Xte_pca = pca.transform(Xte_scaled)

    Xtr = np.hstack([Xtr_pca, cond_prior.condition_onehot(train_conditions)])
    Xte = np.hstack([Xte_pca, cond_prior.condition_onehot(test_conditions)])

    clf = HistGradientBoostingClassifier(max_iter=150, random_state=seed)
    clf.fit(Xtr, train_labels)
    return clf.predict_proba(Xte)


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


def build_folds(split: str, label_map: dict, condition_of: dict, spec: dict, mod=None, kfold_k=5):
    """Returns a list of (train_runs, test_runs) partitions.
    'loco'       -- 15 folds, one per (DOC, speed) condition left out
                    (default) -- tests generalization to a condition NEVER
                    seen during training. The right question if production
                    machining parameters can differ from every condition
                    tested here.
    'standard'   -- ONE fixed fold, using this target's existing fixed
                    train/test split (TARGETS[target]['test_runs_standard']) --
                    the Shoulder-Milling-style single-split comparison point.
    'stratified' -- cnn_train.py's own stratified_kfold(): splits by CLASS,
                    not by condition, so a test run's condition typically
                    still appears (via its sibling runs) in the training
                    set. Tests a different, easier, and often more relevant
                    question: "can the model classify a new run from a
                    condition it has already characterized" -- appropriate
                    if production only ever revisits this same fixed set of
                    (DOC, speed) combinations rather than needing to
                    extrapolate to a brand new one."""
    if split == "stratified":
        return mod.stratified_kfold(label_map, kfold_k)
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
           lr: float, noise_std: float, device, mod, split: str, kfold_k: int = 5,
           cond_weight: float = 0.7, stack_use_residual: bool = True, arch: str = "resnet18",
           weight_decay: float = 1e-4, label_smooth: float = 0.05, dropout: float = None):
    spec = mod.TARGETS[target]
    label_map = spec["label_map"]
    num_classes = spec["num_classes"]

    entries = load_window_index(img_dir)
    if not entries:
        raise FileNotFoundError(f"No run*_w*.png files found in {img_dir}")

    condition_of = {run: (mod.DOC_LABELS[run], mod.SPEED_LABELS[run]) for run in label_map}
    folds = build_folds(split, label_map, condition_of, spec, mod, kfold_k)
    print(f"  split={split}  {len(folds)} fold(s), {len(label_map)} runs, "
          f"{len(entries)} window images")

    all_arrays = {}
    path_of = {}
    for run, window, p in entries:
        path_of[(run, window)] = p
        if model_name != "cnn":   # "cnn" reads full-res RGB straight off disk, doesn't need this
            all_arrays[(run, window)] = np.asarray(Image.open(p).convert("L"), dtype=np.float32)

    cnn_dropout = dropout if dropout is not None else mod.DEFAULT_DROPOUT[target]

    all_probs, all_labels, all_runs = [], [], []
    for fold_i, (train_runs, test_runs) in enumerate(folds, 1):
        train_entries = [(r, w) for r, w, _ in entries if r in train_runs]
        test_entries  = [(r, w) for r, w, _ in entries if r in test_runs]
        if not train_entries or not test_entries:
            print(f"  Skipping fold -- empty train or test partition")
            continue

        train_labels = np.array([label_map[r] for r, w in train_entries])
        test_labels  = np.array([label_map[r] for r, w in test_entries])
        train_conditions = [condition_of[r] for r, w in train_entries]
        test_conditions  = [condition_of[r] for r, w in test_entries]
        test_runs_list = [r for r, w in test_entries]

        if model_name == "cnn":
            if len(folds) > 1:
                print(f"  [cnn] fold {fold_i}/{len(folds)}  test_runs={sorted(test_runs)}")
            train_paths = [path_of[e] for e in train_entries]
            test_paths  = [path_of[e] for e in test_entries]
            model, val_tf = train_backbone_cnn(train_paths, train_labels, num_classes, arch,
                                                cnn_dropout, epochs, batch, lr, weight_decay,
                                                label_smooth, seed, device, mod)
            probs = predict_backbone_cnn(model, val_tf, test_paths, device, mod)
            all_probs.append(probs)
            all_labels.extend(test_labels.tolist())
            all_runs.extend(test_runs_list)
            continue

        train_arrays = [all_arrays[e] for e in train_entries]
        test_arrays  = [all_arrays[e] for e in test_entries]

        if model_name == "hgb":
            probs = predict_hgb(train_arrays, train_labels, test_arrays, seed)
        elif model_name == "residual_hgb":
            probs = predict_residual_hgb(train_arrays, train_labels, train_conditions,
                                          test_arrays, test_conditions, seed)
        elif model_name == "cond_only":
            probs = predict_cond_only(train_labels, train_conditions, test_conditions, num_classes, seed)
        elif model_name == "cond_hgb":
            probs = predict_cond_hgb(train_arrays, train_labels, train_conditions,
                                      test_arrays, test_conditions, seed, use_residual=False)
        elif model_name == "cond_residual_hgb":
            probs = predict_cond_hgb(train_arrays, train_labels, train_conditions,
                                      test_arrays, test_conditions, seed, use_residual=True)
        elif model_name == "cond_stack":
            probs = predict_cond_stack(train_arrays, train_labels, train_conditions,
                                        test_arrays, test_conditions, num_classes, seed,
                                        cond_weight=cond_weight, use_residual=stack_use_residual)
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
    parser.add_argument("--split", default="loco", choices=["loco", "standard", "stratified"],
                        help="'loco': 15-fold leave-one-condition-out (default) -- tests "
                             "generalization to an unseen condition. 'standard': one fixed "
                             "train/test split (this target's existing TEST_RUNS set). "
                             "'stratified': cnn_train.py's stratified_kfold -- splits by "
                             "class, a test run's condition usually still appears in "
                             "training via sibling runs (tests classifying a NEW RUN from "
                             "an ALREADY-SEEN condition, not an unseen one).")
    parser.add_argument("--kfold_k", type=int, default=5, help="'stratified' split only")
    parser.add_argument("--cond_weight", type=float, default=0.7,
                        help="cond_stack only: weight given to predict_cond_only's "
                             "probabilities vs the pixel model's (1-cond_weight)")
    parser.add_argument("--stack_pixel_model", default="residual_hgb",
                        choices=["hgb", "residual_hgb"],
                        help="cond_stack only: which pixel model to average with cond_only")
    parser.add_argument("--models", nargs="+", default=["hgb", "tiny_cnn"],
                        choices=["hgb", "tiny_cnn", "residual_hgb", "cond_only",
                                 "cond_hgb", "cond_residual_hgb", "cond_stack", "cnn"])
    parser.add_argument("--seeds", type=int, nargs="+", default=[42])
    parser.add_argument("--epochs", type=int, default=30,
                        help="tiny_cnn/cnn only. The standard-split headline numbers in "
                             "BEST_MODELS_README.md used 50 epochs -- pass --epochs 50 to match "
                             "that training recipe exactly when running --models cnn.")
    parser.add_argument("--batch", type=int, default=8, help="tiny_cnn/cnn only")
    parser.add_argument("--lr", type=float, default=1e-3, help="tiny_cnn/cnn only")
    parser.add_argument("--noise_std", type=float, default=0.02, help="tiny_cnn only")
    parser.add_argument("--arch", default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0",
                                 "convnext_tiny", "mobilenet_v3_large"],
                        help="cnn only -- which cnn_train_32x3.py backbone to fine-tune per fold")
    parser.add_argument("--weight_decay", type=float, default=1e-4, help="cnn only")
    parser.add_argument("--label_smooth", type=float, default=0.05, help="cnn only")
    parser.add_argument("--dropout", type=float, default=None,
                        help="cnn only. Default: cnn_train_32x3.py's per-target DEFAULT_DROPOUT "
                             "(matches the recipe used for the standard-split headline numbers)")
    args = parser.parse_args()

    img_dir = ROOT / args.img_dir
    if not img_dir.exists():
        raise FileNotFoundError(f"{img_dir} not found")

    mod = _load_cnn_train_32x3_module()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    split_desc = {"loco": "15-fold leave-one-condition-out",
                  "standard": "single fixed train/test split (no leave-one-out)",
                  "stratified": f"{args.kfold_k}-fold stratified-by-class (conditions overlap train/test)"}[args.split]
    print(f"Device: {device}   Scalogram: {img_dir.name}   Target: {args.target}   {split_desc}")

    rows = []
    for model_name in args.models:
        if model_name == "cnn":
            print(f"  [cnn] arch={args.arch}  epochs={args.epochs}  batch={args.batch}  "
                  f"lr={args.lr}  -- one fresh fine-tune per fold, this is slow, "
                  f"see module docstring")
        for seed in args.seeds:
            window_acc, run_hard, run_soft, n_runs = run_cv(
                img_dir, args.target, model_name, seed, args.epochs, args.batch, args.lr,
                args.noise_std, device, mod, args.split, args.kfold_k,
                args.cond_weight, args.stack_pixel_model == "residual_hgb",
                args.arch, args.weight_decay, args.label_smooth, args.dropout,
            )
            print(f"  {model_name:14s} seed={seed:<4d} window_acc={window_acc:.3f}  "
                  f"run_acc_hard={run_hard:.3f}  run_acc_soft={run_soft:.3f}  "
                  f"(pooled over {n_runs} runs)")
            rows.append({
                "target": args.target, "img_dir": img_dir.name, "model": model_name,
                "arch": args.arch if model_name == "cnn" else "",
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
        if "arch" not in prev.columns:
            prev["arch"] = ""        # all pre-existing rows predate --models cnn
        out = pd.concat([prev, out], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"\nWrote {len(rows)} rows -> {out_path.name}")

    print("\n--- Mean +/- std across seeds ---")
    group_cols = ["target", "img_dir", "model", "split"] + (["arch"] if "arch" in out.columns else [])
    for key, g in out.groupby(group_cols):
        tag = "  ".join(str(k) for k in (key if isinstance(key, tuple) else (key,)))
        print(f"  {tag:<70s} n={len(g)}  "
              f"window={g['window_acc'].mean():.3f}+/-{g['window_acc'].std():.3f}  "
              f"run_hard={g['run_acc_hard'].mean():.3f}+/-{g['run_acc_hard'].std():.3f}  "
              f"run_soft={g['run_acc_soft'].mean():.3f}+/-{g['run_acc_soft'].std():.3f}")


if __name__ == "__main__":
    main()
