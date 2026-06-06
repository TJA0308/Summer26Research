"""
Detailed per-window evaluation for any trained model.

Outputs a table showing the prediction for every individual window of every
test run, the majority-vote result for each run, and overall accuracy.
Also writes a Markdown file that can be pasted into the README.

Usage (from project root):
    # Pipeline A (standard CWT, scalograms_10w)
    python cnn_model/eval_detailed.py --model std_speed_rn50_lr1e3.pt --target speed --backbone resnet50 --pipeline a

    # Pipeline B (SES 4-channel, scalograms_ses_10w)
    python cnn_model/eval_detailed.py --model ses_speed_rn18_lr1e3.pt --target speed --backbone resnet18 --pipeline b

    # Save markdown output
    python cnn_model/eval_detailed.py --model std_speed_rn50_lr1e3.pt --target speed --backbone resnet50 --pipeline a --save_md results/std_speed_rn50_lr1e3.md
"""
import argparse
import sys
from collections import defaultdict, Counter

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-16"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

sys.path.insert(0, str(Path(__file__).parent))
from cnn_train import (
    SPEED_LABELS, SPEED_NAMES, SPEED_TEST_RUNS,
    DOC_LABELS, DOC_NAMES, DOC_TEST_RUNS,
    RA_LABELS, RA_NAMES, RA_TEST_RUNS,
    FEED_COARSE_LABELS, FEED_COARSE_NAMES, FEED_COARSE_TEST_RUNS,
    build_model,
)
from cnn_train_hilbert import (
    SPEED_TEST_RUNS_H, DOC_TEST_RUNS_H, FEED_COARSE_TEST_RUNS_H,
    build_model_4ch,
)

ROOT = Path(__file__).parent.parent

VAL_TF = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# ── Target configuration ──────────────────────────────────────────────────────
# (label_map, class_names, test_runs_A, test_runs_B, num_classes)
TARGET_CFG = {
    "speed": (
        SPEED_LABELS, SPEED_NAMES,
        SPEED_TEST_RUNS, SPEED_TEST_RUNS_H,
        5,
    ),
    "doc": (
        DOC_LABELS, DOC_NAMES,
        DOC_TEST_RUNS, DOC_TEST_RUNS_H,
        3,
    ),
    "roughness": (
        RA_LABELS, RA_NAMES,
        RA_TEST_RUNS, RA_TEST_RUNS,   # same test set for both pipelines
        3,
    ),
    "feed_coarse": (
        FEED_COARSE_LABELS, FEED_COARSE_NAMES,
        FEED_COARSE_TEST_RUNS, FEED_COARSE_TEST_RUNS_H,
        3,
    ),
}

# Short class-name abbreviations for the per-window table columns
SHORT_NAMES = {
    # Speed
    "1500 rpm": "1500", "2000 rpm": "2000", "3000 rpm": "3000",
    "4000 rpm": "4000", "5000 rpm": "5000",
    # DOC
    "0.015 mm": ".015", "0.03 mm": ".030", "0.06 mm": ".060",
    # Roughness
    "Smooth (Ra<0.7)": "Smt", "Medium (0.7-1.0)": "Med", "Rough (Ra>1.0)": "Rgh",
    # Feed coarse
    "3-4 mm/rev (low)": "Low", "5-6 mm/rev (med)": "Med", "7-8 mm/rev (high)": "Hi",
}


def short(class_names, label):
    full = class_names[label]
    return SHORT_NAMES.get(full, full[:4])


def load_png_windows(img_dir, label_map, test_runs):
    """Returns {run: [(path, window_num), ...]} for test PNG files."""
    run_windows = defaultdict(list)
    for png in sorted(img_dir.glob("*.png")):
        stem = png.stem
        if stem.startswith("smote_"):
            continue
        parts = stem.rsplit("_w", 1)
        if len(parts) != 2:
            continue
        run, w = parts[0], int(parts[1])
        if run not in test_runs or run not in label_map:
            continue
        run_windows[run].append((png, w))
    for run in run_windows:
        run_windows[run].sort(key=lambda x: x[1])
    return run_windows


