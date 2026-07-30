"""
Detailed per-window evaluation for a trained End Milling 32x3/32x12 parameter
model (speed / doc / feed_coarse / feed / roughness), mirroring Shoulder
Milling's eval_detailed_param.py.

Rather than reload the checkpoint and re-implement cascade/conditioning model
loading here, this reuses generate_window_results.py's
process_one_checkpoint() to (re)generate that single checkpoint's
*_window_preds.csv (filename, run, true_label, pred_label, prob_0..prob_k-1)
if it doesn't already exist next to the checkpoint, then renders it as a
per-run, per-window table -- showing BOTH the hard majority-vote result
(argmax per window, then mode across a run's windows) and the soft
probability-averaged result (mean softmax across windows, then argmax once;
see cnn_train_32x3.py's module docstring on why both are reported) -- plus
overall window and run-level accuracy. Also saves the table as Markdown next
to the checkpoint.

Usage (from this directory):
    python eval_detailed_32x3.py --target roughness --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4 --run_tag smote
    python eval_detailed_32x3.py --target speed --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3

    # feed_coarse cascade-predicted model
    python eval_detailed_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4 --run_tag cascade_smote

    # Force re-running inference even if a *_window_preds.csv already exists
    python eval_detailed_32x3.py --target doc --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-4 --regenerate
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-16"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

sys.path.insert(0, str(Path(__file__).parent))
from generate_window_results import TARGETS, process_one_checkpoint   # noqa: E402

ROOT = Path(__file__).parent

# Short class-name abbreviations for the per-window table columns (see
# cnn_model/eval_detailed.py's SHORT_NAMES, extended with the 32x3 pipeline's
# fine-grained 6-class "feed" target).
SHORT_NAMES = {
    # Speed
    "1500 rpm": "1500", "2000 rpm": "2000", "3000 rpm": "3000",
    "4000 rpm": "4000", "5000 rpm": "5000",
    # DOC
    "0.015 mm": ".015", "0.03 mm": ".030", "0.06 mm": ".060",
    # Feed coarse
    "3-4 mm/rev (low)": "Low", "5-6 mm/rev (med)": "Med", "7-8 mm/rev (high)": "Hi",
    # Feed (fine-grained)
    "3 mm/rev": "3mm", "4 mm/rev": "4mm", "5 mm/rev": "5mm",
    "6 mm/rev": "6mm", "7 mm/rev": "7mm", "8 mm/rev": "8mm",
    # Roughness
    "Smooth (Ra<0.7)": "Smt", "Medium (0.7-1.0)": "Med", "Rough (Ra>1.0)": "Rgh",
}


def short(class_names, label):
    full = class_names[label]
    return SHORT_NAMES.get(full, full[:4])


def _window_num(filename):
    """window_preds.csv 'filename' is e.g. 'run12_w3.png' -- returns 3."""
    return int(Path(filename).stem.rsplit("_w", 1)[1])


def load_window_preds(csv_path, num_classes):
    """Returns ({run: [(window_num, pred_label, prob_vector), ...]}, {run: true_label}),
    windows sorted within each run by window number."""
    df = pd.read_csv(csv_path)
    prob_cols = [f"prob_{c}" for c in range(num_classes)]
    run_windows, run_label = {}, {}
    for _, row in df.iterrows():
        run = row["run"]
        run_windows.setdefault(run, []).append((
            _window_num(row["filename"]), int(row["pred_label"]),
            row[prob_cols].to_numpy(dtype=float),
        ))
        run_label[run] = int(row["true_label"])
    for run in run_windows:
        run_windows[run].sort(key=lambda x: x[0])
    return run_windows, run_label


def build_results(run_windows, run_label):
    """Returns a list of per-run result dicts (hard + soft vote), sorted by run."""
    results = []
    for run in sorted(run_windows.keys()):
        entries = run_windows[run]
        window_preds = [p for _, p, _ in entries]
        probs = np.stack([pr for _, _, pr in entries])
        true_lbl = run_label[run]

        hard = Counter(window_preds).most_common(1)[0][0]
        soft = int(probs.mean(axis=0).argmax())

        results.append({
            "run": run, "true_label": true_lbl, "window_preds": window_preds,
            "hard_vote": hard, "hard_correct": hard == true_lbl,
            "soft_vote": soft, "soft_correct": soft == true_lbl,
        })
    return results


def _summary(results):
    n_runs = len(results)
    n_hard = sum(r["hard_correct"] for r in results)
    n_soft = sum(r["soft_correct"] for r in results)
    all_preds  = [p for r in results for p in r["window_preds"]]
    all_labels = [r["true_label"] for r in results for _ in r["window_preds"]]
    win_correct = sum(p == l for p, l in zip(all_preds, all_labels))
    return win_correct, len(all_preds), n_hard, n_soft, n_runs


def class_metrics(results, class_names, vote_key="soft_vote"):
    """Per-class precision/recall/F1/support at run level (default: soft-vote
    predictions), plus macro-averaged totals. zero_division=0 so classes with
    no predicted/true instances in a small test split report 0 rather than
    raising/warning -- run counts here are small enough (9-15) for that to
    happen routinely."""
    labels = sorted(class_names.keys())
    y_true = [r["true_label"] for r in results]
    y_pred = [r[vote_key] for r in results]
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0)
    per_class = [
        {"label": lbl, "name": class_names[lbl], "precision": precision[i],
         "recall": recall[i], "f1": f1[i], "support": int(support[i])}
        for i, lbl in enumerate(labels)
    ]
    macro = {
        "precision": float(np.mean(precision)), "recall": float(np.mean(recall)),
        "f1": float(np.mean(f1)),
    }
    return per_class, macro


def print_table(results, class_names, n_windows):
    run_w  = max(6, max(len(str(r["run"])) for r in results))
    w_cols = "  ".join(f"w{i+1:>2}" for i in range(n_windows))
    header = f"  {'Run':<{run_w}}  {'True':<8}  {w_cols}  {'Hard':<8}  {'Soft':<8}  OK"
    sep    = "  " + "-" * (len(header) - 2)
    print(header)
    print(sep)
    for r in results:
        true_s = short(class_names, r["true_label"])
        wins_s = "  ".join(f"{short(class_names, p):>4}" for p in r["window_preds"])
        hard_s = short(class_names, r["hard_vote"])
        soft_s = short(class_names, r["soft_vote"])
        ok_s   = "OK" if r["hard_correct"] else ("~ " if r["soft_correct"] else "X ")
        print(f"  {r['run']:<{run_w}}  {true_s:<8}  {wins_s}  {hard_s:<8}  {soft_s:<8}  {ok_s}")
    print(sep)

    win_correct, n_windows_total, n_hard, n_soft, n_runs = _summary(results)
    print(f"  Window accuracy       : {win_correct}/{n_windows_total} = {win_correct/n_windows_total*100:.1f}%")
    print(f"  Run hard-vote accuracy: {n_hard}/{n_runs} = {n_hard/n_runs*100:.1f}%")
    print(f"  Run soft-vote accuracy: {n_soft}/{n_runs} = {n_soft/n_runs*100:.1f}%")

    per_class, macro = class_metrics(results, class_names)
    print(f"\n  Per-class report (run-level, soft-vote):")
    print(f"  {'Class':<10}  {'Precision':>9}  {'Recall':>9}  {'F1':>9}  {'Support':>7}")
    for c in per_class:
        print(f"  {c['name']:<10}  {c['precision']:>9.3f}  {c['recall']:>9.3f}  {c['f1']:>9.3f}  {c['support']:>7}")
    print(f"  {'macro avg':<10}  {macro['precision']:>9.3f}  {macro['recall']:>9.3f}  {macro['f1']:>9.3f}")


def to_markdown(results, class_names, model_name, target, scalo_tag, arch, n_windows):
    w_headers = " | ".join(f"w{i+1}" for i in range(n_windows))
    lines = [
        f"### {model_name}  |  target={target}  |  scalogram={scalo_tag}  |  arch={arch}",
        "",
        f"| Run | True | {w_headers} | Hard | Soft | OK |",
        "|-----|------|" + "|".join(["----"] * n_windows) + "|------|------|----|",
    ]
    for r in results:
        true_s = short(class_names, r["true_label"])
        wins_s = " | ".join(short(class_names, p) for p in r["window_preds"])
        hard_s = short(class_names, r["hard_vote"])
        soft_s = short(class_names, r["soft_vote"])
        ok_s   = "Y" if r["hard_correct"] else ("~" if r["soft_correct"] else "N")
        lines.append(f"| {r['run']} | {true_s} | {wins_s} | {hard_s} | {soft_s} | {ok_s} |")

    win_correct, n_windows_total, n_hard, n_soft, n_runs = _summary(results)
    lines += [
        "",
        f"Window accuracy: **{win_correct/n_windows_total*100:.1f}%** ({win_correct}/{n_windows_total})",
        f"Run hard-vote accuracy: **{n_hard/n_runs*100:.1f}%** ({n_hard}/{n_runs})",
        f"Run soft-vote accuracy: **{n_soft/n_runs*100:.1f}%** ({n_soft}/{n_runs})",
    ]

    per_class, macro = class_metrics(results, class_names)
    lines += [
        "",
        "Per-class report (run-level, soft-vote):",
        "",
        "| Class | Precision | Recall | F1 | Support |",
        "|-------|-----------|--------|----|---------|",
    ]
    for c in per_class:
        lines.append(f"| {c['name']} | {c['precision']:.3f} | {c['recall']:.3f} | {c['f1']:.3f} | {c['support']} |")
    lines.append(f"| **macro avg** | **{macro['precision']:.3f}** | **{macro['recall']:.3f}** | **{macro['f1']:.3f}** | |")
    return "\n".join(lines)


def eval_one(target, img_dir, arch, lr, run_tag="", save_md=None, regenerate=False, verbose=True):
    """Evaluate one trained checkpoint. Returns (results, markdown_string)."""
    spec        = TARGETS[target]
    class_names = spec["class_names"]
    img_dir     = Path(img_dir)
    scalo_tag   = img_dir.name.replace("scalograms_", "")
    model_dir   = ROOT / "cnn_model" / f"models_{target}_{scalo_tag}"

    tag_suffix = f"_{run_tag}" if run_tag else ""
    stem       = f"{arch}_lr{lr:g}{tag_suffix}"
    hist_path  = model_dir / f"{stem}_history.json"
    csv_path   = model_dir / f"{stem}_window_preds.csv"

    if not hist_path.exists():
        raise FileNotFoundError(f"No history.json found: {hist_path}")

    if regenerate or not csv_path.exists():
        ok = process_one_checkpoint(model_dir, target, hist_path, only_missing=not regenerate)
        if ok is False:
            raise RuntimeError(f"Inference failed for {stem} -- see error printed above")
        if not csv_path.exists():
            raise RuntimeError(f"Could not produce {csv_path.name} (missing checkpoint .pt?)")

    run_windows, run_label = load_window_preds(csv_path, spec["num_classes"])
    if not run_windows:
        raise RuntimeError(f"No window predictions found in {csv_path}")

    results   = build_results(run_windows, run_label)
    n_windows = max(len(r["window_preds"]) for r in results)

    if verbose:
        print(f"\nModel : {stem}")
        print(f"Target: {target}  |  Scalogram: {img_dir.name}  |  Arch: {arch}\n")
        print_table(results, class_names, n_windows)
        print(f"\nClass legend:")
        for k, v in sorted(class_names.items()):
            print(f"  {short(class_names, k)} = {v}")

    md = to_markdown(results, class_names, stem, target, scalo_tag, arch, n_windows)
    if save_md:
        save_md = Path(save_md)
        save_md.parent.mkdir(parents=True, exist_ok=True)
        save_md.write_text(md, encoding="utf-8")
        if verbose:
            print(f"\nMarkdown saved to: {save_md}")
    return results, md


def run_all(target_filter, regenerate, summary_csv_path):
    """Batch mode: evaluates every trained checkpoint under
    cnn_model/models_<target>_*/ (optionally restricted to one target),
    writing a <stem>_detailed.md next to each checkpoint (same as the
    single-checkpoint path) plus one combined summary CSV in this directory.

    Reads arch/lr/img_dir/run_tag straight out of each checkpoint's own
    *_history.json (written by cnn_train_32x3.py) rather than re-deriving
    them from the filename -- history.json's own tag construction
    (f"{arch}_lr{lr:g}{'_'+run_tag if run_tag else ''}") is exactly what
    produced that filename in the first place, so this is guaranteed
    consistent and needs no fragile stem-parsing."""
    cnn_model_dir = ROOT / "cnn_model"
    target_keys = list(TARGETS.keys())

    def _owning_target(dir_name):
        # "feed" is a strict prefix of "feed_coarse" (models_feed_coarse_32x3
        # starts with "models_feed_"), so a naive per-target glob/regex loop
        # double-matches those dirs under both targets. Instead resolve each
        # directory to its single longest (most specific) matching target.
        matches = [t for t in target_keys
                   if dir_name == f"models_{t}" or dir_name.startswith(f"models_{t}_")]
        return max(matches, key=len) if matches else None

    rows = []
    n_ok = n_failed = n_skipped = 0
    all_dirs = sorted(d for d in cnn_model_dir.glob("models_*") if d.is_dir())
    for model_dir in all_dirs:
        target = _owning_target(model_dir.name)
        if target is None or (target_filter and target != target_filter):
            continue
        for hist_path in sorted(model_dir.glob("*_history.json")):
                stem = hist_path.name.replace("_history.json", "")
                try:
                    hist = json.loads(hist_path.read_text())
                except Exception as e:
                    print(f"  SKIP {model_dir.name}/{stem}: unreadable history.json ({e})")
                    n_skipped += 1
                    continue

                arch = hist.get("arch")
                lr = hist.get("lr")
                run_tag = hist.get("run_tag", "") or ""
                img_dir_name = Path(hist.get("img_dir", "")).name
                if not (arch and lr is not None and img_dir_name):
                    print(f"  SKIP {model_dir.name}/{stem}: history.json missing arch/lr/img_dir")
                    n_skipped += 1
                    continue

                save_md = model_dir / f"{stem}_detailed.md"
                try:
                    results, _ = eval_one(target, ROOT / img_dir_name, arch, lr, run_tag=run_tag,
                                           save_md=save_md, regenerate=regenerate, verbose=False)
                except Exception as e:
                    print(f"  FAILED {model_dir.name}/{stem}: {e}")
                    n_failed += 1
                    continue

                win_correct, n_windows_total, n_hard, n_soft, n_runs = _summary(results)
                window_acc, hard_acc, soft_acc = (
                    win_correct / n_windows_total, n_hard / n_runs, n_soft / n_runs)
                spec = TARGETS[target]
                _, macro_soft = class_metrics(results, spec["class_names"], vote_key="soft_vote")
                _, macro_hard = class_metrics(results, spec["class_names"], vote_key="hard_vote")
                print(f"  OK {model_dir.name}/{stem}: "
                      f"window={window_acc:.3f}  hard={hard_acc:.3f}  soft={soft_acc:.3f}  "
                      f"soft_f1={macro_soft['f1']:.3f}")
                rows.append({
                    "target": target, "img_dir": img_dir_name, "arch": arch, "lr": lr,
                    "run_tag": run_tag, "n_runs": n_runs, "n_windows": n_windows_total,
                    "window_acc": round(window_acc, 4), "run_hard_acc": round(hard_acc, 4),
                    "run_soft_acc": round(soft_acc, 4),
                    "precision_macro_soft": round(macro_soft["precision"], 4),
                    "recall_macro_soft": round(macro_soft["recall"], 4),
                    "f1_macro_soft": round(macro_soft["f1"], 4),
                    "precision_macro_hard": round(macro_hard["precision"], 4),
                    "recall_macro_hard": round(macro_hard["recall"], 4),
                    "f1_macro_hard": round(macro_hard["f1"], 4),
                    "detailed_md": str(save_md.relative_to(ROOT)),
                })
                n_ok += 1

    summary_csv = Path(summary_csv_path) if summary_csv_path else ROOT / "eval_detailed_summary.csv"
    pd.DataFrame(rows).to_csv(summary_csv, index=False)
    print(f"\n{n_ok} evaluated, {n_failed} failed, {n_skipped} skipped.")
    print(f"Summary CSV: {summary_csv}")


def main():
    parser = argparse.ArgumentParser(
        description="Per-window evaluation for a trained End Milling 32x3/32x12 parameter model.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--target", default=None, choices=list(TARGETS.keys()),
                        help="Required unless --all is given. With --all, optionally filters to one target.")
    parser.add_argument("--img_dir", default=None,
                        help="e.g. scalograms_32x3, scalograms_32x12_feedopt. Required unless --all.")
    parser.add_argument("--arch", default=None,
                        choices=["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny", "mobilenet_v3_large"],
                        help="Required unless --all.")
    parser.add_argument("--lr", type=float, default=None,
                        help="Used to locate the checkpoint (models_<target>_<tag>/<arch>_lr<lr>[_<run_tag>]_*). "
                             "Required unless --all.")
    parser.add_argument("--run_tag", default="",
                        help="Optional suffix matching the training run's --run_tag, e.g. 'smote', 'cascade_smote'")
    parser.add_argument("--all", action="store_true",
                        help="Batch mode: evaluate every trained checkpoint under cnn_model/models_<target>_*/ "
                             "(optionally filtered by --target), writing a <stem>_detailed.md next to each "
                             "checkpoint plus one combined eval_detailed_summary.csv in this directory.")
    parser.add_argument("--summary_csv", default=None,
                        help="--all only: path for the combined summary CSV (default: eval_detailed_summary.csv)")
    parser.add_argument("--regenerate", action="store_true",
                        help="Re-run inference even if a *_window_preds.csv already exists")
    parser.add_argument("--save_md", default=None,
                        help="Path to save markdown output (default: cnn_model/models_<target>_<tag>/<stem>_detailed.md). "
                             "Ignored with --all.")
    args = parser.parse_args()

    if args.all:
        run_all(args.target, args.regenerate, args.summary_csv)
        return

    if not (args.target and args.img_dir and args.arch and args.lr is not None):
        parser.error("--target, --img_dir, --arch, and --lr are all required unless --all is given")

    img_dir    = Path(args.img_dir)
    scalo_tag  = img_dir.name.replace("scalograms_", "")
    tag_suffix = f"_{args.run_tag}" if args.run_tag else ""
    stem       = f"{args.arch}_lr{args.lr:g}{tag_suffix}"

    save_md = args.save_md
    if save_md is None:
        save_md = ROOT / "cnn_model" / f"models_{args.target}_{scalo_tag}" / f"{stem}_detailed.md"

    eval_one(args.target, img_dir, args.arch, args.lr, run_tag=args.run_tag,
             save_md=save_md, regenerate=args.regenerate)


if __name__ == "__main__":
    main()
