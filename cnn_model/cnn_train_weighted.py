"""
cnn_train_weighted.py

CNN training with weighted sampling
(SMOTE-style balancing for image datasets)

This keeps the original cnn_train.py untouched.
"""

import argparse
import random
from pathlib import Path

import numpy as np

import torch
import torch.nn as nn

from torch.utils.data import (
    DataLoader,
    Dataset,
    WeightedRandomSampler,
)

from torchvision import models, transforms

from PIL import Image


SEED = 42


# =========================================================
# LABELS
# =========================================================

SPEED_LABELS = {
    "run1": 3, "run2": 3, "run3": 3,
    "run4": 4, "run5": 4, "run6": 4,
    "run7": 0, "run8": 0, "run9": 0,
    "run10": 1, "run11": 1, "run12": 1,
    "run13": 2, "run14": 2, "run15": 2,
    "run16": 3, "run17": 3, "run18": 3,
    "run19": 4, "run20": 4, "run21": 4,
    "run22": 0, "run23": 0, "run24": 0,
    "run25": 1, "run26": 1, "run27": 1,
    "run28": 2, "run29": 2, "run30": 2,
    "run31": 3, "run32": 3, "run33": 3,
    "run34": 4, "run35": 4, "run36": 4,
    "run37": 0, "run38": 0, "run39": 0,
    "run40": 1, "run41": 1, "run42": 1,
    "run43": 2, "run44": 2, "run45": 2,
}

SPEED_NAMES = {
    0: "1500 rpm",
    1: "2000 rpm",
    2: "3000 rpm",
    3: "4000 rpm",
    4: "5000 rpm",
}

SPEED_TEST_RUNS = {
    "run24",
    "run27",
    "run30",
    "run33",
    "run36",
}


FEED_LABELS = {
    "run1": 0, "run2": 1, "run3": 2,
    "run4": 3, "run5": 4, "run6": 5,

    "run7": 0, "run8": 1, "run9": 2,
    "run10": 0, "run11": 1, "run12": 2,

    "run13": 1, "run14": 2, "run15": 3,
    "run16": 2, "run17": 3, "run18": 4,

    "run19": 3, "run20": 4, "run21": 5,

    "run22": 0, "run23": 1, "run24": 2,
    "run25": 0, "run26": 1, "run27": 2,

    "run28": 1, "run29": 2, "run30": 3,
    "run31": 2, "run32": 3, "run33": 4,

    "run34": 3, "run35": 4, "run36": 5,

    "run37": 0, "run38": 1, "run39": 2,
    "run40": 0, "run41": 1, "run42": 2,

    "run43": 1, "run44": 2, "run45": 3,
}

FEED_NAMES = {
    0: "3 mm/rev",
    1: "4 mm/rev",
    2: "5 mm/rev",
    3: "6 mm/rev",
    4: "7 mm/rev",
    5: "8 mm/rev",
}

FEED_TEST_RUNS = {
    "run25",
    "run13",
    "run31",
    "run17",
    "run5",
    "run36",
}


DOC_LABELS = {
    "run1": 0, "run2": 0, "run3": 0,
    "run4": 0, "run5": 0, "run6": 0,

    "run7": 1, "run8": 1, "run9": 1,
    "run10": 1, "run11": 1, "run12": 1,
    "run13": 1, "run14": 1, "run15": 1,
    "run16": 1, "run17": 1, "run18": 1,
    "run19": 1, "run20": 1, "run21": 1,

    "run22": 2, "run23": 2, "run24": 2,
    "run25": 2, "run26": 2, "run27": 2,
    "run28": 2, "run29": 2, "run30": 2,
    "run31": 2, "run32": 2, "run33": 2,
    "run34": 2, "run35": 2, "run36": 2,

    "run37": 0, "run38": 0, "run39": 0,
    "run40": 0, "run41": 0, "run42": 0,
    "run43": 0, "run44": 0, "run45": 0,
}

DOC_NAMES = {
    0: "0.015 mm",
    1: "0.03 mm",
    2: "0.06 mm",
}

DOC_TEST_RUNS = {
    "run1", "run5", "run43",
    "run7", "run14", "run19",
    "run22", "run29", "run36",
}


# =========================================================
# UTILITIES
# =========================================================

def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


class ScalogramDataset(Dataset):

    def __init__(self, paths, labels, transform=None):
        self.paths = paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, idx):

        img = Image.open(self.paths[idx]).convert("RGB")

        if self.transform:
            img = self.transform(img)

        return img, self.labels[idx]


def load_split(img_dir, label_map, test_runs):

    train_paths = []
    train_labels = []

    test_paths = []
    test_labels = []

    train_runs = set(label_map.keys()) - test_runs

    for png in sorted(img_dir.glob("*.png")):

        run = png.stem.split("_w")[0]

        label = label_map.get(run)

        if label is None:
            continue

        if run in test_runs:
            test_paths.append(png)
            test_labels.append(label)

        elif run in train_runs:
            train_paths.append(png)
            train_labels.append(label)

    return (
        (train_paths, train_labels),
        (test_paths, test_labels),
    )


