import argparse
import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
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
# Within each (speed, DOC) group of 3 runs: 0=low, 1=medium, 2=high feed
FEED_LABELS = {
    "run1": 0,  "run2": 1,  "run3": 2,   # 4000/0.015  feeds 5,6,7
    "run4": 0,  "run5": 1,  "run6": 2,   # 5000/0.015  feeds 6,7,8
    "run7": 0,  "run8": 1,  "run9": 2,   # 1500/0.030  feeds 3,4,5
    "run10": 0, "run11": 1, "run12": 2,  # 2000/0.030  feeds 3,4,5
    "run13": 0, "run14": 1, "run15": 2,  # 3000/0.030  feeds 4,5,6
    "run16": 0, "run17": 1, "run18": 2,  # 4000/0.030  feeds 5,6,7
    "run19": 0, "run20": 1, "run21": 2,  # 5000/0.030  feeds 6,7,8
    "run22": 0, "run23": 1, "run24": 2,  # 1500/0.060  feeds 3,4,5
    "run25": 0, "run26": 1, "run27": 2,  # 2000/0.060  feeds 3,4,5
    "run28": 0, "run29": 1, "run30": 2,  # 3000/0.060  feeds 4,5,6
    "run31": 0, "run32": 1, "run33": 2,  # 4000/0.060  feeds 5,6,7
    "run34": 0, "run35": 1, "run36": 2,  # 5000/0.060  feeds 6,7,8
    "run37": 0, "run38": 1, "run39": 2,  # 1500/0.015  feeds 3,4,5
    "run40": 0, "run41": 1, "run42": 2,  # 2000/0.015  feeds 3,4,5
    "run43": 0, "run44": 1, "run45": 2,  # 3000/0.015  feeds 4,5,6
}
FEED_NAMES = {0: "low feed", 1: "medium feed", 2: "high feed"}
# 3 test per class from diverse speed/DOC combos: 9 test, 36 train
FEED_TEST_RUNS = {
    "run1",  "run22", "run43",   # class 0 (low):    4000/0.015, 1500/0.060, 3000/0.015
    "run2",  "run23", "run44",   # class 1 (medium): 4000/0.015, 1500/0.060, 3000/0.015
    "run3",  "run24", "run45",   # class 2 (high):   4000/0.015, 1500/0.060, 3000/0.015
}

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


def load_split(img_dir, label_map, test_runs):
    train_paths, train_labels = [], []
    test_paths,  test_labels  = [], []
    train_runs = set(label_map.keys()) - test_runs
    for png in sorted(img_dir.glob("*.png")):
        run = png.stem.split("_w")[0]
        label = label_map.get(run)
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


def build_model(backbone, num_classes, freeze_backbone):
    if backbone == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, num_classes)
    elif backbone == "resnet50":
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        in_features = model.fc.in_features
        model.fc = nn.Linear(in_features, num_classes)
    elif backbone == "efficientnet_b0":
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        in_features = model.classifier[1].in_features
        model.classifier[1] = nn.Linear(in_features, num_classes)
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
                        choices=["speed", "feed", "doc"],
                        help="Prediction target: speed (5 cls), feed rate (3 cls), or depth of cut (3 cls)")
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
    args = parser.parse_args()

    seed_everything(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    if args.target == "feed":
        label_map   = FEED_LABELS
        class_names = FEED_NAMES
        test_runs   = FEED_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_feed.pt"
    elif args.target == "doc":
        label_map   = DOC_LABELS
        class_names = DOC_NAMES
        test_runs   = DOC_TEST_RUNS
        num_classes = 3
        if args.save == "best_model.pt":
            args.save = "best_model_doc.pt"
    else:
        label_map   = SPEED_LABELS
        class_names = SPEED_NAMES
        test_runs   = SPEED_TEST_RUNS
        num_classes = 5

    img_dir = Path(args.img_dir)
    (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, label_map, test_runs)

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

    model     = build_model(args.backbone, num_classes=num_classes, freeze_backbone=args.freeze).to(device)
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
        print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}")

    print(f"\nBest test accuracy: {best_test_acc:.3f}")
    print(f"Model saved to {args.save}")


if __name__ == "__main__":
    main()
