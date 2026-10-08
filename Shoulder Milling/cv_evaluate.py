"""
Leave-one-condition-out (LOCO) cross-validation for Shoulder Milling, for
ALL FOUR targets (speed, feed, doc, roughness), with an option to fine-tune
the REAL ImageNet-pretrained backbones from cnn_train_param.py fresh per
fold (--models cnn), not just the cheap hgb/tiny_cnn surrogates.

Every fold's grouping holds out whichever OTHER designed factors aren't the
current target, so the target is (as far as the experimental design can
guarantee) the only thing varying within a held-out fold:
  - feed:      group by (speed, doc) = side  -> 8 folds, 3 runs/fold
  - speed:     group by doc                  -> 4 folds, 6 runs/fold
  - doc:       group by (speed, feed)        -> 6 folds, 4 runs/fold
  - roughness: group by doc (PRIMARY, default) -> 4 folds, 6 runs/fold
               group by (speed, feed) (--roughness_group secondary) -> 6 folds

roughness is NOT a designed factor (it's derived from measured Ra), so unlike
the other three targets it is NOT guaranteed independent of any grouping --
and empirically it isn't: Ra is strongly doc-driven, so grouping by
(speed, feed) leaves doc fully visible in training while varying inside the
held-out fold, letting a zero-vibration doc-lookup alone score ~62.5% run
accuracy (measured 2026-09-21, see run_selftest() below and
project_shoulder_milling.md in ml-strategy-optimizer's agent memory). Grouping
by doc instead (the default here) closes that hole -- verified below at 25%,
i.e. the doc lookup is USELESS once doc itself is held out. Every roughness
LOCO number printed by this script is accompanied by its nuisance-lookup
floor for exactly this reason -- never compare a roughness LOCO number to
raw 50% chance.

Every other target's grouping was verified empirically (not just assumed) to
sit at exact chance for a zero-image nuisance-lookup baseline: feed 8/24
(33.3%), speed 12/24 (50.0%), doc 6/24 (25.0%). Run `--selftest` to
recompute these yourself (fast, labels.csv only, no training/image loading) --
any future change to the grouping logic that reintroduces a confound will
show up there as a baseline above chance.

Anti-leakage discipline (all enforced by construction, not by removing rows
after the fact):
  - No test-accuracy-driven checkpoint selection. The `cnn` path trains a
    FIXED epoch count and evaluates the FINAL-epoch model only, matching the
    fix applied to cnn_train_param.py in the same session that added this
    script's --target/--models cnn options (that file used to save/report
    whichever epoch had the highest TEST accuracy -- the same mechanism
    behind the now-debunked 87.5% feed number).
  - No SMOTE. This script reads ONLY img_dir/labels.csv, never
    smote_<target>_labels.csv -- synthetic samples are interpolated from the
    FIXED standard split's train partition, so under LOCO some source runs
    would land in the test fold (direct leakage). Real windows only.
  - No cascade conditioning. This script never calls load_conditioning() /
    builds a ConditionedModel -- the <parent>_pred_<scalo>.csv files cascade
    conditioning would read were produced by FIXED-split models that saw
    every LOCO test fold's runs during their own training. LOCO here is
    always the plain, unconditioned model.
  - Headline metric is SOFT vote (run_acc_soft, mean-probability), not hard
    majority vote. With 3 windows/run, hard voting on doc (4 classes) ties
    constantly and set-iteration-order breaks ties in a way that's not a
    real signal. run_acc_hard is still reported for reference, never as the
    number to act on.
  - Reported CI is an exact Clopper-Pearson interval over the POOLED runs
    (24 total either way), not a per-fold std -- there is no unbiased
    estimator of k-fold CV variance (Bengio & Grandvalet, JMLR 2004), and
    per-fold accuracy is uninterpretable at 2-6 runs/fold. Treat this CI as
    an approximate, honestly-labeled headline, not a precise guarantee.

Caveat (documented, matching this project's other CV scripts, not silently
ignored): if --img_dir is a *feedopt/*opt* variant, its CWT scale-row
selection (build_option_d_scalograms.py's select_cwt_rows()) was fit ONCE on
ALL runs upstream of the classifier stage. This is cross-validation of the
CLASSIFIER stage only, not a fully leakage-free end-to-end pipeline.

Usage:
    # Fast plumbing check, all 4 targets, seconds:
    python cv_evaluate.py --img_dir scalograms_32x3_feedopt --target feed   --models hgb
    python cv_evaluate.py --img_dir scalograms_32x12        --target speed --models hgb
    python cv_evaluate.py --img_dir scalograms_32x12        --target doc   --models hgb
    python cv_evaluate.py --img_dir scalograms_32x12        --target roughness --models hgb

    # Mandatory pre-flight: does the reimplemented pipeline reproduce the
    # (corrected, final-epoch) standard-split number? Single fold, minutes:
    python cv_evaluate.py --img_dir scalograms_32x12 --target speed --split standard --models cnn --arch resnet18 --epochs 50

    # Real-backbone LOCO (GPU strongly recommended -- see module docstring
    # and project_shoulder_milling.md for CPU wall-time estimates per target):
    python cv_evaluate.py --img_dir scalograms_32x12 --target speed     --models cnn --arch resnet18 --epochs 50
    python cv_evaluate.py --img_dir scalograms_32x12 --target roughness --models cnn --arch resnet18 --epochs 50
    python cv_evaluate.py --img_dir scalograms_32x12 --target roughness --models cnn --arch resnet18 --epochs 50 --roughness_group secondary

    # Verify the grouping-independence assumption (fast, no training):
    python cv_evaluate.py --selftest
"""
import argparse
import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from PIL import Image
from scipy.stats import beta
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from cnn_train_param import (
    AddGaussianNoise, FEED_TO_CLASS, TARGETS, COND_FROM_SIDE_FEED, SIDE_TO_SPEED, SIDE_TO_DOC,
    DEFAULT_DROPOUT, label_for, seed_everything, build_model, build_transforms,
    train_epoch,
)
from cnn_train_param import ScalogramDataset as _PathScalogramDataset

