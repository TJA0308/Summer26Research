"""
Evaluate saved models on held-out test data only.
Reports window-level accuracy, per-run majority-vote accuracy, confusion matrix,
and per-class breakdown.

Usage (run from project root):
    python cnn_model/eval_test.py
"""
import sys
from pathlib import Path
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).parent))
from cnn_train import (
    SPEED_LABELS, SPEED_TEST_RUNS, SPEED_NAMES,
    FEED_LABELS, FEED_TEST_RUNS, FEED_NAMES,
    FEED_COARSE_LABELS, FEED_COARSE_TEST_RUNS, FEED_COARSE_NAMES,
    RA_LABELS, RA_TEST_RUNS, RA_NAMES,
    DOC_LABELS, DOC_TEST_RUNS, DOC_NAMES,
    build_model,
)

ROOT = Path(__file__).parent.parent
IMG_10W    = ROOT / "scalograms_10w"
IMG_10W_FI = ROOT / "scalograms_10w_fi"

VAL_TF = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])


def load_test_images(img_dir, label_map, test_runs):
    """Return (paths, labels, run_ids) for original test run images only (no SMOTE synthetics)."""
    paths, labels, run_ids = [], [], []
    for png in sorted(img_dir.glob("*.png")):
        stem = png.stem  # e.g. "run5_w3"
        if stem.startswith("smote_"):
            continue
        run = stem.split("_w")[0]
        if run not in test_runs:
            continue
        label = label_map.get(run)
        if label is None:
            continue
        paths.append(png)
        labels.append(label)
        run_ids.append(run)
    return paths, labels, run_ids


@torch.no_grad()
def evaluate(model, paths, labels, run_ids, class_names, device):
    """Window-level predictions + hard majority vote per run."""
    model.eval()
    preds = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        t   = VAL_TF(img).unsqueeze(0).to(device)
        p   = model(t).argmax(1).item()
        preds.append(p)

    n       = len(labels)
    correct = sum(p == l for p, l in zip(preds, labels))
    window_acc = correct / n if n > 0 else 0.0

    # Per-run majority vote
    run_votes  = defaultdict(list)
    run_labels = {}
    for run, pred, label in zip(run_ids, preds, labels):
        run_votes[run].append(pred)
        run_labels[run] = label

    run_correct = 0
    run_results = {}
    for run, votes in sorted(run_votes.items()):
        majority  = Counter(votes).most_common(1)[0][0]
        true_lbl  = run_labels[run]
        ok        = (majority == true_lbl)
        run_correct += int(ok)
        run_results[run] = {
            "true":     true_lbl,
            "majority": majority,
            "ok":       ok,
            "votes":    Counter(votes),
        }
    run_acc = run_correct / len(run_votes) if run_votes else 0.0

    # Per-class window accuracy
    class_correct = defaultdict(int)
    class_total   = defaultdict(int)
    class_wrong   = defaultdict(list)
    for p, l in zip(preds, labels):
        class_total[l]   += 1
        class_correct[l] += int(p == l)
        if p != l:
            class_wrong[l].append(p)

    # Confusion matrix
    num_classes = len(class_names)
    conf = np.zeros((num_classes, num_classes), dtype=int)
    for p, l in zip(preds, labels):
        conf[l][p] += 1

    return {
        "window_acc":    window_acc,
        "run_acc":       run_acc,
        "n_windows":     n,
        "n_runs":        len(run_votes),
        "class_correct": dict(class_correct),
        "class_total":   dict(class_total),
        "class_wrong":   dict(class_wrong),
        "run_results":   run_results,
        "conf":          conf,
        "preds":         preds,
        "labels":        labels,
    }


@torch.no_grad()
def evaluate_prob_avg(model, paths, labels, run_ids, class_names, device):
    """
    Run-level soft voting: average softmax probabilities across all windows of
    each run, then take argmax. One prediction per run — no per-window accuracy.
    """
    import torch.nn.functional as F
    model.eval()

    # Group by run
    run_paths  = defaultdict(list)
    run_labels = {}
    for path, label, run in zip(paths, labels, run_ids):
        run_paths[run].append(path)
        run_labels[run] = label

    run_results = {}
    run_correct = 0
    class_correct = defaultdict(int)
    class_total   = defaultdict(int)
    class_wrong   = defaultdict(list)
    num_classes   = len(class_names)
    conf = np.zeros((num_classes, num_classes), dtype=int)

    for run in sorted(run_paths.keys()):
        true_lbl = run_labels[run]
        # Stack all window tensors for this run
        tensors = []
        for path in sorted(run_paths[run]):
            img = Image.open(path).convert("RGB")
            tensors.append(VAL_TF(img))
        batch = torch.stack(tensors).to(device)          # [N_windows, C, H, W]
        logits = model(batch)                             # [N_windows, num_classes]
        probs  = F.softmax(logits, dim=1)                 # [N_windows, num_classes]
        avg_prob = probs.mean(dim=0)                      # [num_classes]
        top2     = avg_prob.topk(2)
        pred     = avg_prob.argmax().item()
        ok = (pred == true_lbl)
        run_correct += int(ok)

        class_total[true_lbl]   += 1
        class_correct[true_lbl] += int(ok)
        if not ok:
            class_wrong[true_lbl].append(pred)
        conf[true_lbl][pred] += 1

        run_results[run] = {
            "true":     true_lbl,
            "pred":     pred,
            "ok":       ok,
            "avg_prob": avg_prob.cpu().numpy(),
            "top2_idx": top2.indices.cpu().tolist(),
            "top2_val": top2.values.cpu().tolist(),
        }

    n_runs  = len(run_paths)
    run_acc = run_correct / n_runs if n_runs > 0 else 0.0

    return {
        "run_acc":       run_acc,
        "n_runs":        n_runs,
        "class_correct": dict(class_correct),
        "class_total":   dict(class_total),
        "class_wrong":   dict(class_wrong),
        "run_results":   run_results,
        "conf":          conf,
    }


