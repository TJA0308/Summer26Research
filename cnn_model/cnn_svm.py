"""
Extract global-average-pool features from a frozen pretrained ResNet18,
then train a scikit-learn SVM classifier. Works well with very small datasets
where end-to-end fine-tuning overfits.
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

from cnn_train import (
    SPEED_LABELS, SPEED_NAMES, SPEED_TEST_RUNS,
    FEED_LABELS,  FEED_NAMES,  FEED_TEST_RUNS,
    FEED_COARSE_LABELS, FEED_COARSE_NAMES, FEED_COARSE_TEST_RUNS,
    DOC_LABELS,   DOC_NAMES,   DOC_TEST_RUNS,
    load_split,
)

VAL_TF = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def extract_features(paths, feature_extractor, device):
    feature_extractor.eval()
    feats = []
    with torch.no_grad():
        for p in paths:
            img = VAL_TF(Image.open(p).convert("RGB")).unsqueeze(0).to(device)
            feats.append(feature_extractor(img).squeeze().cpu().numpy())
    return np.stack(feats)


def build_feature_extractor(backbone, checkpoint, device):
    if backbone == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        model.fc = nn.Identity()
    elif backbone == "resnet50":
        model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        model.fc = nn.Identity()
    elif backbone == "efficientnet_b0":
        model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        model.classifier = nn.Identity()
    else:
        raise ValueError(f"Unknown backbone: {backbone}")

    if checkpoint:
        state = torch.load(checkpoint, map_location=device)
        compatible = {k: v for k, v in state.items()
                      if not k.startswith("fc.") and not k.startswith("classifier.")}
        model.load_state_dict(compatible, strict=False)
        print(f"Loaded backbone weights from {checkpoint} (head ignored)")

    for p in model.parameters():
        p.requires_grad = False

    return model.to(device)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir",    required=True)
    parser.add_argument("--target",     default="feed", choices=["speed", "feed", "doc"])
    parser.add_argument("--backbone",   default="resnet18",
                        choices=["resnet18", "resnet50", "efficientnet_b0"])
    parser.add_argument("--checkpoint", default=None,
                        help="Optional .pt with fine-tuned backbone weights")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if args.target == "feed":
        label_map, class_names, test_runs = FEED_LABELS, FEED_NAMES, FEED_TEST_RUNS
    elif args.target == "doc":
        label_map, class_names, test_runs = DOC_LABELS, DOC_NAMES, DOC_TEST_RUNS
    else:
        label_map, class_names, test_runs = SPEED_LABELS, SPEED_NAMES, SPEED_TEST_RUNS

    img_dir = Path(args.img_dir)
    (tr_p, tr_l), (te_p, te_l) = load_split(img_dir, label_map, test_runs)
    print(f"\nTarget: {args.target}  |  Train: {len(tr_p)}  Test: {len(te_p)}")

    extractor = build_feature_extractor(args.backbone, args.checkpoint, device)

    print("Extracting features …")
    X_train = extract_features(tr_p, extractor, device)
    X_test  = extract_features(te_p, extractor, device)
    y_train = np.array(tr_l)
    y_test  = np.array(te_l)

    print(f"Feature shape: {X_train.shape}")

    cv = min(5, min(np.bincount(y_train)))
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("svm",    SVC(class_weight="balanced")),
    ])
    param_grid = [
        {"svm__kernel": ["linear"], "svm__C": [0.001, 0.01, 0.1, 1.0, 10.0]},
        {"svm__kernel": ["rbf"],    "svm__C": [0.1, 1.0, 10.0], "svm__gamma": ["scale", "auto"]},
    ]
    gs = GridSearchCV(pipe, param_grid, cv=cv, scoring="accuracy", n_jobs=-1)
    gs.fit(X_train, y_train)

    best = gs.best_estimator_
    train_acc = best.score(X_train, y_train)
    test_acc  = best.score(X_test,  y_test)

    print(f"\nBest SVM params: {gs.best_params_}")
    print(f"Train accuracy : {train_acc:.3f}")
    print(f"Test  accuracy : {test_acc:.3f}")

    preds = best.predict(X_test)
    print("\nPer-class results:")
    for c, name in class_names.items():
        idx = [i for i, l in enumerate(te_l) if l == c]
        if idx:
            correct = sum(preds[i] == te_l[i] for i in idx)
            print(f"  class {c} ({name}): {correct}/{len(idx)}")


if __name__ == "__main__":
    main()
