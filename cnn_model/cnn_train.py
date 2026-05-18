import argparse
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms
from PIL import Image

SEED = 42

# ── Speed prediction ──────────────────────────────────────────────────────
SPEED_LABELS = {
    "run1": 3,  "run2": 3,  "run3": 3,   # 4000 rpm  DOC=0.015
    "run4": 4,  "run5": 4,  "run6": 4,   # 5000 rpm  DOC=0.015
    "run7": 0,  "run8": 0,  "run9": 0,   # 1500 rpm  DOC=0.030
    "run10": 1, "run11": 1, "run12": 1,  # 2000 rpm  DOC=0.030
    "run13": 2, "run14": 2, "run15": 2,  # 3000 rpm  DOC=0.030
    "run16": 3, "run17": 3, "run18": 3,  # 4000 rpm  DOC=0.030
    "run19": 4, "run20": 4, "run21": 4,  # 5000 rpm  DOC=0.030
    "run22": 0, "run23": 0, "run24": 0,  # 1500 rpm  DOC=0.060
    "run25": 1, "run26": 1, "run27": 1,  # 2000 rpm  DOC=0.060
    "run28": 2, "run29": 2, "run30": 2,  # 3000 rpm  DOC=0.060
    "run31": 3, "run32": 3, "run33": 3,  # 4000 rpm  DOC=0.060
    "run34": 4, "run35": 4, "run36": 4,  # 5000 rpm  DOC=0.060
    "run37": 0, "run38": 0, "run39": 0,  # 1500 rpm  DOC=0.015
    "run40": 1, "run41": 1, "run42": 1,  # 2000 rpm  DOC=0.015
    "run43": 2, "run44": 2, "run45": 2,  # 3000 rpm  DOC=0.015
}
SPEED_NAMES = {0: "1500 rpm", 1: "2000 rpm", 2: "3000 rpm", 3: "4000 rpm", 4: "5000 rpm"}
SPEED_TEST_RUNS = {"run24", "run27", "run30", "run33", "run36"}  # 1 per class, DOC=0.060

# ── Feed rate prediction ──────────────────────────────────────────────────
# Actual feed values in mm/rev: 0=3, 1=4, 2=5, 3=6, 4=7, 5=8
FEED_LABELS = {
    "run1":  2,  "run2":  3,  "run3":  4,   # DOC=0.015, 4000rpm, feed=5,6,7
    "run4":  3,  "run5":  4,  "run6":  5,   # DOC=0.015, 5000rpm, feed=6,7,8
    "run7":  0,  "run8":  1,  "run9":  2,   # DOC=0.030, 1500rpm, feed=3,4,5
    "run10": 0,  "run11": 1,  "run12": 2,   # DOC=0.030, 2000rpm, feed=3,4,5
    "run13": 1,  "run14": 2,  "run15": 3,   # DOC=0.030, 3000rpm, feed=4,5,6
    "run16": 2,  "run17": 3,  "run18": 4,   # DOC=0.030, 4000rpm, feed=5,6,7
    "run19": 3,  "run20": 4,  "run21": 5,   # DOC=0.030, 5000rpm, feed=6,7,8
    "run22": 0,  "run23": 1,  "run24": 2,   # DOC=0.060, 1500rpm, feed=3,4,5
    "run25": 0,  "run26": 1,  "run27": 2,   # DOC=0.060, 2000rpm, feed=3,4,5
    "run28": 1,  "run29": 2,  "run30": 3,   # DOC=0.060, 3000rpm, feed=4,5,6
    "run31": 2,  "run32": 3,  "run33": 4,   # DOC=0.060, 4000rpm, feed=5,6,7
    "run34": 3,  "run35": 4,  "run36": 5,   # DOC=0.060, 5000rpm, feed=6,7,8
    "run37": 0,  "run38": 1,  "run39": 2,   # DOC=0.015, 1500rpm, feed=3,4,5
    "run40": 0,  "run41": 1,  "run42": 2,   # DOC=0.015, 2000rpm, feed=3,4,5
    "run43": 1,  "run44": 2,  "run45": 3,   # DOC=0.015, 3000rpm, feed=4,5,6
}
FEED_NAMES = {0: "3 mm/rev", 1: "4 mm/rev", 2: "5 mm/rev", 3: "6 mm/rev", 4: "7 mm/rev", 5: "8 mm/rev"}
# 1 test run per class, spread across diverse DOC/speed conditions: 6 test, 39 train
FEED_TEST_RUNS = {
    "run25",  # class 0 (3 mm/rev): DOC=0.060, 2000rpm
    "run13",  # class 1 (4 mm/rev): DOC=0.030, 3000rpm
    "run31",  # class 2 (5 mm/rev): DOC=0.060, 4000rpm
    "run17",  # class 3 (6 mm/rev): DOC=0.030, 4000rpm
    "run5",   # class 4 (7 mm/rev): DOC=0.015, 5000rpm
    "run36",  # class 5 (8 mm/rev): DOC=0.060, 5000rpm
}