def print_prob_avg_results(name, target, backbone, result, class_names):
    print(f"\n{'='*70}")
    print(f"  [PROB-AVG] Model: {name}  |  Target: {target}  |  Backbone: {backbone}")
    print(f"{'='*70}")
    print(f"  Run-level (prob avg) accuracy: {result['run_acc']*100:.1f}%"
          f"  ({sum(result['class_correct'].values())}/{result['n_runs']} runs)")

    print(f"\n  Per-run results:")
    for run, r in sorted(result['run_results'].items()):
        status = "OK   " if r['ok'] else "WRONG"
        top2   = ", ".join(
            f"{class_names[i]}={v:.3f}"
            for i, v in zip(r['top2_idx'], r['top2_val'])
        )
        print(f"    {run:8s}  true={class_names[r['true']]:25s}"
              f"  pred={class_names[r['pred']]:25s}  [{status}]  top2: {top2}")

    print(f"\n  Per-class accuracy:")
    for c in sorted(class_names.keys()):
        tot   = result['class_total'].get(c, 0)
        corr  = result['class_correct'].get(c, 0)
        wrong = result['class_wrong'].get(c, [])
        wrong_str = ""
        if wrong:
            wc = Counter(wrong)
            wrong_str = "  misclassified as: " + ", ".join(
                f"{class_names[k]}×{v}" for k, v in wc.most_common()
            )
        print(f"    {class_names[c]:25s}  {corr}/{tot}{wrong_str}")


def print_results(name, target, backbone, img_dir_name, result, class_names):
    print(f"\n{'='*70}")
    print(f"  Model  : {name}")
    print(f"  Target : {target}  |  Backbone: {backbone}  |  Dir: {img_dir_name}")
    print(f"{'='*70}")
    print(f"  Window-level accuracy : {result['window_acc']*100:.1f}%"
          f"  ({sum(result['class_correct'].values())}/{result['n_windows']})")
    print(f"  Run majority-vote     : {result['run_acc']*100:.1f}%"
          f"  ({sum(1 for r in result['run_results'].values() if r['ok'])}/{result['n_runs']} runs)")

    print(f"\n  Per-class window accuracy:")
    for c in sorted(class_names.keys()):
        tot   = result['class_total'].get(c, 0)
        corr  = result['class_correct'].get(c, 0)
        wrong = result['class_wrong'].get(c, [])
        wrong_str = ""
        if wrong:
            wc = Counter(wrong)
            wrong_str = "  misclassified as: " + ", ".join(
                f"{class_names[k]}×{v}" for k, v in wc.most_common()
            )
        print(f"    {class_names[c]:25s}  {corr:3d}/{tot}{wrong_str}")

    print(f"\n  Per-run majority-vote:")
    for run, r in sorted(result['run_results'].items()):
        status = "OK   " if r['ok'] else "WRONG"
        votes  = ", ".join(f"{class_names[k]}×{v}" for k, v in r['votes'].most_common())
        print(f"    {run:8s}  true={class_names[r['true']]:25s}"
              f"  pred={class_names[r['majority']]:25s}  [{status}]  votes: {votes}")

    print(f"\n  Confusion matrix (rows=true, cols=pred):")
    header = "             " + "".join(f"{class_names[c][:10]:>12}" for c in sorted(class_names))
    print(f"  {header}")
    for c in sorted(class_names.keys()):
        row = "".join(f"{result['conf'][c][p]:>12}" for p in sorted(class_names.keys()))
        print(f"  {class_names[c][:10]:>12}{row}")