def build_transforms():

    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]

    train_tf = transforms.Compose([
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(
            brightness=0.2,
            contrast=0.2
        ),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])

    val_tf = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])

    return train_tf, val_tf


def build_model(num_classes):

    model = models.resnet18(
        weights=models.ResNet18_Weights.DEFAULT
    )

    in_features = model.fc.in_features

    model.fc = nn.Linear(
        in_features,
        num_classes
    )

    return model


def train_epoch(model, loader, criterion, optimizer, device):

    model.train()

    total_loss = 0
    correct = 0
    n = 0

    for imgs, labels in loader:

        imgs = imgs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        out = model(imgs)

        loss = criterion(out, labels)

        loss.backward()

        optimizer.step()

        total_loss += loss.item() * len(labels)

        correct += (
            out.argmax(1) == labels
        ).sum().item()

        n += len(labels)

    return total_loss / n, correct / n


@torch.no_grad()
def eval_epoch(model, loader, criterion, device):

    model.eval()

    total_loss = 0
    correct = 0
    n = 0

    for imgs, labels in loader:

        imgs = imgs.to(device)
        labels = labels.to(device)

        out = model(imgs)

        loss = criterion(out, labels)

        total_loss += loss.item() * len(labels)

        correct += (
            out.argmax(1) == labels
        ).sum().item()

        n += len(labels)

    return total_loss / n, correct / n


# =========================================================
# MAIN
# =========================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--img_dir",
        required=True
    )

    parser.add_argument(
        "--target",
        default="feed",
        choices=["speed", "feed", "doc"]
    )

    parser.add_argument(
        "--epochs",
        type=int,
        default=30
    )

    parser.add_argument(
        "--batch",
        type=int,
        default=8
    )

    parser.add_argument(
        "--lr",
        type=float,
        default=1e-3
    )

    args = parser.parse_args()

    seed_everything(SEED)

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Device:", device)

    # -----------------------------------------------------
    # Select task
    # -----------------------------------------------------

    if args.target == "feed":

        label_map = FEED_LABELS
        class_names = FEED_NAMES
        test_runs = FEED_TEST_RUNS
        num_classes = 6

    elif args.target == "doc":

        label_map = DOC_LABELS
        class_names = DOC_NAMES
        test_runs = DOC_TEST_RUNS
        num_classes = 3

    else:

        label_map = SPEED_LABELS
        class_names = SPEED_NAMES
        test_runs = SPEED_TEST_RUNS
        num_classes = 5

    img_dir = Path(args.img_dir)

    (tr_p, tr_l), (te_p, te_l) = load_split(
        img_dir,
        label_map,
        test_runs
    )

    print(f"\nTarget: {args.target}")
    print(f"Train images: {len(tr_p)}")
    print(f"Test images : {len(te_p)}")

    train_tf, val_tf = build_transforms()

    train_ds = ScalogramDataset(
        tr_p,
        tr_l,
        train_tf
    )

    test_ds = ScalogramDataset(
        te_p,
        te_l,
        val_tf
    )

    # =====================================================
    # WEIGHTED SAMPLING
    # =====================================================

    class_counts = np.bincount(tr_l)

    print("\nClass counts:", class_counts)

    class_weights = 1.0 / class_counts

    sample_weights = [
        class_weights[label]
        for label in tr_l
    ]

    sampler = WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True
    )

    train_dl = DataLoader(
        train_ds,
        batch_size=args.batch,
        sampler=sampler,
        num_workers=0
    )

    test_dl = DataLoader(
        test_ds,
        batch_size=args.batch,
        shuffle=False,
        num_workers=0
    )

    # =====================================================
    # MODEL
    # =====================================================

    model = build_model(
        num_classes=num_classes
    ).to(device)

    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=args.lr,
        weight_decay=1e-4
    )

    # =====================================================
    # TRAINING
    # =====================================================

    best_test_acc = 0.0

    print(
        f"\n{'Epoch':>5} "
        f"{'Train Loss':>10} "
        f"{'Train Acc':>10} "
        f"{'Test Loss':>10} "
        f"{'Test Acc':>10}"
    )

    print("-" * 55)

    for epoch in range(1, args.epochs + 1):

        tr_loss, tr_acc = train_epoch(
            model,
            train_dl,
            criterion,
            optimizer,
            device
        )

        te_loss, te_acc = eval_epoch(
            model,
            test_dl,
            criterion,
            device
        )

        if te_acc > best_test_acc:
            best_test_acc = te_acc

        print(
            f"{epoch:>5} "
            f"{tr_loss:>10.4f} "
            f"{tr_acc:>10.3f} "
            f"{te_loss:>10.4f} "
            f"{te_acc:>10.3f}"
        )

    print(f"\nBest test accuracy: {best_test_acc:.3f}")


if __name__ == "__main__":
    main()