ROOT = Path(__file__).parent


def _open_img(x):
    """Path/str -> PIL image read from disk (original behaviour). A PIL image
    is passed through; a float ndarray (assumed in [0,1]) or uint8 ndarray is
    converted to a PIL image. Lets --preproc feed in-memory images.
    CONTRACT: nested_preproc transform() returns uint8 PIL 'L' images (run_cv
    rejects anything else); the float-[0,1] branch must never see signed data,
    since clip(.,0,1) would destroy it."""
    if isinstance(x, (str, Path)):
        return Image.open(x)
    if isinstance(x, Image.Image):
        return x
    a = np.asarray(x)
    if a.dtype != np.uint8:
        a = (np.clip(a, 0.0, 1.0) * 255.0).round().astype(np.uint8)
    return Image.fromarray(a)


class ScalogramDataset(_PathScalogramDataset):
    """cnn_train_param.ScalogramDataset, but items may be paths OR in-memory images."""
    def __getitem__(self, idx):
        img = _open_img(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]


FEED_CLASSES = TARGETS["feed"]["num_classes"]


# ── LOCO fold-grouping configs (see module docstring for the independence
#    verification behind each choice) ────────────────────────────────────────
def _feed_group(side, feed):
    return (SIDE_TO_SPEED[side], SIDE_TO_DOC[side])


def _speed_group(side, feed):
    return (SIDE_TO_DOC[side],)


def _doc_group(side, feed):
    return (SIDE_TO_SPEED[side], feed)


def _roughness_group_primary(side, feed):
    return (SIDE_TO_DOC[side],)


def _roughness_group_secondary(side, feed):
    return (SIDE_TO_SPEED[side], feed)


# leftover_fn returns the designed-factor tuple that STILL VARIES inside a
# held-out fold for this (target, grouping) -- i.e. what a zero-image
# "nuisance lookup" baseline is allowed to condition on. An empty tuple means
# no other factor is available and the lookup degenerates to the global
# training-set majority class.
FOLD_CONFIGS = {
    ("feed", "primary"):        dict(group_fn=_feed_group,               leftover_fn=lambda s, f: ()),
    ("speed", "primary"):       dict(group_fn=_speed_group,              leftover_fn=lambda s, f: (f,)),
    ("doc", "primary"):         dict(group_fn=_doc_group,                leftover_fn=lambda s, f: ()),
    ("roughness", "primary"):   dict(group_fn=_roughness_group_primary,  leftover_fn=lambda s, f: (SIDE_TO_SPEED[s], f)),
    ("roughness", "secondary"): dict(group_fn=_roughness_group_secondary, leftover_fn=lambda s, f: (SIDE_TO_DOC[s],)),
}

