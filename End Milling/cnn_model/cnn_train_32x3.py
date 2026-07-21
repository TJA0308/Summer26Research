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
    roughness    -- 3-class: Smooth(<0.7) / Medium(0.7-1.0) / Rough(>1.0) Ra um

Scalogram folder (--img_dir, relative to the repo root, one level up from
this file):
    scalograms_32x3                  (roughness-tuned scale selection)
    scalograms_32x3_feedopt          (feed_coarse-tuned scale selection)
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
  --conditioned          feed_coarse only. Conditions on GROUND-TRUTH speed +
                         doc labels (a shortcut -- the model is told the real
                         answer for the parent tasks). Useful as an upper
                         bound / sanity check.
  --cascade_predicted    feed_coarse only. Conditions on PREDICTED speed + doc
                         labels from speed_pred_<scalo_tag>[...].csv and
                         doc_pred_<scalo_tag>[...].csv, written by
                         ../predict_conditioning_32x3.py after training and
                         selecting best speed/doc models. This is the
                         leakage-honest cascade -- the analogue of Shoulder
                         Milling's cnn_train_param.py auto-conditioning via
                         COND_PARENTS/predict_conditioning.py. SMOTE is
                         skipped in this mode (synthetic runs have no real
                         upstream speed/doc prediction to attach).
  Only one of --conditioned / --cascade_predicted may be set.

Usage examples:
    python cnn_train_32x3.py --target roughness --img_dir ../scalograms_32x3 --arch resnet18 --lr 1e-3
    python cnn_train_32x3.py --target feed_coarse --img_dir ../scalograms_32x3_feedopt --arch convnext_tiny --conditioned
    python cnn_train_32x3.py --target feed_coarse --img_dir ../scalograms_32x3_feedopt --cascade_predicted
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

from cnn_train import (   # noqa: E402  (repo-local import, path set above)
    SPEED_LABELS, SPEED_NAMES, SPEED_TEST_RUNS, SPEED_TEST_RUNS_BALANCED,
    DOC_LABELS, DOC_NAMES, DOC_TEST_RUNS, DOC_TEST_RUNS_12,
    FEED_COARSE_LABELS, FEED_COARSE_NAMES, FEED_COARSE_TEST_RUNS, FEED_COARSE_TEST_RUNS_12,
    RA_LABELS, RA_NAMES, RA_TEST_RUNS, RA_TEST_RUNS_12,
    ScalogramDataset, ConditionedScalogramDataset,
    load_split, load_split_conditioned, load_smote_map, load_smote_cond_map,
)

SEED = 42
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

TARGETS = {
    "speed": {
        "num_classes": 5, "class_names": SPEED_NAMES,
        "label_map": SPEED_LABELS,
        "test_runs_standard": SPEED_TEST_RUNS, "test_runs_balanced": SPEED_TEST_RUNS_BALANCED,
        "smote_csv": "smote_speed_labels.csv",
    },
    "doc": {
        "num_classes": 3, "class_names": DOC_NAMES,
        "label_map": DOC_LABELS,
        "test_runs_standard": DOC_TEST_RUNS, "test_runs_balanced": DOC_TEST_RUNS_12,
        "smote_csv": "smote_doc_labels.csv",
    },
    "feed_coarse": {
        "num_classes": 3, "class_names": FEED_COARSE_NAMES,
        "label_map": FEED_COARSE_LABELS,
        "test_runs_standard": FEED_COARSE_TEST_RUNS, "test_runs_balanced": FEED_COARSE_TEST_RUNS_12,
        "smote_csv": "smote_feed_coarse_labels.csv",
    },
    "roughness": {
        "num_classes": 3, "class_names": RA_NAMES,
        "label_map": RA_LABELS,
        "test_runs_standard": RA_TEST_RUNS, "test_runs_balanced": RA_TEST_RUNS_12,
        "smote_csv": "smote_roughness_labels.csv",
    },
}

# Carried over from Shoulder Milling's DEFAULT_DROPOUT finding (speed doesn't
# overfit, others do) as an initial guess for this new feature set -- not yet
# separately validated here.
DEFAULT_DROPOUT = {"speed": 0.0, "doc": 0.15, "feed_coarse": 0.15, "roughness": 0.15}

# End Milling's cascade shape is fixed: feed_coarse conditions jointly on
# BOTH speed and doc (never a subset) -- see cnn_train.py's ConditionedResNet.
COND_PARENTS = {"feed_coarse": ["speed", "doc"]}
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


