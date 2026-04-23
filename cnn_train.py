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

RUN_LABELS = {
    "run1": 0, "run2": 0, "run3": 0,
    "run4": 1, "run5": 1, "run6": 1,
    "run7": 2, "run8": 2, "run9": 2,
}
SPEED_NAMES = {0: "1500 rpm", 1: "2000 rpm", 2: "3000 rpm"}
TEST_RUNS   = {"run3", "run6", "run9"}


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


def load_split(img_dir):
    train_paths, train_labels = [], []
    test_paths,  test_labels  = [], []
    for png in sorted(img_dir.glob("*.png")):
        run = png.stem.split("_w")[0]
        if run not in RUN_LABELS:
            continue
        label = RUN_LABELS[run]
        if run in TEST_RUNS:
            test_paths.append(png);  test_labels.append(label)
        else:
            train_paths.append(png); train_labels.append(label)
    return (train_paths, train_labels), (test_paths, test_labels)


def build_transforms():
    mean = [0.485, 0.456, 0.406]
    std  = [0.229, 0.224, 0.225]
    train_tf = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    val_tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    return train_tf, val_tf


def build_model(num_classes, freeze_backbone=False):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    if freeze_backbone:
        for p in model.parameters():
            p.requires_grad = False
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


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
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", required=True)
    parser.add_argument("--epochs",  type=int,   default=20)
    parser.add_argument("--lr",      type=float, default=1e-3)
    parser.add_argument("--batch",   type=int,   default=16)
    parser.add_argument("--freeze",  action="store_true")
    args = parser.parse_args()

    seed_everything(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    img_dir = Path(args.img_dir)
    (tr_p, tr_l), (te_p, te_l) = load_split(img_dir)

    print(f"\nTrain: {len(tr_p)} images | Test: {len(te_p)} images")
    for c, name in SPEED_NAMES.items():
        print(f"  class {c} ({name}): {tr_l.count(c)} train / {te_l.count(c)} test")

    if not tr_p:
        print("No training images found. Run scalogram.py first.")
        return

    train_tf, val_tf = build_transforms()
    train_ds = ScalogramDataset(tr_p, tr_l, train_tf)
    test_ds  = ScalogramDataset(te_p, te_l, val_tf)
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True,  num_workers=0)
    test_dl  = DataLoader(test_ds,  batch_size=args.batch, shuffle=False, num_workers=0)

    model     = build_model(num_classes=3, freeze_backbone=args.freeze).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()), lr=args.lr
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    print(f"\nTraining ResNet18 for {args.epochs} epochs  (lr={args.lr})\n")
    print(f"{'Epoch':>5} {'Train Loss':>10} {'Train Acc':>10} {'Test Loss':>10} {'Test Acc':>10}")
    print("-" * 52)

    best_test_acc = 0.0
    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(model, train_dl, criterion, optimizer, device)
        te_loss, te_acc = eval_epoch(model, test_dl,  criterion, device)
        scheduler.step()
        if te_acc > best_test_acc:
            best_test_acc = te_acc
            torch.save(model.state_dict(), "best_model.pt")
        print(f"{epoch:>5} {tr_loss:>10.4f} {tr_acc:>10.3f} {te_loss:>10.4f} {te_acc:>10.3f}")

    print(f"\nBest test accuracy: {best_test_acc:.3f}")
    print("Model saved to best_model.pt")


if __name__ == "__main__":
    main()