# Expected (verified 2026-09-21) nuisance-lookup floor for each config, as
# (correct, total). feed/speed/doc must sit at exact chance; roughness/primary
# must be well below chance (doc held out -> lookup is noise, not signal);
# roughness/secondary is the CONFOUND case and is expected ABOVE chance.
EXPECTED_NUISANCE_FLOOR = {
    ("feed", "primary"):        (8, 24),
    ("speed", "primary"):       (12, 24),
    ("doc", "primary"):         (6, 24),
    ("roughness", "primary"):   (6, 24),
    ("roughness", "secondary"): (15, 24),
}


def build_loco_folds(df: pd.DataFrame, target: str, group_variant: str):
    cfg = FOLD_CONFIGS[(target, group_variant)]
    tmp = df.drop_duplicates("run_id")[["run_id", "side", "feed"]].copy()
    tmp["group"] = tmp.apply(lambda r: cfg["group_fn"](int(r["side"]), r["feed"]), axis=1)
    folds = []
    for g in sorted(tmp["group"].unique()):
        test_runs = set(tmp[tmp["group"] == g]["run_id"])
        train_runs = set(tmp["run_id"]) - test_runs
        folds.append((train_runs, test_runs))
    return folds


def nuisance_lookup_baseline(df: pd.DataFrame, target: str, group_variant: str):
    """Zero-image baseline: for each held-out LOCO fold, predict the target
    from whichever designed factors still vary WITHIN that fold (learned as a
    per-value majority class from the training folds only), falling back to
    the global training majority class if a leftover-key value wasn't seen in
    training. Returns (correct, total) pooled over all folds. See module
    docstring -- this is what catches the roughness/doc confound."""
    cfg = FOLD_CONFIGS[(target, group_variant)]
    run_df = df.drop_duplicates("run_id")[["run_id", "side", "feed", "ra"]].copy()
    run_df["label"] = run_df.apply(
        lambda r: label_for(target, int(r["side"]), r["feed"], r.get("ra")), axis=1)
    run_df["group"] = run_df.apply(lambda r: cfg["group_fn"](int(r["side"]), r["feed"]), axis=1)
    run_df["leftover"] = run_df.apply(lambda r: cfg["leftover_fn"](int(r["side"]), r["feed"]), axis=1)

    correct, total = 0, 0
    for g in sorted(run_df["group"].unique()):
        test = run_df[run_df["group"] == g]
        train = run_df[run_df["group"] != g]
        global_majority = train["label"].value_counts().idxmax()
        lookup = train.groupby("leftover")["label"].agg(lambda s: s.value_counts().idxmax())
        for _, row in test.iterrows():
            pred = lookup.get(row["leftover"], global_majority)
            correct += int(pred == row["label"])
            total += 1
    return correct, total


def run_selftest():
    """Fast (no training, no image loading), verifies the grouping-
    independence assumption behind every LOCO fold config in this script.
    Run this after any change to FOLD_CONFIGS / *_group() functions."""
    # labels.csv is identical across scalogram dirs for run/side/feed/ra
    # purposes -- use whichever exists.
    candidates = sorted(ROOT.glob("scalograms_32x*/labels.csv"))
    if not candidates:
        raise FileNotFoundError("No scalograms_32x*/labels.csv found for --selftest")
    df = pd.read_csv(candidates[0])
    print(f"--selftest using {candidates[0].relative_to(ROOT)}\n")

    all_ok = True
    for (target, variant), (exp_correct, exp_total) in EXPECTED_NUISANCE_FLOOR.items():
        got_correct, got_total = nuisance_lookup_baseline(df, target, variant)
        exp_frac, got_frac = exp_correct / exp_total, got_correct / got_total
        ok = got_total == exp_total and abs(got_frac - exp_frac) < 1e-6
        all_ok &= ok
        flag = "OK" if ok else "MISMATCH -- grouping-independence assumption may have changed!"
        print(f"  {target:<10s} {variant:<10s} nuisance-lookup floor = "
              f"{got_correct}/{got_total} ({got_frac:.3f})   expected {exp_correct}/{exp_total}   [{flag}]")

    print(f"\n{'ALL OK' if all_ok else 'FAILURES ABOVE'} -- roughness/primary should sit BELOW chance "
          f"(doc held out), roughness/secondary should sit ABOVE chance (doc leaks) -- both by design, "
          f"not bugs. feed/speed/doc must equal exact chance (1/3, 1/2, 1/4).")
    return all_ok


