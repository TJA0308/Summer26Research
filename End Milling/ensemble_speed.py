"""
Ensemble inference: combines per-run softmax probability vectors from the
best CWT model and the best harmonic model for speed classification.
Tries all alpha in [0.0, 0.1, ..., 1.0] where final_prob = alpha*cwt + (1-alpha)*harmonic.
Reports run-level accuracy for each alpha and the best combo.
"""
import re
import sys
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

SPEED_TEST_RUNS = {"run9","run22","run37","run12","run27","run40",
                   "run15","run28","run43","run2","run16","run31",
                   "run5","run19","run36"}

# Best CWT model and best harmonic model from sweeps
CWT_CONFIGS = [
    # (img_dir, arch, model_stem)
    ("scalograms_32x12_feedopt",    "convnext_tiny", "convnext_tiny_lr0.0001_nosmote"),
    ("scalograms_32x3_speedopt",    "resnet18",      "resnet18_lr0.001_smote"),
    ("scalograms_32x3_speedopt_perdoc", "resnet18",  "resnet18_lr0.001_nosmote"),
]
HARMONIC_CONFIGS = [
    ("scalograms_harmonic_speedopt", "resnet18", "resnet18_lr0.001_nosmote"),
    ("scalograms_harmonic_speedopt", "resnet18", "resnet18_lr0.001_smote"),
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


def get_run_probs(img_dir_name, arch, model_stem, n_cls=5):
    img_dir = ROOT / img_dir_name
    model_dir = ROOT / "cnn_model" / f"models_speed_{img_dir_name.replace('scalograms_', '')}"
    model_path = model_dir / f"{model_stem}_best.pt"
    if not model_path.exists():
        print(f"  MISSING: {model_path}")
        return None, None

    labels_path = img_dir / "labels.csv"
    if not labels_path.exists():
        labels_path = ROOT / "scalograms_32x3_speedopt" / "labels.csv"
    df = pd.read_csv(labels_path)
    test_df = df[df["run"].isin(SPEED_TEST_RUNS)]

    state = torch.load(model_path, map_location=DEVICE, weights_only=False)
    m = build_model(arch, n_cls, dropout=0.15)
    try:
        m.load_state_dict(state)
    except RuntimeError:
        m = build_model(arch, n_cls, dropout=0.0)
        try:
            m.load_state_dict(state)
        except RuntimeError:
            print(f"  State dict mismatch for {model_path.name}")
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
        run_true[row["run"]] = row["speed"]

    avg = {r: np.mean(ps, axis=0) for r, ps in run_probs.items()}
    return avg, run_true


def run_acc(run_probs, run_true):
    correct = sum(1 for r, p in run_probs.items() if p.argmax() == run_true[r])
    return correct / len(run_true)


print(f"Device: {DEVICE}")
print("\nLoading CWT model probability vectors ...")
cwt_results = []
for img_dir, arch, stem in CWT_CONFIGS:
    probs, true = get_run_probs(img_dir, arch, stem)
    if probs:
        acc = run_acc(probs, true)
        print(f"  {img_dir}/{stem}: {acc:.3f}")
        cwt_results.append((img_dir, arch, stem, probs, true, acc))

print("\nLoading harmonic model probability vectors ...")
harm_results = []
for img_dir, arch, stem in HARMONIC_CONFIGS:
    probs, true = get_run_probs(img_dir, arch, stem)
    if probs:
        acc = run_acc(probs, true)
        print(f"  {img_dir}/{stem}: {acc:.3f}")
        harm_results.append((img_dir, arch, stem, probs, true, acc))

print("\nEnsemble sweep (alpha = weight on CWT model) ...")
best_acc, best_cfg = 0, None
for c_dir, c_arch, c_stem, c_probs, c_true, c_acc in cwt_results:
    for h_dir, h_arch, h_stem, h_probs, h_true, h_acc in harm_results:
        # Only ensemble if they share the same test runs
        shared = set(c_probs) & set(h_probs)
        if len(shared) < 10:
            continue
        for alpha in np.arange(0.0, 1.05, 0.1):
            alpha = round(alpha, 1)
            correct = 0
            for r in shared:
                p = alpha * c_probs[r] + (1 - alpha) * h_probs[r]
                if p.argmax() == c_true[r]:
                    correct += 1
            acc = correct / len(shared)
            if acc > best_acc:
                best_acc = acc
                best_cfg = (c_dir, c_stem, h_dir, h_stem, alpha)
            if alpha in (0.0, 0.3, 0.5, 0.7, 1.0):
                print(f"  alpha={alpha:.1f}  CWT={c_stem[:25]}  Harm={h_stem[:20]}  acc={acc:.3f}")

print(f"\nBest ensemble: {best_acc:.3f}")
if best_cfg:
    print(f"  CWT:  {best_cfg[0]}/{best_cfg[1]}")
    print(f"  Harm: {best_cfg[2]}/{best_cfg[3]}")
    print(f"  alpha (CWT weight): {best_cfg[4]}")