def run_eval(name, model_path, backbone, num_classes, target,
             img_dir, label_map, test_runs, class_names, device):
    print(f"\nLoading {name} from {model_path.name} ...", flush=True)
    if not model_path.exists():
        print(f"  ERROR: {model_path} not found, skipping.")
        return None, None

    model = build_model(backbone, num_classes, freeze_backbone=False).to(device)
    state = torch.load(model_path, map_location=device, weights_only=True)
    model.load_state_dict(state)

    paths, labels, run_ids = load_test_images(img_dir, label_map, test_runs)
    if not paths:
        print(f"  ERROR: no test images found in {img_dir}")
        return None, None

    print(f"  Found {len(paths)} test images across {len(set(run_ids))} runs", flush=True)

    # Window-level + hard majority vote
    result_win = evaluate(model, paths, labels, run_ids, class_names, device)
    print_results(name, target, backbone, img_dir.name, result_win, class_names)

    # Soft probability averaging — whole-run inference
    print(f"\n  --- Soft probability averaging (whole-run) ---", flush=True)
    result_prob = evaluate_prob_avg(model, paths, labels, run_ids, class_names, device)
    print_prob_avg_results(name, target, backbone, result_prob, class_names)

    return result_win, result_prob


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    experiments = [
        # (display_name, model_path, backbone, num_classes, target,
        #  img_dir, label_map, test_runs, class_names)
        (
            "speed_cnxt_10w",
            ROOT / "speed_cnxt_10w.pt",
            "convnext_tiny", 5, "speed",
            IMG_10W, SPEED_LABELS, SPEED_TEST_RUNS, SPEED_NAMES,
        ),
        (
            "speed_resnet_10w",
            ROOT / "speed_resnet_10w.pt",
            "resnet18", 5, "speed",
            IMG_10W, SPEED_LABELS, SPEED_TEST_RUNS, SPEED_NAMES,
        ),
        (
            "feed_rn18_10w (best feed)",
            ROOT / "exp_models" / "feed_rn18_10w_adamw.pt",
            "resnet18", 6, "feed",
            IMG_10W, FEED_LABELS, FEED_TEST_RUNS, FEED_NAMES,
        ),
        (
            "feed_effb0_10w (2nd best feed)",
            ROOT / "exp_models" / "feed_effb0_10w_adamw.pt",
            "efficientnet_b0", 6, "feed",
            IMG_10W, FEED_LABELS, FEED_TEST_RUNS, FEED_NAMES,
        ),
        (
            "roughness_rn18_10w (best roughness)",
            ROOT / "exp_models" / "roughness_rn18_10w_adamw.pt",
            "resnet18", 3, "roughness",
            IMG_10W, RA_LABELS, RA_TEST_RUNS, RA_NAMES,
        ),
        (
            "feed_coarse_rn18_10w",
            ROOT / "exp_models" / "feed_coarse_rn18_10w_adamw.pt",
            "resnet18", 3, "feed_coarse",
            IMG_10W, FEED_COARSE_LABELS, FEED_COARSE_TEST_RUNS, FEED_COARSE_NAMES,
        ),
        (
            "feed_coarse_effb0_10w",
            ROOT / "exp_models" / "feed_coarse_effb0_10w_adamw.pt",
            "efficientnet_b0", 3, "feed_coarse",
            IMG_10W, FEED_COARSE_LABELS, FEED_COARSE_TEST_RUNS, FEED_COARSE_NAMES,
        ),
        (
            "feed_cnxt_10w",
            ROOT / "feed_cnxt_10w_adamw.pt",
            "convnext_tiny", 6, "feed",
            IMG_10W, FEED_LABELS, FEED_TEST_RUNS, FEED_NAMES,
        ),
        (
            "feed_coarse_cnxt_10w",
            ROOT / "feed_coarse_cnxt_10w_adamw.pt",
            "convnext_tiny", 3, "feed_coarse",
            IMG_10W, FEED_COARSE_LABELS, FEED_COARSE_TEST_RUNS, FEED_COARSE_NAMES,
        ),
        (
            "doc_resnet18_10w",
            ROOT / "best_model_doc_resnet18.pt",
            "resnet18", 3, "doc",
            IMG_10W, DOC_LABELS, DOC_TEST_RUNS, DOC_NAMES,
        ),
        (
            "doc_convnext_10w",
            ROOT / "best_model_doc_convnext.pt",
            "convnext_tiny", 3, "doc",
            IMG_10W, DOC_LABELS, DOC_TEST_RUNS, DOC_NAMES,
        ),
    ]

    all_results = {}
    for exp in experiments:
        name, model_path, backbone, num_classes, target, img_dir, label_map, test_runs, class_names = exp
        r_win, r_prob = run_eval(name, model_path, backbone, num_classes, target,
                                 img_dir, label_map, test_runs, class_names, device)
        if r_win:
            all_results[name] = (r_win, r_prob, target)

    print(f"\n\n{'#'*70}")
    print("  SUMMARY — Test-only holdout evaluation")
    print("  (models were never trained on these runs)")
    print(f"{'#'*70}")
    print(f"  {'Model':<42} {'Target':<12} {'Window%':>9} {'HardMV%':>9} {'SoftAvg%':>10}")
    print("  " + "-" * 86)
    for name, (r_win, r_prob, target) in all_results.items():
        soft = f"{r_prob['run_acc']*100:.1f}%" if r_prob else "  —"
        print(f"  {name:<42} {target:<12} {r_win['window_acc']*100:>8.1f}%"
              f"  {r_win['run_acc']*100:>8.1f}%  {soft:>9}")


if __name__ == "__main__":
    main()
