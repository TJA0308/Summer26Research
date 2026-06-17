"""
Detailed per-window evaluation for a trained Shoulder Milling parameter model
(speed / feed / doc), mirroring End Milling/cnn_model/eval_detailed.py.

For the given target and scalogram pipeline (Option C = scalograms_32x12,
Option D = scalograms_32x3), loads the checkpoint saved by cnn_train_param.py
and evaluates every window of every held-out test run -- 8 test conditions x
3 time windows = 24 test samples (see README.md "Three Model Splits") --
printing a per-run, per-window prediction table with the majority-vote result
and saving it as Markdown.

Usage (from this directory):
    python eval_detailed_param.py --target speed --img_dir scalograms_32x12 --arch resnet18 --lr 1e-3
    python eval_detailed_param.py --target doc --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4 \
        --save_md exp_results_32x3/doc_convnext_tiny_lr0.0001.md

    # Explicit checkpoint path instead of the default models_<target>_<tag>/<arch>_lr<lr>_best.pt
    python eval_detailed_param.py --target feed --img_dir scalograms_32x12 --arch resnet50 \
        --model models_feed_32x12/resnet50_lr0.001_best.pt --save_md results/feed_resnet50.md
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-16"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd
import torch
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from cnn_train_param import TARGETS, FEED_TO_LETTER, build_model, build_transforms, label_for

ROOT = Path(__file__).parent

# labels.csv "window" column uses a/b/c for the 3 time windows of each run
WINDOW_ORDER = {"a": 1, "b": 2, "c": 3}


def load_test_windows(img_dir, target):
    """Returns ({run_id: [(path, window_num), ...]}, {run_id: label}) for the
    held-out test runs of `target` (run_id = side + feed letter, e.g. '1a')."""
    df = pd.read_csv(img_dir / "labels.csv")
    df["run_id"] = df["side"].astype(str) + df["feed"].map(FEED_TO_LETTER)
    df["label"]  = df.apply(lambda r: label_for(target, r["side"], r["feed"]), axis=1)

    spec    = TARGETS[target]
    test_df = df[df["run_id"].isin(spec["test_runs"])]

    run_windows = defaultdict(list)
    run_label   = {}
    for _, row in test_df.iterrows():
        run_windows[row["run_id"]].append((img_dir / row["filename"], WINDOW_ORDER[row["window"]]))
        run_label[row["run_id"]] = row["label"]
    for run_id in run_windows:
        run_windows[run_id].sort(key=lambda x: x[1])
    return run_windows, run_label


@torch.no_grad()
def predict(model, path, val_tf, device):
    img = Image.open(path).convert("RGB")
    t = val_tf(img).unsqueeze(0).to(device)
    return model(t).argmax(1).item()


def run_evaluation(model, run_windows, run_label, val_tf, device):
    """Returns a list of result dicts, one per test run, sorted by run id."""
    results = []
    for run_id in sorted(run_windows.keys()):
        true_lbl     = run_label[run_id]
        window_preds = [predict(model, path, val_tf, device) for path, _ in run_windows[run_id]]
        majority     = Counter(window_preds).most_common(1)[0][0]
        results.append({
            "run":          run_id,
            "true_label":   true_lbl,
            "window_preds": window_preds,
            "majority":     majority,
            "correct":      majority == true_lbl,
        })
    return results


def _summary(results):
    n_runs, n_correct = len(results), sum(r["correct"] for r in results)
    all_preds  = [p for r in results for p in r["window_preds"]]
    all_labels = [r["true_label"] for r in results for _ in r["window_preds"]]
    win_correct = sum(p == l for p, l in zip(all_preds, all_labels))
    return win_correct, len(all_preds), n_correct, n_runs


def print_table(results, class_names, n_windows=3):
    w_cols = "  ".join(f"w{i+1}" for i in range(n_windows))
    header = f"  {'Run':<6}  {'True':<8}  {w_cols}  {'MV':<8}  OK"
    sep    = "  " + "-" * (len(header) - 2)
    print(header)
    print(sep)
    for r in results:
        true_s = class_names[r["true_label"]]
        wins_s = "  ".join(f"{class_names[p]:>4}" for p in r["window_preds"])
        mv_s   = class_names[r["majority"]]
        ok_s   = "✓" if r["correct"] else "✗"
        print(f"  {r['run']:<6}  {true_s:<8}  {wins_s}  {mv_s:<8}  {ok_s}")
    print(sep)

    win_correct, n_windows_total, n_correct, n_runs = _summary(results)
    print(f"  Window accuracy: {win_correct}/{n_windows_total} = {win_correct/n_windows_total*100:.1f}%")
    print(f"  Run MV accuracy: {n_correct}/{n_runs} = {n_correct/n_runs*100:.1f}%")


def to_markdown(results, class_names, model_name, target, scalo_tag, arch, n_windows=3):
    w_headers = " | ".join(f"w{i+1}" for i in range(n_windows))
    lines = [
        f"### {model_name}  |  target={target}  |  scalogram={scalo_tag}  |  arch={arch}",
        "",
        f"| Run | True | {w_headers} | MV | ✓/✗ |",
        "|-----|------|" + "|".join(["----"] * n_windows) + "|-----|-----|",
    ]
    for r in results:
        true_s = class_names[r["true_label"]]
        wins_s = " | ".join(class_names[p] for p in r["window_preds"])
        mv_s   = class_names[r["majority"]]
        ok_s   = "✓" if r["correct"] else "✗"
        lines.append(f"| {r['run']} | {true_s} | {wins_s} | {mv_s} | {ok_s} |")

    win_correct, n_windows_total, n_correct, n_runs = _summary(results)
    lines += [
        "",
        f"Window accuracy: **{win_correct/n_windows_total*100:.1f}%** ({win_correct}/{n_windows_total})",
        f"Run MV accuracy: **{n_correct/n_runs*100:.1f}%** ({n_correct}/{n_runs})",
    ]
    return "\n".join(lines)


def eval_one(model_path, target, img_dir, arch, device=None, save_md=None, verbose=True, dropout=None):
    """Evaluate one trained checkpoint. Returns (results, markdown_string).

    If dropout is None, it's auto-detected from the sibling <tag>_history.json
    written by cnn_train_param.py (defaults to 0.0 if absent/not found) --
    dropout>0 wraps the final Linear in a Sequential, which changes the
    state_dict key names, so the eval-time model must be built the same way
    the checkpoint was trained or load_state_dict will fail."""
    device      = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    spec        = TARGETS[target]
    class_names = spec["class_names"]
    img_dir     = Path(img_dir)
    model_path  = Path(model_path)

    if dropout is None:
        hist_path = model_path.parent / model_path.name.replace("_best.pt", "_history.json")
        dropout   = 0.0
        if hist_path.exists():
            with open(hist_path) as f:
                dropout = json.load(f).get("dropout", 0.0)

    model = build_model(arch, spec["num_classes"], dropout=dropout).to(device)
    state = torch.load(model_path, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.eval()

    _, val_tf = build_transforms()
    run_windows, run_label = load_test_windows(img_dir, target)
    if not run_windows:
        raise RuntimeError(f"No test windows found for target={target} in {img_dir}")

    results = run_evaluation(model, run_windows, run_label, val_tf, device)

    if verbose:
        print(f"\nModel : {Path(model_path).name}")
        print(f"Target: {target}  |  Scalogram: {img_dir.name}  |  Arch: {arch}\n")
        print_table(results, class_names)

    md = to_markdown(results, class_names, Path(model_path).stem, target, img_dir.name, arch)
    if save_md:
        save_md = Path(save_md)
        save_md.parent.mkdir(parents=True, exist_ok=True)
        save_md.write_text(md, encoding="utf-8")
        if verbose:
            print(f"\nMarkdown saved to: {save_md}")
    return results, md


def main():
    parser = argparse.ArgumentParser(
        description="Per-window evaluation for a trained Shoulder Milling parameter model.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--target",  required=True, choices=list(TARGETS.keys()))
    parser.add_argument("--img_dir", required=True, help="scalograms_32x12 or scalograms_32x3")
    parser.add_argument("--arch",    required=True,
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"])
    parser.add_argument("--lr",      type=float, default=None,
                        help="Used to locate the default checkpoint path "
                             "(models_<target>_<tag>/<arch>_lr<lr>_best.pt) and the default --save_md path")
    parser.add_argument("--model",   default=None,
                        help="Explicit path to a .pt checkpoint (overrides the --lr-derived default path)")
    parser.add_argument("--save_md", default=None,
                        help="Path to save markdown output "
                             "(default: exp_results_<tag>/<target>_<arch>_lr<lr>[_<run_tag>].md)")
    parser.add_argument("--run_tag", default="",
                        help="Optional suffix matching the training run's --run_tag, e.g. 'smote' -- "
                             "used to build the default --model and --save_md paths")
    args = parser.parse_args()

    img_dir    = ROOT / args.img_dir
    scalo_tag  = img_dir.name.replace("scalograms_", "")
    tag_suffix = f"_{args.run_tag}" if args.run_tag else ""

    if args.model:
        model_path = Path(args.model)
        if not model_path.is_absolute():
            model_path = ROOT / model_path
    else:
        if args.lr is None:
            parser.error("--lr is required when --model is not given")
        model_path = ROOT / f"models_{args.target}_{scalo_tag}" / f"{args.arch}_lr{args.lr:g}{tag_suffix}_best.pt"

    if not model_path.exists():
        print(f"ERROR: model file not found: {model_path}")
        sys.exit(1)

    save_md = args.save_md
    if save_md is None and args.lr is not None:
        save_md = ROOT / f"exp_results_{scalo_tag}" / f"{args.target}_{args.arch}_lr{args.lr:g}{tag_suffix}.md"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    eval_one(model_path, args.target, img_dir, args.arch, device=device, save_md=save_md)


if __name__ == "__main__":
    main()