def load_npy_windows(img_dir, label_map, test_runs):
    """Returns {run: [(path, window_num), ...]} for test .npy files."""
    run_windows = defaultdict(list)
    for npy in sorted(img_dir.glob("*.npy")):
        stem = npy.stem
        if stem.startswith("smote_"):
            continue
        parts = stem.rsplit("_w", 1)
        if len(parts) != 2:
            continue
        run, w = parts[0], int(parts[1])
        if run not in test_runs or run not in label_map:
            continue
        run_windows[run].append((npy, w))
    for run in run_windows:
        run_windows[run].sort(key=lambda x: x[1])
    return run_windows


@torch.no_grad()
def predict_png(model, path, device):
    img = Image.open(path).convert("RGB")
    t = VAL_TF(img).unsqueeze(0).to(device)
    return model(t).argmax(1).item()


@torch.no_grad()
def predict_npy(model, path, device):
    arr = torch.from_numpy(np.load(path)).float().unsqueeze(0).to(device)
    return model(arr).argmax(1).item()


def run_evaluation(model, run_windows, label_map, class_names, predict_fn, device):
    """
    Returns list of result dicts, one per run, sorted by run name.
    Each dict: {run, true_label, window_preds (ordered list), majority, correct}
    """
    results = []
    for run in sorted(run_windows.keys()):
        true_lbl = label_map[run]
        window_preds = []
        for path, _ in run_windows[run]:
            window_preds.append(predict_fn(model, path, device))
        majority = Counter(window_preds).most_common(1)[0][0]
        results.append({
            "run":          run,
            "true_label":   true_lbl,
            "window_preds": window_preds,
            "majority":     majority,
            "correct":      majority == true_lbl,
        })
    return results


def print_table(results, class_names, n_windows=10):
    """Print the per-run, per-window table to stdout."""
    w_cols = "  ".join(f"w{i+1:>2}" for i in range(n_windows))
    header = f"  {'Run':<8}  {'True':<10}  {w_cols}  {'MV':<10}  OK"
    sep    = "  " + "-" * (len(header) - 2)
    print(header)
    print(sep)
    for r in results:
        true_s = short(class_names, r["true_label"])
        wins_s = "  ".join(f"{short(class_names, p):>4}" for p in r["window_preds"])
        mv_s   = short(class_names, r["majority"])
        ok_s   = "✓" if r["correct"] else "✗"
        print(f"  {r['run']:<8}  {true_s:<10}  {wins_s}  {mv_s:<10}  {ok_s}")
    print(sep)

    n_runs   = len(results)
    n_correct = sum(r["correct"] for r in results)
    all_preds  = [p for r in results for p in r["window_preds"]]
    all_labels = [r["true_label"] for r in results for _ in r["window_preds"]]
    win_correct = sum(p == l for p, l in zip(all_preds, all_labels))
    print(f"  Window accuracy: {win_correct}/{len(all_preds)} = {win_correct/len(all_preds)*100:.1f}%")
    print(f"  Run MV accuracy: {n_correct}/{n_runs} = {n_correct/n_runs*100:.1f}%")


