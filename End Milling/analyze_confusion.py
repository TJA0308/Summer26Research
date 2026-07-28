"""
Re-run best models and print per-class confusion matrices and run-level breakdown.
"""
import torch
import numpy as np
import pandas as pd
from pathlib import Path
from collections import defaultdict, Counter
import torchvision.transforms as T
import torchvision.models as models
from PIL import Image
import sys

ROOT = Path(__file__).parent
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CONFIGS = [
    # (target, img_dir, arch, lr_str, model_filename_stem)
    ("speed",       "scalograms_32x12_feedopt",               "convnext_tiny", "0.0001", "convnext_tiny_lr0.0001"),
    ("speed",       "scalograms_32x3_speedopt",               "resnet18",      "0.001",  "resnet18_lr0.001_smote"),
    ("feed_coarse", "scalograms_32x3_feedopt_residual",       "resnet18",      "0.001",  "resnet18_lr0.001_nosmote"),
    ("feed_coarse", "scalograms_32x3_feedopt_residual",       "resnet50",      "0.001",  "resnet50_lr0.001_nosmote"),
    ("roughness",   "scalograms_32x12_residual_roughness",    "resnet50",      "0.001",  "resnet50_lr0.001_nosmote"),
    ("roughness",   "scalograms_32x12",                       "convnext_tiny", "0.001",  "convnext_tiny_lr0.001_nosmote"),
]

TARGET_COL = {
    "speed": "speed", "doc": "doc",
    "feed_coarse": "feed_coarse", "roughness": "ra_class", "feed": "feed"
}

def build_model(arch, n_cls):
    if arch == "resnet18":
        m = models.resnet18(weights=None); m.fc = torch.nn.Linear(512, n_cls)
    elif arch == "resnet50":
        m = models.resnet50(weights=None); m.fc = torch.nn.Linear(2048, n_cls)
    elif arch == "efficientnet_b0":
        m = models.efficientnet_b0(weights=None)
        m.classifier[1] = torch.nn.Linear(m.classifier[1].in_features, n_cls)
    elif arch == "convnext_tiny":
        m = models.convnext_tiny(weights=None)
        m.classifier[2] = torch.nn.Linear(m.classifier[2].in_features, n_cls)
    return m