# ── native-resolution dataset (no resize, no ImageNet normalization) --
#    used by the cheap surrogate models only ───────────────────────────────
class NativeScalogramDataset(Dataset):
    def __init__(self, paths, labels, transform):
        self.paths, self.labels, self.transform = paths, labels, transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = _open_img(self.paths[idx]).convert("L")   # single grayscale channel
        return self.transform(img), self.labels[idx]


def native_transforms(noise_std=0.02):
    train_tf = transforms.Compose([
        transforms.ToTensor(), AddGaussianNoise(noise_std), transforms.Normalize([0.5], [0.5]),
    ])
    val_tf = transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])
    return train_tf, val_tf


# ── tiny from-scratch CNN -- kept for backward compatibility with existing
#    cv_summary.csv rows (feed target only; skipped by default for new runs,
#    see module docstring / project_shoulder_milling.md for why) ───────────
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


def train_tiny_cnn(train_paths, train_labels, num_classes, epochs, batch, lr, noise_std, seed, device):
    seed_everything(seed)
    train_tf, val_tf = native_transforms(noise_std)
    ds = NativeScalogramDataset(train_paths, train_labels, train_tf)
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
def predict_tiny_cnn(model, val_tf, paths, device):
    model.eval()
    ds = NativeScalogramDataset(paths, [0] * len(paths), val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    probs = []
    for imgs, _ in dl:
        probs.extend(torch.softmax(model(imgs.to(device)), dim=1).cpu().numpy())
    return np.array(probs)


# ── HGB (native pixels -> PCA -> HistGradientBoosting) -- generalized to any
#    target via label_for(), used as the fast plumbing check ──────────────
def load_pixels(paths):
    return np.stack([np.asarray(_open_img(p).convert("L"), dtype=np.float32).ravel() for p in paths])


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


def predict_residual_hgb(train_paths, train_labels, train_sides, test_paths, seed):
    """Feed-only: condition-prototype subtraction HGB (subtracts per-side
    mean, unsupervised). Kept for backward compatibility -- see
    residual_preprocessing_readme.md for why this doesn't generalize cleanly
    to the other 3 targets (side is the target's own defining factor for
    speed/doc, not a nuisance)."""
    Xtr_raw = load_pixels(train_paths)
    Xte_raw = load_pixels(test_paths)

    Xtr = np.empty_like(Xtr_raw)
    for side in np.unique(train_sides):
        mask = train_sides == side
        Xtr[mask] = Xtr_raw[mask] - Xtr_raw[mask].mean(axis=0)

    Xte = Xte_raw - Xte_raw.mean(axis=0)

    n_components = min(20, Xtr.shape[0] - 1)
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca", PCA(n_components=n_components, random_state=seed)),
        ("clf", HistGradientBoostingClassifier(max_iter=150, random_state=seed)),
    ])
    pipe.fit(Xtr, train_labels)
    return pipe.predict_proba(Xte)


# ── real ImageNet-pretrained backbone -- fine-tuned fresh per fold ────────
def train_backbone_cnn(train_paths, train_labels, num_classes, arch, dropout, epochs, batch, lr,
                        weight_decay, label_smooth, noise_std, seed, device):
    """Fixed epoch count, final-epoch model only -- no test-accuracy-driven
    checkpoint selection (see module docstring). Reuses cnn_train_param.py's
    build_model/build_transforms/ScalogramDataset/train_epoch verbatim, the
    same recipe that produced the standard-split headline numbers."""
    seed_everything(seed)
    train_tf, val_tf = build_transforms(noise_std)
    train_ds = ScalogramDataset(train_paths, train_labels, train_tf)
    train_dl = DataLoader(train_ds, batch_size=min(batch, len(train_ds)), shuffle=True,
                           num_workers=0, drop_last=len(train_ds) > batch)

    model = build_model(arch, num_classes=num_classes, dropout=dropout).to(device)
    counts = np.bincount(train_labels, minlength=num_classes).astype(float)
    counts[counts == 0] = 1.0
    weights = torch.tensor(1.0 / counts, dtype=torch.float32).to(device)
    weights = weights / weights.sum()
    criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=label_smooth)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

    final_train_acc = 0.0
    for _ in range(epochs):
        _, final_train_acc = train_epoch(model, train_dl, criterion, optimizer, device)
        scheduler.step()
    return model, val_tf, final_train_acc


