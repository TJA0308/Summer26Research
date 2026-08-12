"""
CNN training for End Milling's 32x3 (FFT / Mexican-hat CWT / Coiflet CWT)
feature-image pipeline -- mirrors Shoulder Milling's cnn_train_param.py,
adapted to End Milling's targets, label maps, and test-run splits (all
imported from cnn_train.py, this repo's existing scalogram training script,
so the two 32x3-specific pipelines and the original CWT-scalogram pipeline
never disagree about which run belongs to which class or split).

Why a separate script rather than reusing cnn_train.py directly
-----------------------------------------------------------------
cnn_train.py's transforms assume its scalograms are already 224x224 (built by
cnn_model/scalogram.py). The 32x3 feature images built by
../build_32x3_features.py are natively (32, 3) px -- tiny -- so they need an
explicit Resize to 224x224 before any pretrained backbone, exactly like
Shoulder Milling's cnn_train_param.py does for its (32, 3)/(32, 12) images.
Rather than bolt a conditional Resize onto the existing, already-working
cnn_train.py (used elsewhere for scalograms_10w etc.), this mirrors Shoulder
Milling's approach of a dedicated script for the small-native-resolution
feature-image case.

Targets (--target):
    speed        -- 5-class: 1500/2000/3000/4000/5000 rpm
    doc          -- 3-class: 0.015 / 0.030 / 0.060 mm
    feed_coarse  -- 3-class: low(3-4) / med(5-6) / high(7-8) mm/rev
    feed         -- 6-class: 3/4/5/6/7/8 mm/rev (fine-grained; same images
                    as feed_coarse, scale selection was already tuned against
                    the raw mm/rev value, see em_feature_common.select_cwt_rows)
    roughness    -- 3-class: Smooth(<0.7) / Medium(0.7-1.0) / Rough(>1.0) Ra um

Scalogram folder (--img_dir, relative to the repo root, one level up from
this file):
    scalograms_32x3                  (roughness-tuned scale selection)
    scalograms_32x3_feedopt          (feed_coarse/feed-tuned scale selection)
    scalograms_32x3_9win             (9 real time-windows/run variant)
    scalograms_32x3_feedopt_9win
    ..._residual / ..._residual_roughness   (after build_residual_scalograms.py)

Architectures (--arch): resnet18, resnet50, efficientnet_b0, convnext_tiny,
mobilenet_v3_large.

SMOTE: reads pre-generated synthetic runs from smote_<target>_labels.csv (for
plain training) or smote_labels.csv (for --conditioned / cascade training --
see cnn_train.py's load_smote_cond_map) if present -- run
../smote_generate_32x3.py first. --no_smote skips loading them.

Cascade conditioning:
  --conditioned          feed_coarse, feed, or roughness. Conditions on
                         GROUND-TRUTH speed + doc labels (a shortcut -- the
                         model is told the real answer for the parent
                         tasks). Useful as an upper bound / sanity check.
                         All three targets share the same DOC x speed
                         nuisance covariate that motivates condition-residual
                         correction in the first place (see
                         build_residual_scalograms.py's docstring), so all
                         are legitimate cascade candidates.
  --cascade_predicted    feed_coarse, feed, or roughness. Conditions on PREDICTED
                         speed + doc labels from speed_pred_<scalo_tag>[...]
                         .csv and doc_pred_<scalo_tag>[...].csv, written by
                         ../predict_conditioning_32x3.py after training and
                         selecting best speed/doc models. This is the
                         leakage-honest cascade -- the analogue of Shoulder
                         Milling's cnn_train_param.py auto-conditioning via
                         COND_PARENTS/predict_conditioning.py. SMOTE is
                         skipped in this mode (synthetic runs have no real
                         upstream speed/doc prediction to attach).
  Only one of --conditioned / --cascade_predicted may be set.

Cross-validation:
  --kfold N (N>1)        Stratified N-fold CV (folds built by cnn_train.py's
                         stratified_kfold(), same method its own --kfold
                         support uses) instead of the single fixed train/test
                         split -- reports mean/std run-level accuracy across
                         folds. This is the leakage-honest, "does this number
                         actually hold up" check Shoulder Milling's writeup
                         emphasizes (their ad-hoc single-split numbers for
                         feed were later shown inflated; only the CV number
                         -- 87.5% -- was trustworthy). Plain training only
                         (not compatible with --conditioned/--cascade_predicted).

Evaluation:
  Run-level accuracy is reported two ways: hard MAJORITY VOTE (argmax per
  window, then mode across a run's windows -- the original metric) and soft
  PROBABILITY AVERAGING (average per-window softmax probabilities across a
  run's windows, then argmax once). Averaging can recover runs where the
  vote is split near-evenly; End Milling's own README shows this pattern
  helping in several cases for the original CWT pipeline.

Usage examples:
    python cnn_train_32x3.py --target roughness --img_dir ../scalograms_32x3 --arch resnet18 --lr 1e-3
    python cnn_train_32x3.py --target feed_coarse --img_dir ../scalograms_32x3_feedopt --arch convnext_tiny --conditioned
    python cnn_train_32x3.py --target roughness --img_dir ../scalograms_32x3_residual_roughness --conditioned
    python cnn_train_32x3.py --target feed_coarse --img_dir ../scalograms_32x3_feedopt --cascade_predicted
    python cnn_train_32x3.py --target speed --img_dir ../scalograms_32x3_speedopt --arch resnet18 --kfold 5
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import classification_report, f1_score
from torch.utils.data import DataLoader
from torchvision import models, transforms

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))   # repo root -- for cond_prior (below)

from cnn_train import (   # noqa: E402  (repo-local import, path set above)
    SPEED_LABELS, SPEED_NAMES, SPEED_TEST_RUNS, SPEED_TEST_RUNS_BALANCED,
    SPEED_TEST_RUNS_ALT1, SPEED_TEST_RUNS_ALT2, SPEED_TEST_RUNS_ALT3, SPEED_TEST_RUNS_ALT4,
    SPEED_TEST_RUNS_ALT5, SPEED_TEST_RUNS_ALT6,
    DOC_LABELS, DOC_NAMES, DOC_TEST_RUNS, DOC_TEST_RUNS_12,
    DOC_TEST_RUNS_ALT1, DOC_TEST_RUNS_ALT2,
    FEED_COARSE_LABELS, FEED_COARSE_NAMES, FEED_COARSE_TEST_RUNS, FEED_COARSE_TEST_RUNS_12,
    FEED_COARSE_TEST_RUNS_ALT1, FEED_COARSE_TEST_RUNS_ALT2,
    FEED_COARSE_TEST_RUNS_ALT3, FEED_COARSE_TEST_RUNS_ALT4,
    FEED_LABELS, FEED_NAMES, FEED_TEST_RUNS,
    RA_LABELS, RA_NAMES, RA_TEST_RUNS, RA_TEST_RUNS_12,
    RA_TEST_RUNS_ALT1, RA_TEST_RUNS_ALT2,
    ScalogramDataset, ConditionedScalogramDataset,
    load_split, load_split_conditioned, load_smote_map, load_smote_cond_map,
    stratified_kfold, load_smote_full, smote_for_fold,
)
import cond_prior   # noqa: E402  (repo-local import, path set above) -- condition-prior stacking

SEED = 42
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

TARGETS = {
    "speed": {
        "num_classes": 5, "class_names": SPEED_NAMES,
        "label_map": SPEED_LABELS,
        "test_runs_standard": SPEED_TEST_RUNS, "test_runs_balanced": SPEED_TEST_RUNS_BALANCED,
        "test_runs_alt1": SPEED_TEST_RUNS_ALT1, "test_runs_alt2": SPEED_TEST_RUNS_ALT2,
        "test_runs_alt3": SPEED_TEST_RUNS_ALT3, "test_runs_alt4": SPEED_TEST_RUNS_ALT4,
        "test_runs_alt5": SPEED_TEST_RUNS_ALT5, "test_runs_alt6": SPEED_TEST_RUNS_ALT6,
        # Aliased to RA_TEST_RUNS_ALT1/ALT2 (not speed's own splits): lets a
        # speed model be trained held-out on EXACTLY roughness's alt1/alt2
        # test runs, so predict_conditioning_32x3.py's parent predictions
        # for roughness's cascade retrain don't leak roughness's held-out
        # runs through a speed model that already trained on them.
        "test_runs_rough_alt1": RA_TEST_RUNS_ALT1, "test_runs_rough_alt2": RA_TEST_RUNS_ALT2,
        "smote_csv": "smote_speed_labels.csv",
    },
    "doc": {
        "num_classes": 3, "class_names": DOC_NAMES,
        "label_map": DOC_LABELS,
        "test_runs_standard": DOC_TEST_RUNS, "test_runs_balanced": DOC_TEST_RUNS_12,
        "test_runs_alt1": DOC_TEST_RUNS_ALT1, "test_runs_alt2": DOC_TEST_RUNS_ALT2,
        # See speed's identical "test_runs_rough_alt1/2" comment above.
        "test_runs_rough_alt1": RA_TEST_RUNS_ALT1, "test_runs_rough_alt2": RA_TEST_RUNS_ALT2,
        "smote_csv": "smote_doc_labels.csv",
    },
    "feed_coarse": {
        "num_classes": 3, "class_names": FEED_COARSE_NAMES,
        "label_map": FEED_COARSE_LABELS,
        "test_runs_standard": FEED_COARSE_TEST_RUNS, "test_runs_balanced": FEED_COARSE_TEST_RUNS_12,
        "test_runs_alt1": FEED_COARSE_TEST_RUNS_ALT1, "test_runs_alt2": FEED_COARSE_TEST_RUNS_ALT2,
        "test_runs_alt3": FEED_COARSE_TEST_RUNS_ALT3, "test_runs_alt4": FEED_COARSE_TEST_RUNS_ALT4,
        "smote_csv": "smote_feed_coarse_labels.csv",
    },
    "feed": {
        # 6-class fine-grained feed (3/4/5/6/7/8 mm/rev) -- same runs/images
        # as feed_coarse, just unrounded labels. No dedicated "balanced"
        # variant exists (see FEED_TEST_RUNS's comment in cnn_train.py for
        # why: class 5 only has 3 runs total), so both split modes use the
        # same fixed test set.
        "num_classes": 6, "class_names": FEED_NAMES,
        "label_map": FEED_LABELS,
        "test_runs_standard": FEED_TEST_RUNS, "test_runs_balanced": FEED_TEST_RUNS,
        "smote_csv": "smote_labels.csv",
    },
    "roughness": {
        "num_classes": 3, "class_names": RA_NAMES,
        "label_map": RA_LABELS,
        "test_runs_standard": RA_TEST_RUNS, "test_runs_balanced": RA_TEST_RUNS_12,
        "test_runs_alt1": RA_TEST_RUNS_ALT1, "test_runs_alt2": RA_TEST_RUNS_ALT2,
        "smote_csv": "smote_roughness_labels.csv",
    },
}

# Carried over from Shoulder Milling's DEFAULT_DROPOUT finding (speed doesn't
# overfit, others do) as an initial guess for this new feature set -- not yet
# separately validated here.
DEFAULT_DROPOUT = {"speed": 0.0, "doc": 0.15, "feed_coarse": 0.15, "feed": 0.15, "roughness": 0.15}

# End Milling's cascade shape is fixed: a cascading target conditions
# jointly on BOTH speed and doc (never a subset) -- see cnn_train.py's
# ConditionedResNet. feed_coarse, feed, and roughness all qualify: they
# share the DOC x speed nuisance covariate condition-residual correction
# targets (see build_residual_scalograms.py's docstring) -- speed/doc
# themselves don't, since they already hit ~100% on raw features with
# nothing to cascade from. feed (6-class) is just feed_coarse's ungrouped
# version of the same causal-downstream-of-condition relationship, so the
# same condition-prior stacking logic applies unchanged.
COND_PARENTS = {"feed_coarse": ["speed", "doc"], "feed": ["speed", "doc"], "roughness": ["speed", "doc"]}
COND_DIMS    = {"speed": 5, "doc": 3}


def seed_everything(seed: int):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


# ── transforms ───────────────────────────────────────────────────────────────
class AddGaussianNoise:
    """Adds N(0, std) noise to a [0,1]-scaled tensor before ImageNet
    normalisation. These "images" are z-scored engineered feature matrices
    (FFT bands, CWT scale energies), not photographs -- RandomHorizontalFlip
    / ColorJitter would scramble those numeric features in physically
    meaningless ways. Small additive noise is the closer analogue of real
    sensor/measurement noise (same rationale as Shoulder Milling's
    cnn_train_param.py, which this is copied from)."""
    def __init__(self, std: float = 0.02):
        self.std = std

    def __call__(self, tensor):
        if self.std <= 0:
            return tensor
        return tensor + torch.randn_like(tensor) * self.std


class OrdinalCELoss(nn.Module):
    """Cross-entropy + differentiable ordinal distance penalty.

    For ordered classes (0 < 1 < 2 …), predicting class 2 when the true label
    is 0 should hurt more than predicting class 1. Standard CE treats all wrong
    classes identically. This loss adds alpha * E_k[|y-k| * p_k] to the CE so
    the gradient pushes predictions toward adjacent rather than distant classes.

    alpha=1.0 keeps the two terms roughly on the same scale for 3-class targets;
    lower alpha → closer to plain CE.
    """
    def __init__(self, n_cls: int, alpha: float = 1.0, weight=None):
        super().__init__()
        dist = torch.zeros(n_cls, n_cls)
        for i in range(n_cls):
            for j in range(n_cls):
                dist[i, j] = abs(i - j)
        self.register_buffer("dist", dist)
        self.alpha = alpha
        self.weight = weight

    def forward(self, logits, targets):
        probs = torch.softmax(logits, dim=1)
        ordinal_penalty = (probs * self.dist.to(targets.device)[targets]).sum(dim=1).mean()
        ce = F.cross_entropy(logits, targets, weight=self.weight)
        return ce + self.alpha * ordinal_penalty


def build_transforms(noise_std: float = 0.02):
    train_tf = transforms.Compose([
        transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        AddGaussianNoise(noise_std),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    val_tf = transforms.Compose([
        transforms.Resize((224, 224), interpolation=transforms.InterpolationMode.BILINEAR),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    return train_tf, val_tf


# ── model factory ────────────────────────────────────────────────────────────
def build_model(arch: str, num_classes: int, dropout: float = 0.0) -> nn.Module:
    def head(in_features):
        if dropout > 0:
            return nn.Sequential(nn.Dropout(dropout), nn.Linear(in_features, num_classes))
        return nn.Linear(in_features, num_classes)

    if arch == "resnet18":
        m = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        m.fc = head(m.fc.in_features)
    elif arch == "resnet50":
        m = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        m.fc = head(m.fc.in_features)
    elif arch == "efficientnet_b0":
        m = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        m.classifier[1] = head(m.classifier[1].in_features)
    elif arch == "convnext_tiny":
        m = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
        m.classifier[2] = head(m.classifier[2].in_features)
    elif arch == "mobilenet_v3_large":
        m = models.mobilenet_v3_large(weights=models.MobileNet_V3_Large_Weights.DEFAULT)
        m.classifier[3] = head(m.classifier[3].in_features)
    else:
        raise ValueError(f"Unknown arch: {arch}")
    return m


class ConditionedModel(nn.Module):
    """Wraps any of the 4 backbones; concatenates one-hot speed+doc vectors
    with the pooled image features before the final classifier head. Generic
    over cond_dims (unlike cnn_train.py's fixed ConditionedResNet), copied
    from Shoulder Milling's cnn_train_param.py."""
    def __init__(self, arch: str, num_classes: int, cond_dims: list, dropout: float = 0.0):
        super().__init__()
        self.cond_dims = cond_dims

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
            base.classifier = nn.Sequential(base.classifier[0], base.classifier[1])
        else:
            raise ValueError(f"Unknown arch for ConditionedModel: {arch}")

        self.backbone = base
        in_dim = feat_dim + sum(cond_dims)
        self.head = (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_dim, num_classes))
                     if dropout > 0 else nn.Linear(in_dim, num_classes))

    def forward(self, img, *cond_labels):
        feats = self.backbone(img)
        onehots = [F.one_hot(lbl, num_classes=d).float() for lbl, d in zip(cond_labels, self.cond_dims)]
        return self.head(torch.cat([feats] + onehots, dim=1))