transform = T.Compose([
    T.Resize((224, 224)),
    T.Grayscale(3),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

def run_inference(target, img_dir, arch, lr_str, model_stem):
    print(f"\n{'='*70}")
    print(f"TARGET={target}  DIR={img_dir}")
    print(f"ARCH={arch}  MODEL={model_stem}_best.pt")

    img_dir_short = img_dir.replace("scalograms_", "")
    model_dir = ROOT / "cnn_model" / f"models_{target}_{img_dir_short}"
    model_path = model_dir / f"{model_stem}_best.pt"
    if not model_path.exists():
        print(f"  NOT FOUND: {model_path}")
        return

    # Residual dirs inherit labels from their parent
    labels_path = ROOT / img_dir / "labels.csv"
    if not labels_path.exists():
        # Try stripping residual/raw suffix to find parent labels
        parent = img_dir
        for suffix in ["_residual", "_residual_roughness", "_residual_feed", "_raw3w_residual", "_raw9w_residual"]:
            if parent.endswith(suffix):
                parent = parent[:-len(suffix)]
                break
        labels_path = ROOT / parent / "labels.csv"
    labels_df = pd.read_csv(labels_path)
    col = TARGET_COL[target]

    TEST_RUNS_MAP = {
        "speed":       {"run9","run22","run37","run12","run27","run40",
                        "run15","run28","run43","run2","run16","run31",
                        "run5","run19","run36"},
        "feed_coarse": {"run25","run13","run7","run37",
                        "run31","run17","run9","run45",
                        "run5","run36","run3","run21"},
        "roughness":   {"run5","run43","run38","run40",
                        "run7","run27","run11","run19",
                        "run22","run34","run28","run32"},
        "doc":         {"run1","run5","run38","run41",
                        "run7","run14","run16","run19",
                        "run22","run25","run29","run36"},
        "feed":        {"run40","run28","run1","run17","run35","run6"},
    }
    test_runs = TEST_RUNS_MAP[target]
    test_df = labels_df[labels_df["run"].isin(test_runs)].copy()

    classes = sorted(test_df[col].unique())
    n_cls = len(classes)

    state = torch.load(model_path, map_location=DEVICE, weights_only=False)
    # Try standard model first, fall back to dropout variant
    m = build_model(arch, n_cls)
    try:
        m.load_state_dict(state)
    except RuntimeError:
        # Dropout wrapper: fc = Sequential(Dropout, Linear)
        import torch.nn as nn
        if arch in ("resnet18", "resnet50"):
            in_f = m.fc.in_features
            m.fc = nn.Sequential(nn.Dropout(0.15), nn.Linear(in_f, n_cls))
        elif arch == "efficientnet_b0":
            in_f = m.classifier[1].in_features
            m.classifier[1] = nn.Sequential(nn.Dropout(0.15), nn.Linear(in_f, n_cls))
        elif arch == "convnext_tiny":
            in_f = m.classifier[2].in_features
            m.classifier[2] = nn.Sequential(nn.Dropout(0.15), nn.Linear(in_f, n_cls))
        m.load_state_dict(state)
    m.to(DEVICE).eval()

    img_root = ROOT / img_dir
    run_probs = defaultdict(list)
    run_true = {}

    for _, row in test_df.iterrows():
        img_path = img_root / row["filename"]
        if not img_path.exists():
            continue
        img = Image.open(img_path)
        x = transform(img).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            probs = torch.softmax(m(x), dim=1).cpu().numpy()[0]
        run_probs[row["run"]].append(probs)
        run_true[row["run"]] = row[col]

    print(f"\nTest runs: {len(run_true)}  |  Classes: {classes}")
    print(f"\n{'Run':<10} {'True':<18} {'Vote pred':<18} {'Window votes'}")
    print("-" * 72)

    confusion = defaultdict(lambda: defaultdict(int))
    correct = 0

    for run in sorted(run_true.keys(), key=lambda r: int(r[3:])):
        true_cls = run_true[run]
        probs_list = np.array(run_probs[run])
        avg_probs = probs_list.mean(axis=0)
        vote_idx = avg_probs.argmax()
        vote_cls = classes[vote_idx]
        window_preds = [classes[p.argmax()] for p in probs_list]
        ok = "V" if vote_cls == true_cls else "X"
        if vote_cls == true_cls:
            correct += 1
        confusion[true_cls][vote_cls] += 1
        conf_pct = [f"{p*100:.0f}%" for p in avg_probs]
        print(f"{run:<10} {str(true_cls):<18} {str(vote_cls):<18} {window_preds}  {ok}")
        print(f"{'':10} {'avg probs:':18} {dict(zip(classes, conf_pct))}")

    print(f"\nRun-level accuracy: {correct}/{len(run_true)} = {correct/len(run_true)*100:.1f}%")

    print(f"\nConfusion matrix (rows=true, cols=pred):")
    print(f"{'':18}" + "".join(f"{str(c):>12}" for c in classes))
    for tc in classes:
        row_str = f"{str(tc):18}" + "".join(f"{confusion[tc][pc]:>12}" for pc in classes)
        total = sum(confusion[tc].values())
        pct = f"{confusion[tc][tc]/total*100:.0f}%"
        print(f"{row_str}   ({pct} correct)")

    print(f"\nPer-class breakdown:")
    for tc in classes:
        total = sum(confusion[tc].values())
        wrong = {k: v for k, v in confusion[tc].items() if k != tc}
        print(f"  {str(tc):18} {confusion[tc][tc]}/{total} correct  "
              f"misclassified_as={wrong}")

if __name__ == "__main__":
    for cfg in CONFIGS:
        run_inference(*cfg)
