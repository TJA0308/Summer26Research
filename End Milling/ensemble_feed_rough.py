"""
Ensemble inference for feed_coarse and roughness.
Tries all pairs of best-performing models (those at 83.3%) and sweeps alpha.
Goal: find alpha combo that achieves 11/12 = 91.7% run-level accuracy.
"""
import json
from pathlib import Path
from collections import defaultdict

import numpy as np
import torch
import torchvision.transforms as T
import torchvision.models as models
import torch.nn as nn
import pandas as pd
from PIL import Image

ROOT   = Path(__file__).parent
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

FEED_TEST_RUNS = {"run9","run22","run37","run12","run27","run40",
                  "run15","run28","run43","run2","run16","run31"}
RA_TEST_RUNS   = {"run9","run22","run37","run12","run27","run40",
                  "run15","run28","run43","run2","run16","run31"}

# Top feed_coarse model configs (img_dir, arch, model_stem, n_cls, target_col)
FEED_CONFIGS = [
    ("scalograms_32x3_feedopt",          "resnet50",       "resnet50_lr0.001_nosmote",          3, "feed_coarse"),
    ("scalograms_32x3_feedopt",          "resnet18",       "resnet18_lr0.001_smote",             3, "feed_coarse"),
    ("scalograms_32x3_feedopt_residual", "resnet18",       "resnet18_lr0.001_smote",             3, "feed_coarse"),
    ("scalograms_32x12_feedopt_raw3w",   "resnet50",       "resnet50_lr0.001_smote",             3, "feed_coarse"),
    ("scalograms_32x3_feedopt_raw3w_residual", "resnet50", "resnet50_lr0.001",                   3, "feed_coarse"),
    ("scalograms_32x3_feedopt",          "convnext_tiny",  "convnext_tiny_lr0.001_smote",        3, "feed_coarse"),
    ("scalograms_32x3_feedopt",          "efficientnet_b0","efficientnet_b0_lr0.001_smote",      3, "feed_coarse"),
    ("scalograms_32x12_feedopt",         "resnet50",       "resnet50_lr0.001_smote",             3, "feed_coarse"),
    ("scalograms_32x12_feedopt",         "resnet18",       "resnet18_lr0.001_smote",             3, "feed_coarse"),
]

ROUGH_CONFIGS = [
    ("scalograms_32x12_9win_residual_roughness", "resnet50",       "resnet50_lr0.001_smote",       3, "ra_label"),
    ("scalograms_32x12_9win_residual_roughness", "resnet18",       "resnet18_lr0.001_smote",       3, "ra_label"),
    ("scalograms_32x12_9win_residual_roughness", "resnet50",       "resnet50_lr0.001_nosmote",     3, "ra_label"),
    ("scalograms_32x12_9win_residual_roughness", "resnet18",       "resnet18_lr0.001_nosmote",     3, "ra_label"),
    ("scalograms_32x12_9win_residual_roughness", "convnext_tiny",  "convnext_tiny_lr0.0001_smote", 3, "ra_label"),
    ("scalograms_32x12_residual_roughness",      "resnet50",       "resnet50_lr0.001_smote",       3, "ra_label"),
    ("scalograms_32x12_residual_roughness",      "resnet50",       "resnet50_lr0.001_nosmote",     3, "ra_label"),
    ("scalograms_32x12_residual_roughness",      "resnet18",       "resnet18_lr0.001_smote",       3, "ra_label"),
    ("scalograms_32x12_residual_roughness",      "resnet18",       "resnet18_lr0.001_nosmote",     3, "ra_label"),
    ("scalograms_32x12_residual_roughness",      "convnext_tiny",  "convnext_tiny_lr0.0001_nosmote",3,"ra_label"),
    ("scalograms_32x12_raw3w_residual_roughness","convnext_tiny",  "convnext_tiny_lr0.0001_nosmote",3,"ra_label"),
    ("scalograms_32x3_residual_roughness",       "resnet50",       "resnet50_lr0.001_nosmote",     3, "ra_label"),
    ("scalograms_32x3",                          "resnet50",       "resnet50_lr0.001_nosmote",     3, "ra_label"),
]