# ── Coarsened feed rate (3-class: low/medium/high) ───────────────────────
# Groups: 0=low(3-4mm/rev), 1=medium(5-6mm/rev), 2=high(7-8mm/rev)
FEED_COARSE_LABELS = {k: v // 2 for k, v in FEED_LABELS.items()}
FEED_COARSE_NAMES  = {0: "3-4 mm/rev (low)", 1: "5-6 mm/rev (med)", 2: "7-8 mm/rev (high)"}
FEED_COARSE_TEST_RUNS = FEED_TEST_RUNS   # same test runs, labels remapped

# ── Depth-of-cut prediction ───────────────────────────────────────────────
DOC_LABELS = {
    "run1": 0,  "run2": 0,  "run3": 0,   # DOC=0.015
    "run4": 0,  "run5": 0,  "run6": 0,   # DOC=0.015
    "run7": 1,  "run8": 1,  "run9": 1,   # DOC=0.030
    "run10": 1, "run11": 1, "run12": 1,  # DOC=0.030
    "run13": 1, "run14": 1, "run15": 1,  # DOC=0.030
    "run16": 1, "run17": 1, "run18": 1,  # DOC=0.030
    "run19": 1, "run20": 1, "run21": 1,  # DOC=0.030
    "run22": 2, "run23": 2, "run24": 2,  # DOC=0.060
    "run25": 2, "run26": 2, "run27": 2,  # DOC=0.060
    "run28": 2, "run29": 2, "run30": 2,  # DOC=0.060
    "run31": 2, "run32": 2, "run33": 2,  # DOC=0.060
    "run34": 2, "run35": 2, "run36": 2,  # DOC=0.060
    "run37": 0, "run38": 0, "run39": 0,  # DOC=0.015
    "run40": 0, "run41": 0, "run42": 0,  # DOC=0.015
    "run43": 0, "run44": 0, "run45": 0,  # DOC=0.015
}
DOC_NAMES = {0: "0.015 mm", 1: "0.03 mm", 2: "0.06 mm"}
# 3 test per class from diverse speed combos: 9 test, 36 train
DOC_TEST_RUNS = {
    "run1",  "run5",  "run43",   # class 0 (0.015): 4000rpm, 5000rpm, 3000rpm
    "run7",  "run14", "run19",   # class 1 (0.030): 1500rpm, 3000rpm, 5000rpm
    "run22", "run29", "run36",   # class 2 (0.060): 1500rpm, 3000rpm, 5000rpm
}

# ── Surface roughness prediction (Ra μm) ─────────────────────────────────
# 0=Smooth (Ra<0.7), 1=Medium (0.7≤Ra≤1.0), 2=Rough (Ra>1.0)
RA_LABELS = {
    # DOC=0.015 — all smooth
    "run1": 0,  "run2": 0,  "run3": 0,    # Ra: 0.392, 0.282, 0.328
    "run4": 0,  "run5": 0,  "run6": 0,    # Ra: 0.302, 0.424, 0.448
    "run37": 0, "run38": 0, "run39": 0,   # Ra: 0.416, 0.302, 0.326
    "run40": 0, "run41": 0, "run42": 0,   # Ra: 0.328, 0.304, 0.454
    "run43": 0, "run44": 0, "run45": 0,   # Ra: 0.364, 0.314, 0.414
    # DOC=0.030 — mixed
    "run7": 1,  "run8": 1,  "run9": 0,    # Ra: 0.930, 0.852, 0.558
    "run10": 0, "run11": 1, "run12": 1,   # Ra: 0.640, 0.896, 0.902
    "run13": 0, "run14": 0, "run15": 0,   # Ra: 0.494, 0.418, 0.482
    "run16": 1, "run17": 0, "run18": 0,   # Ra: 0.834, 0.678, 0.384
    "run19": 1, "run20": 2, "run21": 2,   # Ra: 0.864, 1.048, 1.638
    # DOC=0.060 — mostly medium/rough
    "run22": 2, "run23": 1, "run24": 1,   # Ra: 1.186, 0.814, 0.726
    "run25": 0, "run26": 1, "run27": 1,   # Ra: 0.596, 0.838, 0.868
    "run28": 2, "run29": 2, "run30": 2,   # Ra: 1.340, 1.108, 1.010
    "run31": 1, "run32": 2, "run33": 2,   # Ra: 0.820, 1.612, 1.490
    "run34": 2, "run35": 2, "run36": 2,   # Ra: 2.084, 1.980, 1.790
}
RA_NAMES = {0: "Smooth (Ra<0.7)", 1: "Medium (0.7-1.0)", 2: "Rough (Ra>1.0)"}
# 2 test per class, spread across DOC/speed: 6 test, 39 train
RA_TEST_RUNS = {
    "run5",  "run43",   # Smooth: DOC=0.015 5000rpm, 3000rpm
    "run7",  "run27",   # Medium: DOC=0.030 1500rpm, DOC=0.060 2000rpm
    "run22", "run34",   # Rough:  DOC=0.060 1500rpm, 5000rpm
}

# Legacy aliases (used by load_split default path)
RUN_LABELS = SPEED_LABELS
TEST_RUNS  = SPEED_TEST_RUNS
TRAIN_RUNS = set(RUN_LABELS.keys()) - TEST_RUNS


def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class ScalogramDataset(Dataset):
    def __init__(self, paths, labels, transform=None):
        self.paths     = paths
        self.labels    = labels
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx]