@torch.no_grad()
def predict_backbone_cnn(model, val_tf, test_paths, device):
    model.eval()
    ds = ScalogramDataset(test_paths, [0] * len(test_paths), val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    probs = []
    for imgs, _ in dl:
        probs.extend(torch.softmax(model(imgs.to(device)), dim=1).cpu().numpy())
    return np.array(probs)


# ── voting + Clopper-Pearson CI ─────────────────────────────────────────────
def vote(probs, labels, run_ids):
    """Returns (window_acc, run_acc_hard, run_acc_soft) from per-window softmax probs.
    run_acc_soft (mean-probability vote) is the headline metric -- see module
    docstring for why hard vote is unreliable here (tie pathology on doc)."""
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


def clopper_pearson_ci(k: int, n: int, alpha: float = 0.05):
    """Exact binomial CI. Approximate/honest headline only -- see module
    docstring: there is no unbiased estimator of k-fold CV variance, this
    just gives a defensible interval over the pooled run count."""
    lo = 0.0 if k == 0 else beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - alpha / 2, k + 1, n - k)
    return lo, hi


# ── fold loop ────────────────────────────────────────────────────────────────
def run_cv(img_dir: Path, target: str, model_name: str, seed: int, split: str, group_variant: str,
           epochs: int, batch: int, lr: float, noise_std: float, weight_decay: float,
           label_smooth: float, dropout: float, arch: str, device, preproc: str = "none",
           preds_out=None):
    df = pd.read_csv(img_dir / "labels.csv")
    if "run_id" not in df.columns and "run" in df.columns:
        df = df.rename(columns={"run": "run_id"})
    spec = TARGETS[target]
    num_classes = spec["num_classes"]
    df["label"] = df.apply(lambda r: label_for(target, int(r["side"]), r["feed"], r.get("ra")), axis=1)

    if split == "standard":
        test_runs_std = set(spec["test_runs"])
        train_runs_std = set(df["run_id"].unique()) - test_runs_std
        folds = [(train_runs_std, test_runs_std)]
    else:
        if model_name in ("tiny_cnn", "residual_hgb") and target != "feed":
            raise ValueError(f"{model_name} is feed-only (backward-compat); use hgb or cnn for {target}")
        folds = build_loco_folds(df, target, group_variant)

    make_preproc = None
    if preproc != "none":
        try:
            from nested_preproc import make_preproc
        except ImportError as e:
            raise ImportError(
                f"--preproc {preproc} requires nested_preproc.py (providing "
                f"make_preproc(kind, img_dir, labels_df)) next to cv_evaluate.py, but it could "
                f"not be imported: {e}") from e

    cnn_dropout = dropout if dropout is not None else DEFAULT_DROPOUT[target]

    all_probs, all_labels, all_runs, fold_train_accs = [], [], [], []
    all_files, all_folds = [], []
    for fold_i, (train_runs, test_runs) in enumerate(folds, 1):
        train_df = df[df["run_id"].isin(train_runs)].reset_index(drop=True)
        test_df  = df[df["run_id"].isin(test_runs)].reset_index(drop=True)
        if make_preproc is None:
            train_paths  = [img_dir / fn for fn in train_df["filename"]]
            test_paths   = [img_dir / fn for fn in test_df["filename"]]
        else:
            # fresh preproc per fold; fit on TRAIN window indices only, then
            # transform train and test (indices = row positions in df)
            train_idx = np.flatnonzero(df["run_id"].isin(train_runs).to_numpy())
            test_idx  = np.flatnonzero(df["run_id"].isin(test_runs).to_numpy())
            pp = make_preproc(preproc, img_dir, df)
            pp.fit(train_idx)
            assert np.array_equal(np.asarray(pp.fit_idx_), train_idx),                 "preproc.fit must see exactly the training indices"
            assert not set(np.asarray(pp.fit_idx_).tolist()) & set(test_idx.tolist()),                 "test windows leaked into preproc.fit"
            train_paths = list(pp.transform(train_idx))
            test_paths  = list(pp.transform(test_idx))
            for _im in train_paths[:1] + test_paths[:1]:
                assert isinstance(_im, Image.Image) and _im.mode == "L",                     "nested_preproc.transform must return uint8 PIL 'L' images (see nested_preproc docstring)"
            assert len(train_paths) == len(train_idx) and len(test_paths) == len(test_idx), \
                "nested_preproc.transform must return one image per index"
        train_labels = train_df["label"].to_numpy()
        train_sides  = train_df["side"].to_numpy()
        test_labels  = test_df["label"].to_numpy()
        test_run_ids = test_df["run_id"].tolist()

        if model_name == "cnn":
            if len(folds) > 1:
                print(f"  [cnn] fold {fold_i}/{len(folds)}  test_runs={sorted(test_runs)}")
            model, val_tf, final_train_acc = train_backbone_cnn(
                train_paths, train_labels.tolist(), num_classes, arch, cnn_dropout, epochs, batch,
                lr, weight_decay, label_smooth, noise_std, seed, device)
            probs = predict_backbone_cnn(model, val_tf, test_paths, device)
            fold_train_accs.append(final_train_acc)
        elif model_name == "hgb":
            probs = predict_hgb(train_paths, train_labels, test_paths, seed)
        elif model_name == "residual_hgb":
            probs = predict_residual_hgb(train_paths, train_labels, train_sides, test_paths, seed)
        elif model_name == "tiny_cnn":
            model, val_tf = train_tiny_cnn(train_paths, train_labels, num_classes, epochs, batch, lr,
                                            noise_std, seed, device)
            probs = predict_tiny_cnn(model, val_tf, test_paths, device)
        else:
            raise ValueError(model_name)

        all_probs.append(probs)
        all_labels.extend(test_labels.tolist())
        all_runs.extend(test_run_ids)
        all_files.extend(test_df["filename"].tolist())
        all_folds.extend([fold_i] * len(test_df))

    all_probs = np.concatenate(all_probs, axis=0)
    all_labels = np.array(all_labels)
    if preds_out is not None:
        # per-window held-out softmax probs, for post-hoc P/R/F1 (see compute_prf1.py)
        preds_out = Path(preds_out)
        preds_out.parent.mkdir(parents=True, exist_ok=True)
        pdf = pd.DataFrame({"filename": all_files, "run_id": all_runs, "fold": all_folds,
                            "label": all_labels})
        for c in range(all_probs.shape[1]):
            pdf[f"p{c}"] = all_probs[:, c]
        pdf.to_csv(preds_out, index=False)
    window_acc, run_hard, run_soft = vote(all_probs, all_labels, all_runs)
    n_runs = len(set(all_runs))
    mean_train_acc = float(np.mean(fold_train_accs)) if fold_train_accs else None
    return window_acc, run_hard, run_soft, n_runs, mean_train_acc