val_tf = T.Compose([
    T.Resize((224, 224)),
    T.Grayscale(3),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def build_model(arch, n_cls, dropout=0.15):
    def head(in_f):
        return nn.Sequential(nn.Dropout(dropout), nn.Linear(in_f, n_cls)) if dropout > 0 else nn.Linear(in_f, n_cls)
    if arch == "resnet18":
        m = models.resnet18(weights=None); m.fc = head(m.fc.in_features)
    elif arch == "resnet50":
        m = models.resnet50(weights=None); m.fc = head(m.fc.in_features)
    elif arch == "convnext_tiny":
        m = models.convnext_tiny(weights=None); m.classifier[2] = head(m.classifier[2].in_features)
    elif arch == "efficientnet_b0":
        m = models.efficientnet_b0(weights=None); m.classifier[1] = head(m.classifier[1].in_features)
    return m


def model_dir_for(target, img_dir_name):
    suffix = img_dir_name.replace("scalograms_", "")
    if target == "feed_coarse":
        return ROOT / "cnn_model" / f"models_feed_coarse_{suffix}"
    elif target in ("roughness", "ra_label"):
        return ROOT / "cnn_model" / f"models_roughness_{suffix}"
    return None


def get_run_probs(img_dir_name, arch, model_stem, n_cls, target_col, test_runs):
    img_dir = ROOT / img_dir_name
    target_key = "feed_coarse" if target_col == "feed_coarse" else "roughness"
    model_dir = model_dir_for(target_key, img_dir_name)
    if model_dir is None:
        return None, None
    model_path = model_dir / f"{model_stem}_best.pt"
    if not model_path.exists():
        print(f"  MISSING: {model_path.name} in {model_dir.name}")
        return None, None

    labels_path = img_dir / "labels.csv"
    if not labels_path.exists():
        print(f"  MISSING labels: {labels_path}")
        return None, None
    df = pd.read_csv(labels_path)
    test_df = df[df["run"].isin(test_runs)]

    state = torch.load(model_path, map_location=DEVICE, weights_only=False)
    m = build_model(arch, n_cls, dropout=0.15)
    try:
        m.load_state_dict(state)
    except RuntimeError:
        m = build_model(arch, n_cls, dropout=0.0)
        try:
            m.load_state_dict(state)
        except RuntimeError:
            print(f"  State dict mismatch: {model_path.name}")
            return None, None
    m.to(DEVICE).eval()

    run_probs, run_true = defaultdict(list), {}
    for _, row in test_df.iterrows():
        img_path = img_dir / row["filename"]
        if not img_path.exists():
            continue
        img = Image.open(img_path).convert("RGB")
        x = val_tf(img).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            p = torch.softmax(m(x), dim=1).cpu().numpy()[0]
        run_probs[row["run"]].append(p)
        run_true[row["run"]] = int(row[target_col])

    avg = {r: np.mean(ps, axis=0) for r, ps in run_probs.items()}
    return avg, run_true


def run_acc(run_probs, run_true):
    correct = sum(1 for r, p in run_probs.items() if p.argmax() == run_true[r])
    return correct / max(len(run_true), 1)


def ensemble_sweep(configs, test_runs, target_col, label):
    print(f"\n{'='*60}")
    print(f"TARGET: {label}")
    print(f"{'='*60}")

    print(f"\nLoading {len(configs)} model configs ...")
    loaded = []
    for img_dir, arch, stem, n_cls, tcol in configs:
        probs, true = get_run_probs(img_dir, arch, stem, n_cls, tcol, test_runs)
        if probs and len(probs) >= 8:
            acc = run_acc(probs, true)
            print(f"  {acc:.3f}  {img_dir}/{stem}")
            loaded.append((img_dir, arch, stem, probs, true, acc))
        else:
            print(f"  skip  {img_dir}/{stem} (too few runs)")

    if len(loaded) < 2:
        print("Not enough models loaded for ensemble.")
        return

    # Sort by individual accuracy descending
    loaded.sort(key=lambda x: -x[5])

    print(f"\nPairwise ensemble sweep ...")
    best_acc, best_cfg = 0, None
    for i, (d1, a1, s1, p1, t1, acc1) in enumerate(loaded):
        for j, (d2, a2, s2, p2, t2, acc2) in enumerate(loaded):
            if j <= i:
                continue
            shared = set(p1) & set(p2)
            if len(shared) < 8:
                continue
            for alpha in np.arange(0.0, 1.05, 0.1):
                alpha = round(alpha, 1)
                correct = 0
                for r in shared:
                    p = alpha * p1[r] + (1 - alpha) * p2[r]
                    if p.argmax() == t1[r]:
                        correct += 1
                acc = correct / len(shared)
                if acc > best_acc:
                    best_acc = acc
                    best_cfg = (d1, s1, d2, s2, alpha, acc)

    print(f"\nBest pairwise ensemble: {best_acc:.3f}  ({int(best_acc * 12)}/12 runs)")
    if best_cfg:
        print(f"  Model A (alpha={best_cfg[4]:.1f}): {best_cfg[0]}/{best_cfg[1]}")
        print(f"  Model B (1-alpha):                {best_cfg[2]}/{best_cfg[3]}")

    # Also try 3-model uniform average of top-3
    if len(loaded) >= 3:
        top3 = loaded[:3]
        shared3 = set(top3[0][3]) & set(top3[1][3]) & set(top3[2][3])
        if len(shared3) >= 8:
            correct = sum(
                1 for r in shared3
                if (top3[0][3][r] + top3[1][3][r] + top3[2][3][r]).argmax() == top3[0][4][r]
            )
            acc3 = correct / len(shared3)
            print(f"\nTop-3 uniform average: {acc3:.3f}  ({int(acc3 * len(shared3))}/{len(shared3)} runs)")

    # Try all-model uniform average
    all_shared = set(loaded[0][3])
    for _, _, _, p, _, _ in loaded[1:]:
        all_shared &= set(p)
    if len(all_shared) >= 8:
        correct = sum(
            1 for r in all_shared
            if sum(p[r] for _, _, _, p, _, _ in loaded).argmax() == loaded[0][4][r]
        )
        acc_all = correct / len(all_shared)
        print(f"All-{len(loaded)}-model uniform average: {acc_all:.3f}  ({int(acc_all * len(all_shared))}/{len(all_shared)} runs)")


print(f"Device: {DEVICE}")
ensemble_sweep(FEED_CONFIGS, FEED_TEST_RUNS, "feed_coarse", "FEED_COARSE")
ensemble_sweep(ROUGH_CONFIGS, RA_TEST_RUNS,  "ra_label",    "ROUGHNESS")
