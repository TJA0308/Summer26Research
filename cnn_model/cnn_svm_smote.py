"""
CNN feature extractor + SVM classifier + SMOTE experiment.

This file is separate from cnn_svm.py so the baseline pipeline
remains untouched.
"""

import argparse
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

from torchvision import models, transforms
from PIL import Image

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

from imblearn.over_sampling import SMOTE

from cnn_train import (
    SPEED_LABELS,
    SPEED_NAMES,
    SPEED_TEST_RUNS,

    FEED_LABELS,
    FEED_NAMES,
    FEED_TEST_RUNS,

    DOC_LABELS,
    DOC_NAMES,
    DOC_TEST_RUNS,

    load_split,
)

VAL_TF = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(
        [0.485, 0.456, 0.406],
        [0.229, 0.224, 0.225]
    ),
])


def extract_features(paths, feature_extractor, device):

    feature_extractor.eval()

    feats = []

    with torch.no_grad():

        for p in paths:

            img = VAL_TF(
                Image.open(p).convert("RGB")
            ).unsqueeze(0).to(device)

            feat = feature_extractor(img)

            feats.append(
                feat.squeeze().cpu().numpy()
            )

    return np.stack(feats)


def build_feature_extractor(backbone, checkpoint, device):

    if backbone == "resnet18":

        model = models.resnet18(
            weights=models.ResNet18_Weights.DEFAULT
        )

        model.fc = nn.Identity()

    elif backbone == "resnet50":

        model = models.resnet50(
            weights=models.ResNet50_Weights.DEFAULT
        )

        model.fc = nn.Identity()

    elif backbone == "efficientnet_b0":

        model = models.efficientnet_b0(
            weights=models.EfficientNet_B0_Weights.DEFAULT
        )

        model.classifier = nn.Identity()

    else:
        raise ValueError(f"Unknown backbone: {backbone}")

    if checkpoint:

        state = torch.load(
            checkpoint,
            map_location=device
        )

        compatible = {
            k: v for k, v in state.items()
            if not k.startswith("fc.")
            and not k.startswith("classifier.")
        }

        model.load_state_dict(
            compatible,
            strict=False
        )

        print(f"Loaded backbone weights from {checkpoint}")

    for p in model.parameters():
        p.requires_grad = False

    return model.to(device)


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
        "--backbone",
        default="resnet18",
        choices=["resnet18", "resnet50", "efficientnet_b0"]
    )

    parser.add_argument(
        "--checkpoint",
        default=None
    )

    args = parser.parse_args()

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    # ---------------------------------------------------------
    # Select task
    # ---------------------------------------------------------

    if args.target == "feed":

        label_map = FEED_LABELS
        class_names = FEED_NAMES
        test_runs = FEED_TEST_RUNS

    elif args.target == "doc":

        label_map = DOC_LABELS
        class_names = DOC_NAMES
        test_runs = DOC_TEST_RUNS

    else:

        label_map = SPEED_LABELS
        class_names = SPEED_NAMES
        test_runs = SPEED_TEST_RUNS

    # ---------------------------------------------------------
    # Load split
    # ---------------------------------------------------------

    img_dir = Path(args.img_dir)

    (tr_p, tr_l), (te_p, te_l) = load_split(
        img_dir,
        label_map,
        test_runs
    )

    print(f"\nTarget: {args.target}")
    print(f"Train images: {len(tr_p)}")
    print(f"Test images : {len(te_p)}")

    # ---------------------------------------------------------
    # Feature extractor
    # ---------------------------------------------------------

    extractor = build_feature_extractor(
        args.backbone,
        args.checkpoint,
        device
    )

    print("\nExtracting features...")

    X_train = extract_features(
        tr_p,
        extractor,
        device
    )

    X_test = extract_features(
        te_p,
        extractor,
        device
    )

    y_train = np.array(tr_l)
    y_test = np.array(te_l)

    print(f"Feature shape: {X_train.shape}")

    # ---------------------------------------------------------
    # SMOTE
    # ---------------------------------------------------------

    print("\nBefore SMOTE:", np.bincount(y_train))

    smote = SMOTE(
        random_state=42,
        k_neighbors=2
    )

    X_train, y_train = smote.fit_resample(
        X_train,
        y_train
    )

    print("After SMOTE :", np.bincount(y_train))

    # ---------------------------------------------------------
    # SVM
    # ---------------------------------------------------------

    cv = min(
        5,
        min(np.bincount(y_train))
    )

    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("svm", SVC(class_weight="balanced")),
    ])

    param_grid = [

        {
            "svm__kernel": ["linear"],
            "svm__C": [0.001, 0.01, 0.1, 1.0, 10.0]
        },

        {
            "svm__kernel": ["rbf"],
            "svm__C": [0.1, 1.0, 10.0],
            "svm__gamma": ["scale", "auto"]
        },
    ]

    gs = GridSearchCV(
        pipe,
        param_grid,
        cv=cv,
        scoring="accuracy",
        n_jobs=-1
    )

    print("\nTraining SVM...")

    gs.fit(X_train, y_train)

    best = gs.best_estimator_

    train_acc = best.score(X_train, y_train)
    test_acc = best.score(X_test, y_test)

    print(f"\nBest SVM params: {gs.best_params_}")

    print(f"Train accuracy : {train_acc:.3f}")
    print(f"Test  accuracy : {test_acc:.3f}")

    # ---------------------------------------------------------
    # Per-class results
    # ---------------------------------------------------------

    preds = best.predict(X_test)

    print("\nPer-class results:")

    for c, name in class_names.items():

        idx = [
            i for i, l in enumerate(te_l)
            if l == c
        ]

        if idx:

            correct = sum(
                preds[i] == te_l[i]
                for i in idx
            )

            print(
                f"  class {c} ({name}): "
                f"{correct}/{len(idx)}"
            )


if __name__ == "__main__":
    main()