def _git_sha():
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                       stderr=subprocess.DEVNULL, text=True).strip() or "unknown"
    except Exception:
        return "unknown"


def _append_row(path: Path, row: dict):
    """Append one row and flush. Header written if file is new/empty; if the
    existing header differs from this row's columns, the file is rewritten once
    with the union of columns (old rows get blanks)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    cols = list(row.keys())
    new_file = True
    if path.exists() and path.stat().st_size > 0:
        with open(path, newline="", encoding="utf-8") as f:
            existing = next(csv.reader(f), [])
        if existing != cols:
            prev = pd.read_csv(path)
            pd.concat([prev, pd.DataFrame([row])], ignore_index=True).to_csv(path, index=False)
            return
        new_file = False
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        if new_file:
            w.writeheader()
        w.writerow(row)
        f.flush()


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--selftest", action="store_true",
                        help="Verify the grouping-independence assumption for all target/grouping "
                             "configs (fast, no training) and exit.")
    parser.add_argument("--img_dir", default="scalograms_32x3_feedopt")
    parser.add_argument("--target", default="feed", choices=["speed", "feed", "doc", "roughness"])
    parser.add_argument("--split", default="loco", choices=["loco", "standard"],
                        help="'loco': leave-one-condition-out (default). 'standard': this target's "
                             "existing fixed train/test split, single fold -- the mandatory pre-flight "
                             "check that this pipeline reproduces the (corrected) standard-split number.")
    parser.add_argument("--roughness_group", default="primary", choices=["primary", "secondary"],
                        help="roughness LOCO only: 'primary' groups by doc (4 folds) -- recommended "
                             "headline, doc lookup is useless (~25%%, below chance). 'secondary' groups "
                             "by (speed,feed) (6 folds) -- doc leaks into training, nuisance floor is "
                             "~62.5%%; ALWAYS report both the LOCO number and this floor together.")
    parser.add_argument("--models", nargs="+", default=["hgb"],
                        choices=["hgb", "cnn", "tiny_cnn", "residual_hgb"],
                        help="tiny_cnn/residual_hgb are feed-only, kept for backward compatibility with "
                             "existing cv_summary.csv rows -- not recommended for new runs (see module "
                             "docstring). Use hgb for a fast plumbing check, cnn for the real headline.")
    parser.add_argument("--seeds", type=int, nargs="+", default=[42])
    parser.add_argument("--epochs", type=int, default=50,
                        help="cnn/tiny_cnn only. Matches the standard-split recipe -- do not reduce for "
                             "LOCO, or 'LOCO is harder' becomes confounded with 'trained less'.")
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--noise_std", type=float, default=0.02)
    parser.add_argument("--weight_decay", type=float, default=1e-4, help="cnn only")
    parser.add_argument("--label_smooth", type=float, default=0.05, help="cnn only")
    parser.add_argument("--dropout", type=float, default=None,
                        help="cnn only. Default: cnn_train_param.py's per-target DEFAULT_DROPOUT")
    parser.add_argument("--arch", default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"],
                        help="cnn only")
    parser.add_argument("--out_csv", default=None,
                        help="Write rows to ONLY this CSV (parent dirs created), appending+flushing after "
                             "each seed so a crash keeps completed seeds. Never touches cv_summary.csv. "
                             "Default (unset): legacy behaviour, rewrite cv_summary.csv at end of run.")
    parser.add_argument("--preproc", default="none",
                        choices=["none", "feedopt_nested", "residual_inductive"],
                        help="Fold-nested preprocessing via nested_preproc.make_preproc (fit on train "
                             "windows only per fold). 'none' = read scalogram PNGs directly.")
    parser.add_argument("--save_preds", default=None,
                        help="Directory. Also write per-window held-out softmax probabilities for each "
                             "(model, seed) run to <dir>/<target>__<scalogram>__<model>__<group>__s<seed>.csv "
                             "so precision/recall/F1 can be computed afterwards (compute_prf1.py). "
                             "Default (unset): nothing extra is written.")
    args = parser.parse_args()

    if args.selftest:
        ok = run_selftest()
        raise SystemExit(0 if ok else 1)

    group_variant = "primary" if args.target != "roughness" else args.roughness_group

    img_dir = ROOT / args.img_dir
    device  = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    def _load_labels(p):
        d = pd.read_csv(p)
        if "run_id" not in d.columns and "run" in d.columns:
            d = d.rename(columns={"run": "run_id"})
        return d

    n_folds = 1 if args.split == "standard" else len(build_loco_folds(
        _load_labels(img_dir / "labels.csv"), args.target, group_variant))
    print(f"Device: {device}   Scalogram: {img_dir.name}   Target: {args.target}   "
          f"Split: {args.split}{'' if args.split == 'standard' else f' (group={group_variant})'}   "
          f"{n_folds} fold(s)")

    if args.target == "roughness" and args.split == "loco":
        nf_correct, nf_total = nuisance_lookup_baseline(
            _load_labels(img_dir / "labels.csv"), "roughness", group_variant)
        print(f"  Nuisance-lookup floor for this grouping ({group_variant}): "
              f"{nf_correct}/{nf_total} = {nf_correct/nf_total:.3f} -- "
              f"{'compare LOCO numbers to THIS, not 50% chance' if group_variant == 'secondary' else 'below-chance sanity check, doc is genuinely held out'}")

    rows = []
    sha = _git_sha()
    out_csv = Path(args.out_csv) if args.out_csv else None
    for model_name in args.models:
        if model_name == "cnn":
            print(f"  [cnn] arch={args.arch}  epochs={args.epochs}  batch={args.batch}  lr={args.lr}  "
                  f"-- one fresh fine-tune per fold, this is slow, see module docstring")
        for seed in args.seeds:
            preds_out = None
            if args.save_preds:
                _tag = f"{model_name}-{args.arch}" if model_name == "cnn" else model_name
                _grp = group_variant if args.split == "loco" else "standard"
                preds_out = (Path(args.save_preds) /
                             f"{args.target}__{img_dir.name.replace('scalograms_', '')}__{_tag}"
                             f"__{_grp}__s{seed}.csv")
            window_acc, run_hard, run_soft, n_runs, mean_train_acc = run_cv(
                img_dir, args.target, model_name, seed, args.split, group_variant,
                args.epochs, args.batch, args.lr, args.noise_std, args.weight_decay,
                args.label_smooth, args.dropout, args.arch, device, args.preproc,
                preds_out,
            )
            k_soft = round(run_soft * n_runs)
            ci_lo, ci_hi = clopper_pearson_ci(k_soft, n_runs)
            train_acc_str = f"  train_acc={mean_train_acc:.3f}" if mean_train_acc is not None else ""
            print(f"  {model_name:12s} seed={seed:<4d} window_acc={window_acc:.3f}  "
                  f"run_acc_soft={run_soft:.3f} [{ci_lo:.3f},{ci_hi:.3f}] (HEADLINE)  "
                  f"run_acc_hard={run_hard:.3f}  (pooled over {n_runs} runs){train_acc_str}")
            rows.append({
                "target": args.target, "scalogram": img_dir.name.replace("scalograms_", ""),
                "model": model_name, "arch": args.arch if model_name == "cnn" else "",
                "split": args.split, "group": group_variant if args.split == "loco" else "",
                "seed": seed, "window_acc": round(window_acc, 4),
                "run_acc_soft": round(run_soft, 4), "run_acc_soft_ci_lo": round(ci_lo, 4),
                "run_acc_soft_ci_hi": round(ci_hi, 4), "run_acc_hard": round(run_hard, 4),
                "mean_final_train_acc": round(mean_train_acc, 4) if mean_train_acc is not None else "",
                "n_runs": n_runs,
                "lr": args.lr,
                "git_sha": sha,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "preproc": str(args.preproc),
            })
            if out_csv is not None:
                _append_row(out_csv, rows[-1])

    if out_csv is not None:
        out_path = out_csv
        out = pd.read_csv(out_path) if out_path.exists() else pd.DataFrame(rows)
        print(f"\nWrote {len(rows)} rows -> {out_path}")
    else:
        out = pd.DataFrame(rows)
        out_path = ROOT / "cv_summary.csv"
        if out_path.exists():
            prev = pd.read_csv(out_path)
            for col in out.columns:
                if col not in prev.columns:
                    prev[col] = ""
            if "target" not in prev.columns:
                prev["target"] = "feed"   # all pre-existing rows predate --target, were feed-only
            out = pd.concat([prev, out], ignore_index=True)
        out.to_csv(out_path, index=False)
        print(f"\nWrote {len(rows)} rows -> {out_path.name}")

    print("\n--- Mean +/- std across seeds (headline = run_acc_soft); never averaged across lr/arch/preproc ---")
    keys = ["target", "scalogram", "model", "arch", "split", "group", "lr", "preproc"]
    summ = out.copy()
    for k in keys:
        if k not in summ.columns:
            summ[k] = ""
        summ[k] = summ[k].fillna("").astype(str)
    for key, g in summ.groupby(keys, dropna=False):
        target, scalo, model, arch, split, group, lr, pp = key
        print(f"  {target:<10s} {scalo:<20s} {model:<10s} arch={arch:<14s} split={split:<8s} group={group:<9s} "
              f"lr={lr:<7s} preproc={pp:<18s} n={len(g)}  "
              f"run_soft={g['run_acc_soft'].astype(float).mean():.3f}+/-{g['run_acc_soft'].astype(float).std():.3f}  "
              f"run_hard={g['run_acc_hard'].astype(float).mean():.3f}+/-{g['run_acc_hard'].astype(float).std():.3f}")

if __name__ == "__main__":
    main()