def run_ids_from_paths(paths):
    return [Path(p).stem.split("_w")[0] for p in paths]


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
    parser.add_argument("--split", default="standard", choices=["standard", "balanced"],
                        help="Which *_TEST_RUNS set from cnn_train.py to use")
    parser.add_argument("--conditioned", action="store_true",
                        help="feed_coarse only: condition on GROUND-TRUTH speed+doc")
    parser.add_argument("--cascade_predicted", action="store_true",
                        help="feed_coarse only: condition on PREDICTED speed+doc "
                             "(run predict_conditioning_32x3.py for both first)")
    args = parser.parse_args()

    if args.conditioned and args.cascade_predicted:
        raise SystemExit("Pass only one of --conditioned / --cascade_predicted")
    if (args.conditioned or args.cascade_predicted) and args.target != "feed_coarse":
        raise SystemExit("--conditioned / --cascade_predicted only apply to --target feed_coarse")

    dropout = args.dropout if args.dropout is not None else DEFAULT_DROPOUT[args.target]
    seed_everything(SEED)

    img_dir = Path(args.img_dir)
    scalo_tag = img_dir.name.replace("scalograms_", "")
    out_dir = HERE / f"models_{args.target}_{scalo_tag}"
    out_dir.mkdir(exist_ok=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    spec = TARGETS[args.target]
    test_runs = spec["test_runs_balanced"] if args.split == "balanced" else spec["test_runs_standard"]
    print(f"Device    : {device}")
    print(f"Target    : {args.target}  ({spec['num_classes']} classes)")
    print(f"Img dir   : {img_dir}")
    print(f"Arch      : {args.arch}   LR: {args.lr}   Dropout: {dropout}   Split: {args.split}")

    train_tf, val_tf = build_transforms(args.noise_std)

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

    criterion = nn.CrossEntropyLoss(weight=weights, label_smoothing=args.label_smooth)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    tag = f"{args.arch}_lr{args.lr:g}"
    if args.run_tag:
        tag += f"_{args.run_tag}"
    best_acc, best_epoch, history = 0.0, 0, []

    print(f"\n{'Ep':>4}  {'TrLoss':>8}  {'TrAcc':>7}  {'TeLoss':>8}  {'TeAcc':>7}  {'TeF1':>6}")
    print("-" * 50)
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_fn(model, train_dl, criterion, optimizer, device)
        te_loss, te_acc, te_preds, te_lbls = eval_fn(model, test_dl, criterion, device)
        te_f1 = f1_score(te_lbls, te_preds, average="macro", zero_division=0)
        scheduler.step()

        if te_acc > best_acc:
            best_acc, best_epoch = te_acc, epoch
            torch.save(model.state_dict(), out_dir / f"{tag}_best.pt")

        history.append({"epoch": epoch, "tr_loss": round(tr_loss, 4), "tr_acc": round(tr_acc, 4),
                         "te_loss": round(te_loss, 4), "te_acc": round(te_acc, 4), "te_f1": round(te_f1, 4)})
        print(f"{epoch:>4}  {tr_loss:>8.4f}  {tr_acc:>7.3f}  {te_loss:>8.4f}  {te_acc:>7.3f}  {te_f1:>6.3f}")

    model.load_state_dict(torch.load(out_dir / f"{tag}_best.pt", map_location=device, weights_only=True))
    te_run_ids = run_ids_from_paths(te_p)
    if cascading:
        run_acc, vote_preds, vote_true = majority_vote_accuracy_cond(
            model, te_p, te_l, te_run_ids, [te_spd, te_doc], val_tf, device)
    else:
        run_acc, vote_preds, vote_true = majority_vote_accuracy(model, te_p, te_l, te_run_ids, val_tf, device)

    print(f"\nBest window-level test acc : {best_acc:.3f}  (epoch {best_epoch})")
    print(f"Run-level majority vote acc: {run_acc:.3f}  "
          f"({int(round(run_acc * len(set(te_run_ids))))}/{len(set(te_run_ids))} runs)")
    class_name_list = [spec["class_names"][c] for c in sorted(spec["class_names"])]
    print("\nPer-class report (run-level, best model):")
    print(classification_report(vote_true, vote_preds, target_names=class_name_list, zero_division=0))

    hist_path = out_dir / f"{tag}_history.json"
    with open(hist_path, "w") as f:
        json.dump({
            "target": args.target, "img_dir": str(img_dir), "arch": args.arch,
            "epochs": args.epochs, "lr": args.lr,
            "smote": (not args.no_smote) and not cascading, "dropout": dropout,
            "label_smooth": args.label_smooth, "noise_std": args.noise_std,
            "run_tag": args.run_tag, "conditioned": args.conditioned,
            "cascade_predicted": args.cascade_predicted, "split": args.split,
            "best_window_acc": round(best_acc, 4), "best_epoch": best_epoch,
            "run_level_acc": round(run_acc, 4), "history": history,
        }, f, indent=2)
    print(f"\nHistory saved to {hist_path}")


if __name__ == "__main__":
    main()
