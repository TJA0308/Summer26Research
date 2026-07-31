"""
Quick ad-hoc ensembling of several already-trained configs' *_window_preds.csv
files, soft-voted per run then averaged across configs, to see whether
combining models beats any single config's run-level accuracy. Read-only:
does not retrain anything.

Usage:
    python ensemble_eval.py --target feed_coarse --dirs model_dir1/stem1 model_dir2/stem2 ...
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

HERE = Path(__file__).parent


def run_level_probs(csv_path: Path):
    df = pd.read_csv(csv_path)
    prob_cols = [c for c in df.columns if c.startswith("prob_")]
    grouped = df.groupby("run")
    run_probs = {}
    run_true = {}
    for run, g in grouped:
        run_probs[run] = g[prob_cols].to_numpy().mean(axis=0)
        run_true[run] = int(g["true_label"].iloc[0])
    return run_probs, run_true, len(prob_cols)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--paths", nargs="+", required=True,
                         help="Paths to *_window_preds.csv files to ensemble")
    parser.add_argument("--class_names", nargs="+", default=None,
                         help="Optional class names (in label-index order) for the precision/recall report")
    args = parser.parse_args()

    all_run_probs = []
    all_run_true = None
    for p in args.paths:
        csv_path = HERE / p
        run_probs, run_true, n_classes = run_level_probs(csv_path)
        all_run_probs.append(run_probs)
        if all_run_true is None:
            all_run_true = run_true
        else:
            assert set(run_true) == set(all_run_true), f"run set mismatch in {p}"
            for r in run_true:
                assert run_true[r] == all_run_true[r], f"label mismatch for {r} in {p}"

    runs = sorted(all_run_true.keys())
    n_correct = 0
    y_true, y_pred = [], []
    print(f"Ensembling {len(args.paths)} configs over {len(runs)} runs:")
    for r in runs:
        avg_prob = np.mean([rp[r] for rp in all_run_probs], axis=0)
        pred = int(np.argmax(avg_prob))
        true = all_run_true[r]
        ok = pred == true
        n_correct += ok
        y_true.append(true)
        y_pred.append(pred)
        print(f"  {r}: true={true} pred={pred} {'OK' if ok else 'WRONG'}  probs={np.round(avg_prob, 3)}")
    print(f"\nEnsemble run-level soft-vote accuracy: {n_correct}/{len(runs)} = {n_correct/len(runs):.4f}")

    labels = sorted(set(y_true) | set(y_pred))
    names = args.class_names if args.class_names else [str(l) for l in labels]
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0)
    print(f"\nPer-class report (ensemble, run-level soft-vote):")
    print(f"  {'Class':<10}  {'Precision':>9}  {'Recall':>9}  {'F1':>9}  {'Support':>7}")
    for i, lbl in enumerate(labels):
        print(f"  {names[i]:<10}  {precision[i]:>9.3f}  {recall[i]:>9.3f}  {f1[i]:>9.3f}  {support[i]:>7}")
    print(f"  {'macro avg':<10}  {np.mean(precision):>9.3f}  {np.mean(recall):>9.3f}  {np.mean(f1):>9.3f}")


if __name__ == "__main__":
    main()
