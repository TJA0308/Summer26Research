"""Quick run-level accuracy eval for roughness alt checkpoints."""
import sys
from pathlib import Path
from collections import Counter, defaultdict
import torch
import numpy as np
from torchvision import transforms
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent / "cnn_model"))
from cnn_train import (
    RA_LABELS, RA_NAMES,
    RA_TEST_RUNS_ALT7, RA_TEST_RUNS_ALT8,
    build_model,
)

ROOT = Path(__file__).parent
IMG_DIR = ROOT / "scalograms_10w"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

VAL_TF = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

def load_test_images(test_runs):
    paths, labels, runs = [], [], []
    for png in sorted(IMG_DIR.glob("*.png")):
        stem = png.stem
        if stem.startswith("smote_"):
            continue
        run = stem.split("_w")[0]
        if run not in test_runs:
            continue
        label = RA_LABELS.get(run)
        if label is None:
            continue
        paths.append(png)
        labels.append(label)
        runs.append(run)
    return paths, labels, runs

@torch.no_grad()
def eval_ckpt(pt_path, test_runs):
    model = build_model("resnet18", 3, freeze_backbone=False, dropout=0.15).to(DEVICE)
    state = torch.load(pt_path, map_location=DEVICE, weights_only=False)
    if isinstance(state, dict) and "model_state_dict" in state:
        state = state["model_state_dict"]
    model.load_state_dict(state)
    model.eval()

    paths, labels, run_ids = load_test_images(test_runs)

    run_votes = defaultdict(list)
    for p, l, r in zip(paths, labels, run_ids):
        img = VAL_TF(Image.open(p).convert("RGB")).unsqueeze(0).to(DEVICE)
        logits = model(img)
        pred = logits.argmax(dim=1).item()
        run_votes[r].append((l, pred))

    correct = 0
    total = 0
    print(f"  {'Run':<12} {'True':>5} {'Pred':>5} {'Win':>6} {'Pass':>5}")
    for run in sorted(run_votes):
        pairs = run_votes[run]
        true_l = pairs[0][0]
        votes = Counter(p for _, p in pairs)
        pred_l = votes.most_common(1)[0][0]
        win_correct = sum(1 for tl, pl in pairs if tl == pl)
        passed = pred_l == true_l
        correct += int(passed)
        total += 1
        mark = "OK" if passed else "FAIL"
        print(f"  {run:<12} {RA_NAMES[true_l]:>20}  {win_correct:>2}/10  {mark}")

    print(f"  Run-level: {correct}/{total} = {correct/total*100:.1f}%")
    return correct, total

MODELS_DIR = ROOT / "cnn_model" / "models_roughness_raw_10w"

checkpoints = [
    ("ALT7 run4", MODELS_DIR / "resnet18_lr1e3_alt7_run4_best.pt", RA_TEST_RUNS_ALT7),
    ("ALT7 run5", MODELS_DIR / "resnet18_lr1e3_alt7_run5_best.pt", RA_TEST_RUNS_ALT7),
    ("ALT7 run2", MODELS_DIR / "resnet18_lr1e3_alt7_run2_best.pt", RA_TEST_RUNS_ALT7),
    ("ALT8 run2", MODELS_DIR / "resnet18_lr1e3_alt8_run2_best.pt", RA_TEST_RUNS_ALT8),
    ("ALT8 run4", MODELS_DIR / "resnet18_lr1e3_alt8_run4_best.pt", RA_TEST_RUNS_ALT8),
]

for name, pt, test_runs in checkpoints:
    if not pt.exists():
        print(f"\n{name}: MISSING {pt.name}")
        continue
    print(f"\n{name} ({pt.name}):")
    eval_ckpt(pt, test_runs)