class ConditionedScalogramDataset(Dataset):
    """Returns (image, feed_label, speed_label, doc_label) for cascade training."""
    def __init__(self, paths, labels, speed_labels, doc_labels, transform=None):
        self.paths        = paths
        self.labels       = labels
        self.speed_labels = speed_labels
        self.doc_labels   = doc_labels
        self.transform    = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):
        img = Image.open(self.paths[idx]).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, self.labels[idx], self.speed_labels[idx], self.doc_labels[idx]


def load_split_conditioned(img_dir, label_map, test_runs, speed_map, doc_map):
    """Like load_split but also returns per-image speed and DOC labels."""
    tr_p, tr_l, tr_spd, tr_doc = [], [], [], []
    te_p, te_l, te_spd, te_doc = [], [], [], []
    train_runs = set(label_map.keys()) - test_runs
    for png in sorted(img_dir.glob("*.png")):
        run   = png.stem.split("_w")[0]
        label = label_map.get(run)
        if label is None:
            continue
        spd = speed_map[run]
        doc = doc_map[run]
        if run in test_runs:
            te_p.append(png);  te_l.append(label);  te_spd.append(spd);  te_doc.append(doc)
        elif run in train_runs:
            tr_p.append(png);  tr_l.append(label);  tr_spd.append(spd);  tr_doc.append(doc)
    return (tr_p, tr_l, tr_spd, tr_doc), (te_p, te_l, te_spd, te_doc)


def load_smote_map(img_dir):
    """Return {run_stem: label} from smote_labels.csv if present, else {}."""
    smote_csv = Path(img_dir) / "smote_labels.csv"
    if not smote_csv.exists():
        return {}
    import csv as _csv
    with open(smote_csv) as f:
        return {row["run"]: int(row["label"]) for row in _csv.DictReader(f)}


def load_smote_cond_map(img_dir):
    """Return {run_stem: (label, speed, doc)} from smote_labels.csv if present, else {}."""
    smote_csv = Path(img_dir) / "smote_labels.csv"
    if not smote_csv.exists():
        return {}
    import csv as _csv
    result = {}
    with open(smote_csv) as f:
        for row in _csv.DictReader(f):
            if "speed" in row and "doc" in row:
                result[row["run"]] = (int(row["label"]), int(row["speed"]), int(row["doc"]))
    return result


