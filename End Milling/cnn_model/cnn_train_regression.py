"""
Feed rate regression/ordinal training with MSE loss.
Supports feed (6-class, 0-5) and feed_coarse (3-class, 0-2).
Evaluated by MAE and within-1 accuracy.

Loss options:
  mse      -- standard MSE on scalar output
  wmse     -- inverse-frequency weighted MSE
  ordinal  -- cumulative threshold (CORN-style): predict K-1 binary
               thresholds P(y>0)...P(y>K-2), decode by summing sigmoids

Usage:
    python cnn_model/cnn_train_regression.py --img_dir scalograms_10w_residual_feed --kfold 5
    python cnn_model/cnn_train_regression.py --img_dir scalograms_10w_residual_feed --loss ordinal --kfold 5
    python cnn_model/cnn_train_regression.py --img_dir scalograms_10w_residual_feed --loss wmse --backbone convnext_tiny --epochs 80
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from cnn_train import (FEED_LABELS, FEED_NAMES,
                       FEED_COARSE_LABELS, FEED_COARSE_NAMES,
                       stratified_kfold, SEED)


def seed_everything(seed):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class PNGDataset(Dataset):
    def __init__(self, paths, labels, tf):
        self.paths, self.labels, self.tf = paths, labels, tf

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = self.tf(Image.open(self.paths[idx]).convert("RGB"))
        return img, torch.tensor(self.labels[idx], dtype=torch.float32)


def build_transforms(augment="light"):
    base = [transforms.Resize((224, 224)), transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]
    if augment == "light":
        train = [transforms.Resize((224, 224)),
                 transforms.RandomHorizontalFlip(),
                 transforms.ColorJitter(brightness=0.2, contrast=0.2),
                 transforms.ToTensor(),
                 transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])]
    else:
        train = base
    return transforms.Compose(train), transforms.Compose(base)


def build_model(backbone, num_outputs=1, freeze=False):
    """Return backbone with num_outputs head (1 for mse/wmse, K-1 for ordinal)."""
    def _head(in_f):
        return nn.Linear(in_f, num_outputs)

    if backbone == "resnet18":
        m = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        m.fc = _head(m.fc.in_features)
    elif backbone == "resnet50":
        m = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        m.fc = _head(m.fc.in_features)
    elif backbone == "efficientnet_b0":
        m = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        m.classifier[1] = _head(m.classifier[1].in_features)
    elif backbone == "convnext_tiny":
        m = models.convnext_tiny(weights=models.ConvNeXt_Tiny_Weights.DEFAULT)
        m.classifier[2] = _head(m.classifier[2].in_features)
    else:
        raise ValueError(f"Unsupported backbone: {backbone}")
    if freeze:
        for name, p in m.named_parameters():
            if not any(k in name for k in ("fc", "classifier")):
                p.requires_grad = False
    return m


def ordinal_encode(labels, num_classes):
    """Convert class indices to cumulative binary targets (K-1,)."""
    k = num_classes - 1
    targets = torch.zeros(len(labels), k)
    for i, lbl in enumerate(labels):
        targets[i, :int(lbl.item())] = 1.0
    return targets


def ordinal_decode(logits):
    """Sum sigmoid outputs to get soft class prediction in [0, K-1]."""
    return torch.sigmoid(logits).sum(dim=1)


def train_epoch(model, loader, optimizer, device, loss_type, class_weights, num_classes):
    model.train()
    total_loss, n = 0.0, 0
    for imgs, targets in loader:
        imgs, targets = imgs.to(device), targets.to(device)

        if loss_type == "ordinal":
            ot = ordinal_encode(targets, num_classes).to(device)
            logits = model(imgs)  # (B, K-1)
            loss = F.binary_cross_entropy_with_logits(logits, ot, reduction="mean")
        else:
            out = model(imgs).squeeze(1)
            if loss_type == "wmse" and class_weights is not None:
                w = class_weights[targets.long()]
                loss = (w * (out - targets) ** 2).mean()
            else:
                loss = F.mse_loss(out, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(targets)
        n += len(targets)
    return total_loss / n


@torch.no_grad()
def eval_epoch(model, loader, device, loss_type, num_classes):
    model.eval()
    abs_err, within1, n = 0.0, 0, 0
    preds_all, targets_all = [], []
    total_loss = 0.0
    for imgs, targets in loader:
        imgs, targets = imgs.to(device), targets.to(device)

        if loss_type == "ordinal":
            ot = ordinal_encode(targets, num_classes).to(device)
            logits = model(imgs)
            loss = F.binary_cross_entropy_with_logits(logits, ot, reduction="mean")
            out = ordinal_decode(logits)
        else:
            out = model(imgs).squeeze(1)
            loss = F.mse_loss(out, targets)

        total_loss += loss.item() * len(targets)
        rounded = out.round().clamp(0, num_classes - 1)
        abs_err += (out - targets).abs().sum().item()
        within1 += (rounded - targets).abs().le(1).sum().item()
        n += len(targets)
        preds_all.extend(out.cpu().tolist())
        targets_all.extend(targets.cpu().tolist())
    return total_loss / n, abs_err / n, within1 / n, preds_all, targets_all


def load_split(img_dir, label_map, test_runs):
    tr_p, tr_l, te_p, te_l = [], [], [], []
    train_runs = set(label_map.keys()) - test_runs
    for png in sorted(img_dir.glob("*.png")):
        run = png.stem.split("_w")[0]
        lbl = label_map.get(run)
        if lbl is None:
            continue
        if run in test_runs:
            te_p.append(png); te_l.append(lbl)
        elif run in train_runs:
            tr_p.append(png); tr_l.append(lbl)
    return (tr_p, tr_l), (te_p, te_l)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--img_dir",  required=True)
    parser.add_argument("--backbone", default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"])
    parser.add_argument("--epochs",   type=int,   default=40)
    parser.add_argument("--lr",       type=float, default=1e-3)
    parser.add_argument("--batch",    type=int,   default=16)
    parser.add_argument("--wd",       type=float, default=1e-4)
    parser.add_argument("--target",   default="feed", choices=["feed", "feed_coarse"])
    parser.add_argument("--kfold",    type=int,   default=5)
    parser.add_argument("--augment",  default="light", choices=["none", "light"])
    parser.add_argument("--freeze",   action="store_true")
    parser.add_argument("--loss",     default="mse", choices=["mse", "wmse", "ordinal"],
                        help="mse=standard, wmse=weighted MSE, ordinal=cumulative thresholds")
    parser.add_argument("--tag",      default="",
                        help="Extra tag appended to saved model filenames")
    args = parser.parse_args()

    seed_everything(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tag = f"_{args.tag}" if args.tag else f"_{args.loss}_{args.backbone}"
    print(f"Device: {device}")
    print(f"Config: backbone={args.backbone}  loss={args.loss}  lr={args.lr}  wd={args.wd}"
          f"  batch={args.batch}  epochs={args.epochs}  kfold={args.kfold}  tag={tag}")

    if args.target == "feed_coarse":
        label_map, class_names, num_classes = FEED_COARSE_LABELS, FEED_COARSE_NAMES, 3
    else:
        label_map, class_names, num_classes = FEED_LABELS, FEED_NAMES, 6

    num_outputs = 1 if args.loss != "ordinal" else (num_classes - 1)
    img_dir = Path(args.img_dir)
    train_tf, val_tf = build_transforms(args.augment)

    folds = stratified_kfold(label_map, k=args.kfold)
    fold_maes, fold_w1s = [], []

    for fi, (train_runs, test_runs) in enumerate(folds, 1):
        print(f"\n{'='*56}")
        print(f"Fold {fi}/{args.kfold}  train={len(train_runs)} runs  test={len(test_runs)} runs")

        (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, label_map, test_runs)
        if not tr_p:
            print("No training images, skipping."); continue

        for c, name in class_names.items():
            print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")

        # Class weights for wmse
        counts = np.bincount(tr_l, minlength=num_classes).astype(np.float32)
        weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
        weights = weights / weights.sum() * num_classes

        train_ds = PNGDataset(tr_p, tr_l, train_tf)
        test_ds  = PNGDataset(te_p, te_l, val_tf)
        train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
        test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

        model = build_model(args.backbone, num_outputs=num_outputs, freeze=args.freeze).to(device)
        optimizer = torch.optim.AdamW(
            filter(lambda p: p.requires_grad, model.parameters()),
            lr=args.lr, weight_decay=args.wd)
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

        print(f"\n{'Epoch':>5} {'Train Loss':>11} {'Test Loss':>10} {'MAE':>8} {'Within-1':>10}")
        print("-" * 52)

        best_mae = float("inf")
        best_w1  = 0.0
        best_preds, best_targets = [], []
        save_path = f"best_regression_{args.target}{tag}_fold{fi}.pt"

        for epoch in range(1, args.epochs + 1):
            tr_loss = train_epoch(model, train_dl, optimizer, device,
                                  args.loss, weights, num_classes)
            te_loss, mae, w1, preds, targets = eval_epoch(model, test_dl, device,
                                                           args.loss, num_classes)
            scheduler.step()
            if mae < best_mae:
                best_mae = mae
                best_w1  = w1
                best_preds, best_targets = preds, targets
                torch.save(model.state_dict(), save_path)
            print(f"{epoch:>5} {tr_loss:>11.4f} {te_loss:>10.4f} {mae:>8.3f} {w1:>10.3f}", flush=True)

        fold_maes.append(best_mae)
        fold_w1s.append(best_w1)
        print(f"\nFold {fi} best: MAE={best_mae:.3f}  Within-1={best_w1:.3f}  saved -> {save_path}")

        print(f"\nPer-class results (best MAE model, fold {fi}):")
        for c, name in class_names.items():
            idx = [i for i, t in enumerate(best_targets) if round(t) == c]
            if not idx:
                print(f"  class {c} ({name}): no test samples"); continue
            preds_c = [best_preds[i] for i in idx]
            mae_c   = np.mean([abs(p - c) for p in preds_c])
            exact   = sum(round(p) == c for p in preds_c)
            w1c     = sum(abs(round(p) - c) <= 1 for p in preds_c)
            print(f"  class {c} ({name}): exact={exact}/{len(idx)}  w1={w1c}/{len(idx)}"
                  f"  MAE={mae_c:.2f}  preds={[f'{p:.1f}' for p in preds_c[:8]]}")

    print(f"\n{'='*56}")
    print(f"K-fold ({args.kfold}) MAE:      {[f'{m:.3f}' for m in fold_maes]}")
    print(f"K-fold ({args.kfold}) Within-1: {[f'{w:.3f}' for w in fold_w1s]}")
    if fold_maes:
        print(f"Mean MAE:      {np.mean(fold_maes):.3f} ± {np.std(fold_maes):.3f}")
        print(f"Mean Within-1: {np.mean(fold_w1s):.3f} ± {np.std(fold_w1s):.3f}")


if __name__ == "__main__":
    main()
