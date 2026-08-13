"""Evaluate speed alt1/alt2 checkpoints run-level accuracy."""
import sys
from pathlib import Path
from collections import Counter, defaultdict
import torch
from torchvision import transforms
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent / "cnn_model"))
from cnn_train import (
    SPEED_LABELS, SPEED_NAMES,
    SPEED_TEST_RUNS, SPEED_TEST_RUNS_ALT1, SPEED_TEST_RUNS_ALT2,
    build_model,
)

ROOT = Path(__file__).parent
IMG_DIR = ROOT / "scalograms_10w"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODELS_DIR = ROOT / "cnn_model" / "models_speed_raw_10w"

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
        label = SPEED_LABELS.get(run)
        if label is None:
            continue
        paths.append(png)
        labels.append(label)
        runs.append(run)
    return paths, labels, runs

@torch.no_grad()
def eval_ckpt(name, pt_path, test_runs, num_classes=5):
    if not Path(pt_path).exists():
        print(f"{name}: MISSING")
        return
    model = build_model("resnet18", num_classes, freeze_backbone=False, dropout=0.15).to(DEVICE)
    state = torch.load(pt_path, map_location=DEVICE, weights_only=False)
    if isinstance(state, dict) and "model_state_dict" in state:
        state = state["model_state_dict"]
    # remap old fc.weight -> fc.1.weight if needed
    if "fc.weight" in state and "fc.1.weight" not in state:
        state = {("fc.1." + k[3:] if k.startswith("fc.") else k): v
                 for k, v in state.items()}
    model.load_state_dict(state)
    model.eval()

    paths, labels, run_ids = load_test_images(test_runs)
    run_votes = defaultdict(list)
    for p, l, r in zip(paths, labels, run_ids):
        img = VAL_TF(Image.open(p).convert("RGB")).unsqueeze(0).to(DEVICE)
        pred = model(img).argmax(dim=1).item()
        run_votes[r].append((l, pred))

    correct = 0
    total = 0
    print(f"\n{name}:")
    for run in sorted(run_votes):
        pairs = run_votes[run]
        true_l = pairs[0][0]
        votes = Counter(p for _, p in pairs)
        pred_l = votes.most_common(1)[0][0]
        win_ok = sum(1 for tl, pl in pairs if tl == pl)
        passed = pred_l == true_l
        correct += int(passed)
        total += 1
        mark = "OK" if passed else "FAIL"
        print(f"  {run:<8} {SPEED_NAMES[true_l]:>12}  {win_ok:>2}/10  {mark}")
    pct = correct / total * 100
    print(f"  Run-level: {correct}/{total} = {pct:.1f}%")

# Also evaluate baseline standard split
eval_ckpt("Standard (resnet18)", MODELS_DIR / "resnet18_lr0.001_best.pt",
          SPEED_TEST_RUNS)
eval_ckpt("ALT1 (resnet18)", MODELS_DIR / "resnet18_lr1e3_alt1_best.pt",
          SPEED_TEST_RUNS_ALT1)
eval_ckpt("ALT2 (resnet18)", MODELS_DIR / "resnet18_lr1e3_alt2_best.pt",
          SPEED_TEST_RUNS_ALT2)