def to_markdown(results, class_names, model_name, target, pipeline, n_windows=10):
    """Generate markdown table string."""
    w_headers = " | ".join(f"w{i+1}" for i in range(n_windows))
    lines = [
        f"### {model_name}  |  target={target}  |  pipeline={pipeline.upper()}",
        "",
        f"| Run | True | {w_headers} | MV | ✓/✗ |",
        "|-----|------|" + "|".join(["----"] * n_windows) + "|-----|-----|",
    ]
    for r in results:
        true_s = short(class_names, r["true_label"])
        wins_s = " | ".join(f"{short(class_names, p)}" for p in r["window_preds"])
        mv_s   = short(class_names, r["majority"])
        ok_s   = "✓" if r["correct"] else "✗"
        lines.append(f"| {r['run']} | {true_s} | {wins_s} | {mv_s} | {ok_s} |")

    n_runs    = len(results)
    n_correct = sum(r["correct"] for r in results)
    all_preds  = [p for r in results for p in r["window_preds"]]
    all_labels = [r["true_label"] for r in results for _ in r["window_preds"]]
    win_correct = sum(p == l for p, l in zip(all_preds, all_labels))
    lines += [
        "",
        f"Window accuracy: **{win_correct/len(all_preds)*100:.1f}%** ({win_correct}/{len(all_preds)})",
        f"Run MV accuracy: **{n_correct/n_runs*100:.1f}%** ({n_correct}/{n_runs})",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Per-window evaluation for any trained model.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--model",    required=True,  help="Path to .pt model file (relative to project root or absolute)")
    parser.add_argument("--target",   required=True,  choices=list(TARGET_CFG.keys()))
    parser.add_argument("--backbone", required=True,
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"])
    parser.add_argument("--pipeline", required=True,  choices=["a", "b"],
                        help="a=Std CWT (scalograms_10w), b=SES 4-ch (scalograms_ses_10w)")
    parser.add_argument("--img_dir",  default=None,
                        help="Override default image directory for pipeline a (e.g. scalograms_ses_rgb_10w)")
    parser.add_argument("--save_md",  default=None,
                        help="Optional path to save markdown output (e.g. results/model_name.md)")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    model_path = Path(args.model)
    if not model_path.is_absolute():
        model_path = ROOT / model_path
    if not model_path.exists():
        print(f"ERROR: model file not found: {model_path}")
        sys.exit(1)

    label_map, class_names, test_runs_a, test_runs_b, num_classes = TARGET_CFG[args.target]
    test_runs = test_runs_a if args.pipeline == "a" else test_runs_b
    if args.img_dir:
        img_dir = ROOT / args.img_dir
    else:
        img_dir = ROOT / ("scalograms_10w" if args.pipeline == "a" else "scalograms_ses_10w")

    # Load model
    if args.pipeline == "a":
        model = build_model(args.backbone, num_classes, freeze_backbone=False).to(device)
    else:
        model = build_model_4ch(args.backbone, num_classes, freeze_backbone=False).to(device)

    state = torch.load(model_path, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.eval()
    print(f"Loaded: {model_path.name}")

    # Load windows
    if args.pipeline == "a":
        run_windows  = load_png_windows(img_dir, label_map, test_runs)
        predict_fn   = predict_png
    else:
        run_windows  = load_npy_windows(img_dir, label_map, test_runs)
        predict_fn   = predict_npy

    if not run_windows:
        print(f"ERROR: no test files found in {img_dir}")
        sys.exit(1)

    n_windows = max(len(v) for v in run_windows.values())
    print(f"Test runs: {len(run_windows)}  |  Windows per run: {n_windows}\n")

    # Evaluate
    results = run_evaluation(model, run_windows, label_map, class_names, predict_fn, device)

    print(f"\nModel  : {model_path.name}")
    print(f"Target : {args.target}  |  Pipeline: {'A (Std CWT)' if args.pipeline == 'a' else 'B (SES 4-ch)'}  |  Backbone: {args.backbone}\n")
    print_table(results, class_names, n_windows)

    # Class name legend
    print(f"\nClass legend:")
    for k, v in sorted(class_names.items()):
        print(f"  {short(class_names, k)} = {v}")

    # Save markdown
    if args.save_md:
        md_path = Path(args.save_md)
        if not md_path.is_absolute():
            md_path = ROOT / md_path
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md = to_markdown(results, class_names, model_path.stem, args.target,
                         args.pipeline, n_windows)
        md_path.write_text(md, encoding="utf-8")
        print(f"\nMarkdown saved to: {md_path}")


if __name__ == "__main__":
    main()