# ── predicted-parent conditioning (the leakage-honest cascade) ─────────────
def load_predicted_conditioning(img_dir: Path, parent: str, paths: list, scalo_tag: str, run_tag: str):
    """Loads <parent>_pred_<scalo_tag>[_<run_tag>].csv (written by
    ../predict_conditioning_32x3.py) and returns predicted labels aligned to
    `paths`, or None if that file doesn't exist yet."""
    suffix = f"_{run_tag}" if run_tag else ""
    csv_path = img_dir / f"{parent}_pred_{scalo_tag}{suffix}.csv"
    if not csv_path.exists():
        return None
    df = pd.read_csv(csv_path).set_index("filename")
    return [int(df.loc[Path(p).name, "pred_label"]) for p in paths]


# ── training / evaluation ───────────────────────────────────────────────────
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        out = model(imgs)
        loss = criterion(out, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(labels)
        correct += (out.argmax(1) == labels).sum().item()
        n += len(labels)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    all_preds, all_labels = [], []
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        out = model(imgs)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        preds = out.argmax(1)
        correct += (preds == labels).sum().item()
        n += len(labels)
        all_preds.extend(preds.cpu().tolist())
        all_labels.extend(labels.cpu().tolist())
    return total_loss / n, correct / n, all_preds, all_labels


def train_epoch_cond(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels, *conds in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        conds = [c.to(device) for c in conds]
        optimizer.zero_grad()
        out = model(imgs, *conds)
        loss = criterion(out, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(labels)
        correct += (out.argmax(1) == labels).sum().item()
        n += len(labels)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch_cond(model, loader, criterion, device):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    all_preds, all_labels = [], []
    for imgs, labels, *conds in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        conds = [c.to(device) for c in conds]
        out = model(imgs, *conds)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        preds = out.argmax(1)
        correct += (preds == labels).sum().item()
        n += len(labels)
        all_preds.extend(preds.cpu().tolist())
        all_labels.extend(labels.cpu().tolist())
    return total_loss / n, correct / n, all_preds, all_labels


def _vote(all_preds, labels, run_ids):
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


@torch.no_grad()
def majority_vote_accuracy(model, paths, labels, run_ids, val_tf, device):
    model.eval()
    ds = ScalogramDataset(paths, labels, val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    all_preds = []
    for imgs, _ in dl:
        all_preds.extend(model(imgs.to(device)).argmax(1).cpu().tolist())
    return _vote(all_preds, labels, run_ids)


@torch.no_grad()
def majority_vote_accuracy_cond(model, paths, labels, run_ids, cond_labels_list, val_tf, device):
    model.eval()
    ds = ConditionedScalogramDataset(paths, labels, cond_labels_list[0], cond_labels_list[1], val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    all_preds = []
    for imgs, _lbls, spd, doc in dl:
        all_preds.extend(model(imgs.to(device), spd.to(device), doc.to(device)).argmax(1).cpu().tolist())
    return _vote(all_preds, labels, run_ids)


def _soft_vote(all_probs, labels, run_ids):
    """Averages per-window softmax probabilities within each run, then
    argmaxes once -- an alternative to _vote()'s hard majority vote that can
    recover runs where the window-level vote is split near-evenly (a run
    with e.g. 5/9 windows for the wrong class still hard-votes wrong, but
    might average to the right class if the margins are close)."""
    run_probs, run_true = {}, {}
    for prob, true, run in zip(all_probs, labels, run_ids):
        run_probs.setdefault(run, []).append(prob)
        run_true[run] = true
    correct = 0
    vote_preds, vote_true = [], []
    for run in run_true:
        avg_prob = torch.stack(run_probs[run]).mean(dim=0)
        pred = int(avg_prob.argmax().item())
        vote_preds.append(pred)
        vote_true.append(run_true[run])
        if pred == run_true[run]:
            correct += 1
    return correct / len(run_true), vote_preds, vote_true


@torch.no_grad()
def soft_vote_accuracy(model, paths, labels, run_ids, val_tf, device):
    model.eval()
    ds = ScalogramDataset(paths, labels, val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    all_probs = []
    for imgs, _ in dl:
        probs = torch.softmax(model(imgs.to(device)), dim=1).cpu()
        all_probs.extend(probs.unbind(0))
    return _soft_vote(all_probs, labels, run_ids)


@torch.no_grad()
def soft_vote_accuracy_cond(model, paths, labels, run_ids, cond_labels_list, val_tf, device):
    model.eval()
    ds = ConditionedScalogramDataset(paths, labels, cond_labels_list[0], cond_labels_list[1], val_tf)
    dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
    all_probs = []
    for imgs, _lbls, spd, doc in dl:
        probs = torch.softmax(model(imgs.to(device), spd.to(device), doc.to(device)), dim=1).cpu()
        all_probs.extend(probs.unbind(0))
    return _soft_vote(all_probs, labels, run_ids)


@torch.no_grad()
def run_prob_vectors(model, paths, labels, run_ids, val_tf, device, cond_labels_list=None):
    """Returns (run_probs: {run: np.ndarray[num_classes]}, run_true: {run: int}) --
    the per-run averaged softmax probability vector that _soft_vote() computes
    internally (see its `avg_prob = torch.stack(run_probs[run]).mean(dim=0)`)
    but discards after argmax. Needed for condition-prior probability stacking
    (cond_prior.py) -- both stack_conditioning_32x3.py (post-hoc, an already-
    trained checkpoint) and this module's own main() call this, so the
    forward-pass loop lives in exactly one place.

    cond_labels_list=[spd, doc] routes through ConditionedScalogramDataset /
    model(imgs, spd, doc) (matching soft_vote_accuracy_cond); None routes
    through the plain ScalogramDataset / model(imgs) path (matching
    soft_vote_accuracy) -- so this works for both cascading and plain
    checkpoints."""
    model.eval()
    if cond_labels_list is not None:
        ds = ConditionedScalogramDataset(paths, labels, cond_labels_list[0], cond_labels_list[1], val_tf)
        dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
        all_probs = []
        for imgs, _lbls, spd, doc in dl:
            probs = torch.softmax(model(imgs.to(device), spd.to(device), doc.to(device)), dim=1).cpu()
            all_probs.extend(probs.unbind(0))
    else:
        ds = ScalogramDataset(paths, labels, val_tf)
        dl = DataLoader(ds, batch_size=16, shuffle=False, num_workers=0)
        all_probs = []
        for imgs, _ in dl:
            probs = torch.softmax(model(imgs.to(device)), dim=1).cpu()
            all_probs.extend(probs.unbind(0))

    run_prob_lists, run_true = {}, {}
    for prob, true, run in zip(all_probs, labels, run_ids):
        run_prob_lists.setdefault(run, []).append(prob)
        run_true[run] = true
    run_probs = {run: torch.stack(probs).mean(dim=0).numpy() for run, probs in run_prob_lists.items()}
    return run_probs, run_true


def run_ids_from_paths(paths):
    return [Path(p).stem.split("_w")[0] for p in paths]


def run_kfold(args, spec, img_dir, scalo_tag, device, dropout, train_tf, val_tf):
    """Stratified N-fold CV: same stratified_kfold() method cnn_train.py's own
    --kfold uses. Plain (non-cascade) training only -- trains a fresh model
    per fold, reports window-level and BOTH run-level (majority-vote,
    soft-vote) accuracy, mean/std across folds. This is what actually tells
    you whether a single-fixed-split number is trustworthy or a lucky/
    unlucky split -- see the module docstring's Shoulder Milling caveat."""
    smote_full = {} if args.no_smote else load_smote_full(img_dir, spec["smote_csv"])
    splits = stratified_kfold(spec["label_map"], args.kfold)

    fold_win_accs, fold_vote_accs, fold_soft_accs = [], [], []
    for fold_i, (fold_train, fold_test) in enumerate(splits, 1):
        print(f"\n{'=' * 60}\nFold {fold_i}/{args.kfold}  "
              f"train={len(fold_train)} runs  test={len(fold_test)} runs")
        fold_smote = smote_for_fold(smote_full, fold_train) if smote_full else {}
        if fold_smote:
            print(f"  SMOTE: {len(fold_smote)} synthetic runs valid for this fold "
                  f"(both parents in train)")

        (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, spec["label_map"], fold_test, fold_smote)
        if not tr_p or not te_p:
            print("  Skipping fold -- empty train or test split")
            continue

        train_ds = ScalogramDataset(tr_p, tr_l, train_tf)
        test_ds = ScalogramDataset(te_p, te_l, val_tf)
        train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=0)
        test_dl = DataLoader(test_ds, batch_size=args.batch, shuffle=False, num_workers=0)

        model = build_model(args.arch, spec["num_classes"], dropout=dropout).to(device)
        counts = np.bincount(tr_l, minlength=spec["num_classes"]).astype(float)
        counts[counts == 0] = 1.0
        weights = torch.tensor(1.0 / counts, dtype=torch.float32).to(device)
        weights = weights / weights.sum()
        if args.ordinal_loss:
            criterion = OrdinalCELoss(spec["num_classes"], alpha=args.ordinal_alpha, weight=weights)
        else:
            criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=args.label_smooth)
        optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

        for epoch in range(1, args.epochs + 1):
            train_epoch(model, train_dl, criterion, optimizer, device)
            _, te_acc, _, _ = eval_epoch(model, test_dl, criterion, device)
            scheduler.step()

        # Fixed-epoch-count result -- no test-accuracy-driven checkpoint
        # selection (same leakage `cnn_train_32x3.py`'s main() path had; see
        # Shoulder Milling/residual_preprocessing_readme.md's bias source #2).
        best_fold_win_acc = te_acc
        te_run_ids = run_ids_from_paths(te_p)
        vote_acc, _, _ = majority_vote_accuracy(model, te_p, te_l, te_run_ids, val_tf, device)
        soft_acc, _, _ = soft_vote_accuracy(model, te_p, te_l, te_run_ids, val_tf, device)

        print(f"  Fold {fold_i} result: window acc={best_fold_win_acc:.3f}  "
              f"run majority-vote acc={vote_acc:.3f}  run soft-vote acc={soft_acc:.3f}")
        fold_win_accs.append(best_fold_win_acc)
        fold_vote_accs.append(vote_acc)
        fold_soft_accs.append(soft_acc)

    print(f"\n{'=' * 60}")
    print(f"K-fold ({args.kfold}) results across {len(fold_win_accs)} folds:")
    print(f"  Window acc            : mean={np.mean(fold_win_accs):.3f}  std={np.std(fold_win_accs):.3f}")
    print(f"  Run majority-vote acc : mean={np.mean(fold_vote_accs):.3f}  std={np.std(fold_vote_accs):.3f}")
    print(f"  Run soft-vote acc     : mean={np.mean(fold_soft_accs):.3f}  std={np.std(fold_soft_accs):.3f}")

    out_dir = HERE / f"models_{args.target}_{scalo_tag}"
    out_dir.mkdir(exist_ok=True)
    kfold_path = out_dir / f"{args.arch}_lr{args.lr:g}_kfold{args.kfold}_results.json"
    with open(kfold_path, "w") as f:
        json.dump({
            "target": args.target, "img_dir": str(img_dir), "arch": args.arch,
            "kfold": args.kfold, "epochs": args.epochs, "lr": args.lr,
            "smote": not args.no_smote, "dropout": dropout,
            "fold_window_acc": [round(a, 4) for a in fold_win_accs],
            "fold_run_vote_acc": [round(a, 4) for a in fold_vote_accs],
            "fold_run_soft_acc": [round(a, 4) for a in fold_soft_accs],
            "mean_window_acc": round(float(np.mean(fold_win_accs)), 4),
            "mean_run_vote_acc": round(float(np.mean(fold_vote_accs)), 4),
            "std_run_vote_acc": round(float(np.std(fold_vote_accs)), 4),
            "mean_run_soft_acc": round(float(np.mean(fold_soft_accs)), 4),
            "std_run_soft_acc": round(float(np.std(fold_soft_accs)), 4),
        }, f, indent=2)
    print(f"\nK-fold results saved to {kfold_path}")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", required=True, choices=list(TARGETS.keys()))
    parser.add_argument("--img_dir", required=True,
                        help="Path to a scalograms_32x3* directory (relative to cwd)")
    parser.add_argument("--arch", default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0",
                                 "convnext_tiny", "mobilenet_v3_large"])
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch", type=int, default=8)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--weight_decay", type=float, default=1e-4)
    parser.add_argument("--no_smote", action="store_true",
                        help="Skip loading pre-generated SMOTE synthetic runs")
    parser.add_argument("--dropout", type=float, default=None,
                        help="Default: per-target (see DEFAULT_DROPOUT)")
    parser.add_argument("--label_smooth", type=float, default=0.05)
    parser.add_argument("--noise_std", type=float, default=0.02)
    parser.add_argument("--run_tag", default="",
                        help="Optional filename suffix; also used to locate "
                             "<parent>_pred_<scalo_tag>_<run_tag>.csv for --cascade_predicted")
    parser.add_argument("--split", default="standard",
                        choices=["standard", "balanced", "alt1", "alt2", "alt3", "alt4", "alt5", "alt6",
                                 "rough_alt1", "rough_alt2"],
                        help="Which *_TEST_RUNS set from cnn_train.py to use, checked against "
                             "TARGETS[target]['test_runs_<split>'] (SystemExit if undefined for "
                             "this target). alt1/alt2 exist for speed, feed_coarse, doc, and "
                             "roughness -- all fully disjoint from that target's standard split "
                             "except feed_coarse's/roughness's smallest class, which shares a "
                             "handful of runs between alt1/alt2 themselves (never with standard) "
                             "due to limited pool size. alt3/alt4 exist for speed and feed_coarse; "
                             "alt5/alt6 exist for speed only. rough_alt1/rough_alt2 exist for speed "
                             "and doc only -- aliased to roughness's RA_TEST_RUNS_ALT1/ALT2, used to "
                             "train a speed/doc parent model held out on exactly roughness's alt-split "
                             "test runs before running predict_conditioning_32x3.py, so roughness's "
                             "cascade-conditioned retrain under a new split doesn't leak its held-out "
                             "runs through a parent model that already trained on them. Mirrors "
                             "Shoulder Milling's exp11/exp12 practice of checking whether a config's "
                             "accuracy survives a different held-out set.")
    parser.add_argument("--conditioned", action="store_true",
                        help="feed_coarse/feed/roughness only: condition on GROUND-TRUTH speed+doc")
    parser.add_argument("--cascade_predicted", action="store_true",
                        help="feed_coarse/feed/roughness only: condition on PREDICTED speed+doc "
                             "(run predict_conditioning_32x3.py for both first)")
    parser.add_argument("--kfold", type=int, default=1,
                        help="Stratified N-fold CV (1=single fixed split, N>1=N-fold). "
                             "Not compatible with --conditioned/--cascade_predicted.")
    parser.add_argument("--ordinal_loss", action="store_true",
                        help="Replace CE with ordinal CE (CE + distance penalty). "
                             "Meaningful for ordered targets: feed_coarse (low<med<high), "
                             "doc (0.015<0.030<0.060), roughness (smooth<medium<rough).")
    parser.add_argument("--ordinal_alpha", type=float, default=1.0,
                        help="Weight of the ordinal distance penalty term (see OrdinalCELoss). "
                             "1.0 keeps CE and penalty on similar scale for 3-class targets.")
    parser.add_argument("--cond_weight", type=float, default=0.7,
                        help="feed_coarse/feed/roughness only: weight given to the condition-prior "
                             "model (cond_prior.py, fit on (DOC,speed) one-hot alone) vs this "
                             "run's own image-model probabilities when computing the additive "
                             "run_level_stack_acc metric. Post-hoc only -- affects nothing about "
                             "how this model is trained, only what gets reported alongside it.")
    args = parser.parse_args()

    if args.conditioned and args.cascade_predicted:
        raise SystemExit("Pass only one of --conditioned / --cascade_predicted")
    if (args.conditioned or args.cascade_predicted) and args.target not in COND_PARENTS:
        raise SystemExit(f"--conditioned / --cascade_predicted only apply to "
                          f"--target in {list(COND_PARENTS.keys())}")
    if args.kfold > 1 and (args.conditioned or args.cascade_predicted):
        raise SystemExit("--kfold is not compatible with --conditioned/--cascade_predicted")

    dropout = args.dropout if args.dropout is not None else DEFAULT_DROPOUT[args.target]
    seed_everything(SEED)

    img_dir = Path(args.img_dir)
    scalo_tag = img_dir.name.replace("scalograms_", "")
    out_dir = HERE / f"models_{args.target}_{scalo_tag}"
    out_dir.mkdir(exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    spec = TARGETS[args.target]
    if args.split not in ("standard", "balanced") and f"test_runs_{args.split}" not in spec:
        raise SystemExit(f"--split {args.split} is not defined for --target {args.target} "
                          f"(defined splits for this target: standard, balanced, "
                          f"{', '.join(k.removeprefix('test_runs_') for k in spec if k.startswith('test_runs_alt') or k.startswith('test_runs_rough'))})")
    test_runs = {
        "standard": spec["test_runs_standard"],
        "balanced": spec["test_runs_balanced"],
        "alt1": spec.get("test_runs_alt1"),
        "alt2": spec.get("test_runs_alt2"),
        "alt3": spec.get("test_runs_alt3"),
        "alt4": spec.get("test_runs_alt4"),
        "alt5": spec.get("test_runs_alt5"),
        "alt6": spec.get("test_runs_alt6"),
        "rough_alt1": spec.get("test_runs_rough_alt1"),
        "rough_alt2": spec.get("test_runs_rough_alt2"),
    }[args.split]
    print(f"Device    : {device}")
    print(f"Target    : {args.target}  ({spec['num_classes']} classes)")
    print(f"Img dir   : {img_dir}")
    print(f"Arch      : {args.arch}   LR: {args.lr}   Dropout: {dropout}   Split: {args.split}")

    train_tf, val_tf = build_transforms(args.noise_std)

    if args.kfold > 1:
        print(f"K-fold CV : {args.kfold} folds (stratified)")
        run_kfold(args, spec, img_dir, scalo_tag, device, dropout, train_tf, val_tf)
        return

    cascading = args.conditioned or args.cascade_predicted
    if cascading:
        (tr_p, tr_l, tr_spd, tr_doc), (te_p, te_l, te_spd, te_doc) = load_split_conditioned(
            img_dir, spec["label_map"], test_runs, SPEED_LABELS, DOC_LABELS)

        if args.cascade_predicted:
            for parent in ("speed", "doc"):
                pred_tr = load_predicted_conditioning(img_dir, parent, tr_p, scalo_tag, args.run_tag)
                pred_te = load_predicted_conditioning(img_dir, parent, te_p, scalo_tag, args.run_tag)
                if pred_tr is None or pred_te is None:
                    raise SystemExit(
                        f"--cascade_predicted requires {parent}_pred_{scalo_tag}"
                        f"{'_' + args.run_tag if args.run_tag else ''}.csv in {img_dir} -- "
                        f"run predict_conditioning_32x3.py --target {parent} first."
                    )
                if parent == "speed":
                    tr_spd[:], te_spd[:] = pred_tr, pred_te
                else:
                    tr_doc[:], te_doc[:] = pred_tr, pred_te
            print("  Cascade: conditioning on PREDICTED speed+doc "
                  f"(speed_pred_{scalo_tag}.csv, doc_pred_{scalo_tag}.csv)")
        else:
            print("  Cascade: conditioning on GROUND-TRUTH speed+doc (shortcut / upper-bound mode)")

        if not args.no_smote:
            print("  SMOTE: skipped in cascade mode (synthetic runs have no real "
                  "upstream speed/doc value to attach)")

        print(f"\nTrain windows : {len(tr_p)}  |  Test windows : {len(te_p)}")
        for c, name in spec["class_names"].items():
            print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")
        if not tr_p:
            raise SystemExit("No training images found -- run build_32x3_features.py first.")

        train_ds = ConditionedScalogramDataset(tr_p, tr_l, tr_spd, tr_doc, train_tf)
        test_ds  = ConditionedScalogramDataset(te_p, te_l, te_spd, te_doc, val_tf)
        model = ConditionedModel(args.arch, spec["num_classes"],
                                  [COND_DIMS["speed"], COND_DIMS["doc"]], dropout=dropout).to(device)
        train_fn, eval_fn = train_epoch_cond, eval_epoch_cond
    else:
        smote_map = {}
        if not args.no_smote:
            smote_map = load_smote_map(img_dir, spec["smote_csv"])
            if smote_map:
                print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from {spec['smote_csv']}")

        (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, spec["label_map"], test_runs, smote_map)
        print(f"\nTrain windows : {len(tr_p)}  |  Test windows : {len(te_p)}")
        for c, name in spec["class_names"].items():
            print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")
        if not tr_p:
            raise SystemExit("No training images found -- run build_32x3_features.py first.")

        train_ds = ScalogramDataset(tr_p, tr_l, train_tf)
        test_ds  = ScalogramDataset(te_p, te_l, val_tf)
        model = build_model(args.arch, spec["num_classes"], dropout=dropout).to(device)
        train_fn, eval_fn = train_epoch, eval_epoch

    counts = np.bincount(tr_l, minlength=spec["num_classes"]).astype(float)
    counts[counts == 0] = 1.0
    weights = torch.tensor(1.0 / counts, dtype=torch.float32).to(device)
    weights = weights / weights.sum()
    print(f"\nClass weights: {weights.cpu().numpy().round(3)}")

    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True, num_workers=0)
    test_dl  = DataLoader(test_ds, batch_size=args.batch, shuffle=False, num_workers=0)

    if args.ordinal_loss:
        criterion = OrdinalCELoss(spec["num_classes"], alpha=args.ordinal_alpha, weight=weights)
        print(f"Loss: OrdinalCE (alpha={args.ordinal_alpha})")
    else:
        criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=args.label_smooth)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    tag = f"{args.arch}_lr{args.lr:g}"
    if args.run_tag:
        tag += f"_{args.run_tag}"
    history = []

    print(f"\n{'Ep':>4}  {'TrLoss':>8}  {'TrAcc':>7}  {'TeLoss':>8}  {'TeAcc':>7}  {'TeF1':>6}")
    print("-" * 50)
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_fn(model, train_dl, criterion, optimizer, device)
        te_loss, te_acc, te_preds, te_lbls = eval_fn(model, test_dl, criterion, device)
        te_f1 = f1_score(te_lbls, te_preds, average="macro", zero_division=0)
        scheduler.step()

        history.append({"epoch": epoch, "tr_loss": round(tr_loss, 4), "tr_acc": round(tr_acc, 4),
                         "te_loss": round(te_loss, 4), "te_acc": round(te_acc, 4), "te_f1": round(te_f1, 4)})
        print(f"{epoch:>4}  {tr_loss:>8.4f}  {tr_acc:>7.3f}  {te_loss:>8.4f}  {te_acc:>7.3f}  {te_f1:>6.3f}")

    # Fixed-epoch-count checkpoint -- no test-accuracy-driven selection (see
    # Shoulder Milling/residual_preprocessing_readme.md's "Why the Old Numbers
    # Were Misleading" #2: `if te_acc > best_acc: save` picks whichever epoch
    # happened to fit THIS test split best, which is itself test-set leakage
    # even though it looks like ordinary early stopping).
    best_acc, best_epoch = te_acc, args.epochs
    torch.save(model.state_dict(), out_dir / f"{tag}_best.pt")
    te_run_ids = run_ids_from_paths(te_p)
    if cascading:
        run_acc, vote_preds, vote_true = majority_vote_accuracy_cond(
            model, te_p, te_l, te_run_ids, [te_spd, te_doc], val_tf, device)
        soft_acc, soft_preds, soft_true = soft_vote_accuracy_cond(
            model, te_p, te_l, te_run_ids, [te_spd, te_doc], val_tf, device)
    else:
        run_acc, vote_preds, vote_true = majority_vote_accuracy(model, te_p, te_l, te_run_ids, val_tf, device)
        soft_acc, soft_preds, soft_true = soft_vote_accuracy(model, te_p, te_l, te_run_ids, val_tf, device)

    # Condition-prior probability stacking (additive, post-hoc metric only --
    # see cond_prior.py's docstring). feed_coarse/feed/roughness only
    # (COND_PARENTS identifies exactly the targets that are causally
    # downstream of the (DOC, speed) machining condition; speed/doc
    # themselves are the parents, nothing to stack). Wrapped in try/except
    # so a condition-prior edge case
    # can never break this training run's checkpoint/JSON emission.
    stack_acc, stack_acc_by_weight = None, None
    if args.target in COND_PARENTS:
        try:
            run_probs, run_true_map = run_prob_vectors(
                model, te_p, te_l, te_run_ids, val_tf, device,
                [te_spd, te_doc] if cascading else None)
            test_order = list(run_true_map)
            pixel_mat = np.stack([run_probs[r] for r in test_order])
            true_arr = np.array([run_true_map[r] for r in test_order])

            # Fit at WINDOW level (tr_p/tr_l, one row per training window),
            # not run level -- HistGradientBoostingClassifier's default
            # min_samples_leaf=20 can't split meaningfully on only ~33 RUN-
            # level rows and degenerates to predicting the single overall-
            # majority class for every test run (confirmed while building
            # stack_conditioning_32x3.py). Window-level repetition (each
            # run's condition repeated once per training window) gives it
            # enough rows.
            cond_of = cond_prior.conditions_for_runs(spec["label_map"], DOC_LABELS, SPEED_LABELS)
            tr_run_ids = run_ids_from_paths(tr_p)
            # tr_p/tr_l may include synthetic SMOTE runs (smote<target><i>_w{k})
            # when SMOTE is enabled -- those have no real (DOC,speed) condition
            # (not in spec["label_map"]/cond_of), so exclude them from the
            # condition-prior fit; only real runs carry a genuine condition.
            real_mask = [r in cond_of for r in tr_run_ids]
            tr_cond_list = [cond_of[r] for r, keep in zip(tr_run_ids, real_mask) if keep]
            tr_cond_labels = [lbl for lbl, keep in zip(tr_l, real_mask) if keep]
            clf, classes_ = cond_prior.fit_condition_prior(
                tr_cond_list, tr_cond_labels, spec["num_classes"])
            cond_mat = cond_prior.predict_condition_prior(
                clf, classes_, [cond_of[r] for r in test_order], spec["num_classes"])

            stack_acc_by_weight = {}
            for w in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0):
                stacked = cond_prior.stack_probs(cond_mat, pixel_mat, w)
                stack_acc_by_weight[str(w)] = round(float(np.mean(stacked.argmax(1) == true_arr)), 4)
            stack_acc = stack_acc_by_weight.get(str(args.cond_weight))
            if stack_acc is None:
                stacked = cond_prior.stack_probs(cond_mat, pixel_mat, args.cond_weight)
                stack_acc = round(float(np.mean(stacked.argmax(1) == true_arr)), 4)
            print(f"Run-level condition-prior-stacked acc (weight={args.cond_weight}): "
                  f"{stack_acc:.3f}  (sweep: {stack_acc_by_weight})")
        except Exception as e:
            print(f"  [cond-prior stacking] skipped due to error: {e}")

    print(f"\nBest window-level test acc : {best_acc:.3f}  (epoch {best_epoch})")
    print(f"Run-level majority vote acc: {run_acc:.3f}  "
          f"({int(round(run_acc * len(set(te_run_ids))))}/{len(set(te_run_ids))} runs)")
    print(f"Run-level soft (prob-avg) acc: {soft_acc:.3f}  "
          f"({int(round(soft_acc * len(set(te_run_ids))))}/{len(set(te_run_ids))} runs)")
    class_name_list = [spec["class_names"][c] for c in sorted(spec["class_names"])]
    print("\nPer-class report (run-level majority vote, best model):")
    print(classification_report(vote_true, vote_preds, target_names=class_name_list, zero_division=0))
    print("\nPer-class report (run-level soft/prob-avg, best model):")
    print(classification_report(soft_true, soft_preds, target_names=class_name_list, zero_division=0))

    hist_path = out_dir / f"{tag}_history.json"
    with open(hist_path, "w") as f:
        json.dump({
            "target": args.target, "img_dir": str(img_dir), "arch": args.arch,
            "epochs": args.epochs, "lr": args.lr,
            "smote": (not args.no_smote) and not cascading, "dropout": dropout,
            "label_smooth": args.label_smooth, "noise_std": args.noise_std,
            "ordinal_loss": args.ordinal_loss, "ordinal_alpha": args.ordinal_alpha,
            "run_tag": args.run_tag, "conditioned": args.conditioned,
            "cascade_predicted": args.cascade_predicted, "split": args.split,
            "best_window_acc": round(best_acc, 4), "best_epoch": best_epoch,
            "run_level_acc": round(run_acc, 4), "run_level_soft_acc": round(soft_acc, 4),
            "cond_weight": args.cond_weight, "run_level_stack_acc": stack_acc,
            "run_level_stack_acc_by_weight": stack_acc_by_weight,
            "history": history,
        }, f, indent=2)
    print(f"\nHistory saved to {hist_path}")


if __name__ == "__main__":
    main()