def load_split(img_dir, label_map, test_runs, extra_label_map=None):
    combined_map = {**label_map, **(extra_label_map or {})}
    train_paths, train_labels = [], []
    test_paths,  test_labels  = [], []
    train_runs = set(combined_map.keys()) - test_runs
    for png in sorted(img_dir.glob("*.png")):
        run = png.stem.split("_w")[0]
        label = combined_map.get(run)
        if label is None:
            continue
        if run in test_runs:
            test_paths.append(png);  test_labels.append(label)
        elif run in train_runs:
            train_paths.append(png); train_labels.append(label)
    return (train_paths, train_labels), (test_paths, test_labels)


def build_transforms(augment):
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]

    if augment == "none":
        train_tf = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])
    elif augment == "light":
        train_tf = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])
    else:  # strong
        train_tf = transforms.Compose([
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(brightness=0.4, contrast=0.4, saturation=0.2),
            transforms.RandomRotation(5),
            transforms.GaussianBlur(kernel_size=3, sigma=(0.1, 1.0)),
            transforms.ToTensor(),
            transforms.Normalize(mean, std),
        ])

    val_tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    return train_tf, val_tf


class ConditionedResNet(nn.Module):
    """ResNet18 whose final head receives image features + speed one-hot + DOC one-hot."""
    NUM_SPEED = 5
    NUM_DOC   = 3

    def __init__(self, num_classes, dropout=0.0):
        super().__init__()
        base = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        feat_dim  = base.fc.in_features
        base.fc   = nn.Identity()
        self.backbone = base
        in_dim = feat_dim + self.NUM_SPEED + self.NUM_DOC
        self.head = (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_dim, num_classes))
                     if dropout > 0 else nn.Linear(in_dim, num_classes))

    def forward(self, img, speed_lbl, doc_lbl):
        feats    = self.backbone(img)
        speed_oh = F.one_hot(speed_lbl, num_classes=self.NUM_SPEED).float()
        doc_oh   = F.one_hot(doc_lbl,   num_classes=self.NUM_DOC).float()
        return self.head(torch.cat([feats, speed_oh, doc_oh], dim=1))


def train_epoch_cond(model, loader, criterion, optimizer, device):
    model.train()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels, speed, doc in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        speed, doc   = speed.to(device), doc.to(device)
        optimizer.zero_grad()
        out  = model(imgs, speed, doc)
        loss = criterion(out, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch_cond(model, loader, criterion, device):
    model.eval()
    total_loss, correct, n = 0.0, 0, 0
    for imgs, labels, speed, doc in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        speed, doc   = speed.to(device), doc.to(device)
        out  = model(imgs, speed, doc)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


def build_model(backbone, num_classes, freeze_backbone, dropout=0.0):
    if backbone == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        in_features = model.fc.in_features
        model.fc = (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_features, num_classes))
                    if dropout > 0 else nn.Linear(in_features, num_classes))
    elif backbone == "resnet50":
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        in_features = model.fc.in_features
        model.fc = (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_features, num_classes))
                    if dropout > 0 else nn.Linear(in_features, num_classes))
    elif backbone == "efficientnet_b0":
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        in_features = model.classifier[1].in_features
        model.classifier[1] = (nn.Sequential(nn.Dropout(dropout), nn.Linear(in_features, num_classes))
                                if dropout > 0 else nn.Linear(in_features, num_classes))
    else:
        raise ValueError(f"Unknown backbone: {backbone}")

    if freeze_backbone:
        for name, p in model.named_parameters():
            if "fc" not in name and "classifier" not in name:
                p.requires_grad = False

    return model


def build_scheduler(name, optimizer, epochs):
    if name == "cosine":
        return torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    elif name == "step":
        return torch.optim.lr_scheduler.StepLR(optimizer, step_size=max(1, epochs // 3), gamma=0.1)
    else:  # none
        return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda e: 1.0)


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
    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        out  = model(imgs)
        loss = criterion(out, labels)
        total_loss += loss.item() * len(labels)
        correct    += (out.argmax(1) == labels).sum().item()
        n          += len(labels)
    return total_loss / n, correct / n


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--img_dir",      required=True,            help="Folder of scalogram PNGs")
    parser.add_argument("--target",       default="speed",
                        choices=["speed", "feed", "feed_coarse", "doc", "roughness"],
                        help="Prediction target: speed (5 cls), feed (6 cls), feed_coarse (3 cls), doc (3 cls), roughness (3 cls)")
    parser.add_argument("--epochs",       type=int,   default=30,   help="Number of training epochs")
    parser.add_argument("--lr",           type=float, default=1e-3, help="Initial learning rate")
    parser.add_argument("--batch",        type=int,   default=8,    help="Batch size")
    parser.add_argument("--weight_decay", type=float, default=1e-4, help="L2 regularisation strength")
    parser.add_argument("--backbone",     default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0"],
                        help="Pretrained backbone architecture")
    parser.add_argument("--freeze",       action="store_true",
                        help="Freeze backbone weights, train classification head only")
    parser.add_argument("--augment",      default="light",
                        choices=["none", "light", "strong"],
                        help="Data augmentation strength applied to training images")
    parser.add_argument("--scheduler",    default="cosine",
                        choices=["cosine", "step", "none"],
                        help="Learning rate schedule")
    parser.add_argument("--save",         default="best_model.pt",  help="Path to save best model")
    parser.add_argument("--checkpoint",   default=None,             help="Load weights from this .pt file before training")
    parser.add_argument("--dropout",       type=float, default=0.0,  help="Dropout rate before the final classifier (0=off)")
    parser.add_argument("--weighted_loss", action="store_true",      help="Weight CE loss inversely by class frequency")
    parser.add_argument("--conditioned",   action="store_true",
                        help="Cascade mode: concatenate speed+DOC one-hot vectors with image features before classifying feed")
    args = parser.parse_args()

    seed_everything(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    if args.target == "feed":
        label_map   = FEED_LABELS
        class_names = FEED_NAMES
        test_runs   = FEED_TEST_RUNS
        num_classes = 6
        if args.save == "best_model.pt":
            args.save = "best_model_feed.pt"
    elif args.target == "feed_coarse":
        label_map   = FEED_COARSE_LABELS
        class_names = FEED_COARSE_NAMES
        test_runs   = FEED_COARSE_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_feed_coarse.pt"
    elif args.target == "doc":
        label_map   = DOC_LABELS
        class_names = DOC_NAMES
        test_runs   = DOC_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_doc.pt"
    elif args.target == "roughness":
        label_map   = RA_LABELS
        class_names = RA_NAMES
        test_runs   = RA_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_roughness.pt"
    else:
        label_map   = SPEED_LABELS
        class_names = SPEED_NAMES
        test_runs   = SPEED_TEST_RUNS
        num_classes = 5

    img_dir = Path(args.img_dir)

    if args.conditioned:
        if args.target not in ("feed", "feed_coarse"):
            print("--conditioned only applies to feed / feed_coarse targets")
            return
        if args.save == "best_model.pt":
            args.save = f"best_{args.target}_conditioned.pt"
        (tr_p, tr_l, tr_spd, tr_doc), (te_p, te_l, te_spd, te_doc) = \
            load_split_conditioned(img_dir, label_map, test_runs, SPEED_LABELS, DOC_LABELS)

        smote_cond = load_smote_cond_map(img_dir)
        if smote_cond:
            if args.target == "feed_coarse":
                smote_cond = {r: (lbl // 2, spd, doc) for r, (lbl, spd, doc) in smote_cond.items()}
            for run, (lbl, spd, doc) in smote_cond.items():
                for png in sorted(img_dir.glob(f"{run}_w*.png")):
                    tr_p.append(png); tr_l.append(lbl)
                    tr_spd.append(spd); tr_doc.append(doc)
            print(f"  SMOTE: {len(smote_cond)} synthetic runs loaded from smote_labels.csv")

        print(f"\nTarget: {args.target} [conditioned on speed+DOC]"
              f"  |  Train: {len(tr_p)} images | Test: {len(te_p)} images")
        for c, name in class_names.items():
            print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")
        if not tr_p:
            print("No training images found. Run scalogram.py first.")
            return

        print(f"\nConfig: ConditionedResNet  lr={args.lr}  wd={args.weight_decay}"
              f"  batch={args.batch}  epochs={args.epochs}"
              f"  augment={args.augment}  scheduler={args.scheduler}")

        train_tf, val_tf = build_transforms(args.augment)
        train_ds = ConditionedScalogramDataset(tr_p, tr_l, tr_spd, tr_doc, train_tf)
        test_ds  = ConditionedScalogramDataset(te_p, te_l, te_spd, te_doc, val_tf)
        train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
        test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

        model = ConditionedResNet(num_classes, dropout=args.dropout).to(device)
        if args.weighted_loss:
            counts  = np.bincount(tr_l, minlength=num_classes).astype(np.float32)
            weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
            weights = weights / weights.sum() * num_classes
            criterion = nn.CrossEntropyLoss(weight=weights)
            print(f"Class weights: {weights.cpu().numpy().round(3)}")
        else:
            criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
        scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

        print(f"\n{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} {'Test Loss':>10} {'Test Acc':>10}")
        print("-" * 52)

        best_test_acc = 0.0
        for epoch in range(1, args.epochs + 1):
            tr_loss, tr_acc = train_epoch_cond(model, train_dl, criterion, optimizer, device)
            te_loss, te_acc = eval_epoch_cond(model, test_dl,  criterion, device)
            scheduler.step()
            if te_acc > best_test_acc:
                best_test_acc = te_acc
                torch.save(model.state_dict(), args.save)
            print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}", flush=True)

        print(f"\nBest test accuracy: {best_test_acc:.3f}")
        print(f"Model saved to {args.save}")

        model.load_state_dict(torch.load(args.save, map_location=device))
        model.eval()
        all_preds, all_labels = [], []
        with torch.no_grad():
            for imgs, labels, speed, doc in test_dl:
                preds = model(imgs.to(device), speed.to(device), doc.to(device)).argmax(1).cpu().tolist()
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
        return

    smote_map = {}
    if args.target in ("feed", "feed_coarse"):
        smote_map = load_smote_map(img_dir)
        if smote_map:
            if args.target == "feed_coarse":
                smote_map = {run: lbl // 2 for run, lbl in smote_map.items()}
            print(f"  SMOTE: {len(smote_map)} synthetic runs loaded from smote_labels.csv")

    (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, label_map, test_runs, smote_map)

    print(f"\nTarget: {args.target}  |  Train: {len(tr_p)} images | Test: {len(te_p)} images")
    for c, name in class_names.items():
        print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")

    if not tr_p:
        print("No training images found. Run scalogram.py first.")
        return

    print(f"\nConfig: backbone={args.backbone}  lr={args.lr}  wd={args.weight_decay}"
          f"  batch={args.batch}  epochs={args.epochs}"
          f"  augment={args.augment}  scheduler={args.scheduler}  freeze={args.freeze}")

    train_tf, val_tf = build_transforms(args.augment)
    train_ds = ScalogramDataset(tr_p, tr_l, train_tf)
    test_ds  = ScalogramDataset(te_p, te_l, val_tf)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
    test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

    model = build_model(args.backbone, num_classes=num_classes, freeze_backbone=args.freeze, dropout=args.dropout).to(device)
    if args.checkpoint:
        model.load_state_dict(torch.load(args.checkpoint, map_location=device))
        print(f"Loaded checkpoint: {args.checkpoint}")
    if args.weighted_loss:
        counts = np.bincount(tr_l, minlength=num_classes).astype(np.float32)
        weights = torch.tensor(1.0 / np.maximum(counts, 1)).to(device)
        weights = weights / weights.sum() * num_classes
        criterion = nn.CrossEntropyLoss(weight=weights)
        print(f"Class weights: {weights.cpu().numpy().round(3)}")
    else:
        criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
    scheduler = build_scheduler(args.scheduler, optimizer, args.epochs)

    print(f"\n{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} {'Test Loss':>10} {'Test Acc':>10}")
    print("-" * 52)

    best_test_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(model, train_dl, criterion, optimizer, device)
        te_loss, te_acc = eval_epoch(model, test_dl,  criterion, device)
        scheduler.step()
        if te_acc > best_test_acc:
            best_test_acc = te_acc
            torch.save(model.state_dict(), args.save)
        print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}", flush=True)

    print(f"\nBest test accuracy: {best_test_acc:.3f}")
    print(f"Model saved to {args.save}")

    # Per-class breakdown using best saved model
    model.load_state_dict(torch.load(args.save, map_location=device))
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
            correct = sum(all_preds[i] == all_labels[i] for i in idx)
            wrong_as = [all_preds[i] for i in idx if all_preds[i] != all_labels[i]]
            detail = f"  predicted as {wrong_as}" if wrong_as else ""
            print(f"  class {c} ({name}): {correct}/{len(idx)}{detail}")


if __name__ == "__main__":
    main()
