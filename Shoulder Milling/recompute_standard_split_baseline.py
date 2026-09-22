"""
Recomputes WINDOW-LEVEL standard-split accuracy from existing training
history JSONs, using the FINAL-epoch number instead of the best-test-
accuracy number those files were originally headlined with.

Why this exists: cnn_train_param.py used to save/report whichever epoch's
checkpoint had the highest TEST accuracy (`if te_acc > best_acc: save`),
then load that checkpoint for the run-level headline -- test-accuracy-driven
checkpoint selection, the same leakage mechanism that produced the
now-debunked 87.5% feed number (residual_preprocessing_readme.md). That bug
was fixed in cnn_train_param.py in this same session (final-epoch model is
now always what gets saved/reported for new runs), but ALL PRE-EXISTING
`*_history.json` files were written before the fix -- their "best_window_acc"
field is the inflated number.

Good news: every history JSON already stores the full per-epoch history, so
the honest final-epoch WINDOW accuracy (`history[-1]["te_acc"]`) is sitting
right there at zero extra compute -- no retraining needed for this part.

What this script does NOT fix: RUN-LEVEL majority-vote accuracy (the actual
headline metric in every appendix/writeup) required loading a specific
checkpoint and re-running inference, so it cannot be recovered from the JSON
alone -- those numbers must be re-earned by retraining with the fixed script
(cv_evaluate.py --split standard --models cnn does this per-target).

Usage:
    python recompute_standard_split_baseline.py
    python recompute_standard_split_baseline.py --target doc
"""
import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent


def scan(target_filter=None):
    rows = []
    for hist_path in sorted(ROOT.glob("models_*/*_history.json")):
        with open(hist_path) as f:
            d = json.load(f)

        target = d.get("target", "")
        if target_filter and target != target_filter:
            continue
        history = d.get("history", [])
        if not history:
            continue

        final = history[-1]
        old_best_acc = d.get("best_window_acc")   # only present in pre-fix files
        old_best_epoch = d.get("best_epoch")
        already_fixed = "final_window_acc" in d    # written by the post-fix script

        rows.append({
            "history_file": hist_path.relative_to(ROOT).as_posix(),
            "target": target,
            "scalogram": d.get("scalogram", ""),
            "arch": d.get("arch", ""),
            "lr": d.get("lr", ""),
            "run_tag": d.get("run_tag", ""),
            "split_id": d.get("split_id", ""),
            "conditioned": d.get("conditioned", False),
            "smote": d.get("smote", False),
            "epochs_run": len(history),
            "final_window_acc": final["te_acc"],
            "final_train_acc": final["tr_acc"],
            "old_best_window_acc_INFLATED": old_best_acc if not already_fixed else None,
            "old_best_epoch_INFLATED": old_best_epoch if not already_fixed else None,
            "inflation_pp": (round((old_best_acc - final["te_acc"]) * 100, 2)
                              if (old_best_acc is not None and not already_fixed) else None),
            "already_fixed_schema": already_fixed,
            "old_run_level_acc_STALE_CHECKPOINT": d.get("run_level_acc"),
        })
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", default=None, choices=[None, "speed", "feed", "doc", "roughness"])
    args = parser.parse_args()

    df = scan(args.target)
    if df.empty:
        print("No history JSONs found.")
        return

    out_path = ROOT / "corrected_standard_split_window_acc.csv"
    df.to_csv(out_path, index=False)
    print(f"Scanned {len(df)} history files -> {out_path.name}")

    inflated = df[df["inflation_pp"].notna()]
    if len(inflated):
        print(f"\n{len(inflated)} pre-fix files (test-accuracy-selected checkpoint):")
        print(f"  mean inflation : {inflated['inflation_pp'].mean():.2f} pp")
        print(f"  median inflation: {inflated['inflation_pp'].median():.2f} pp")
        print(f"  p90 inflation   : {inflated['inflation_pp'].quantile(0.9):.2f} pp")
        print(f"  median old best_epoch: {inflated['old_best_epoch_INFLATED'].median():.0f} "
              f"of {inflated['epochs_run'].median():.0f}")

    low_train_acc = df[df["final_train_acc"] < 0.95]
    if len(low_train_acc):
        print(f"\n{len(low_train_acc)} runs with final TRAIN acc < 0.95 "
              f"(possible under-training -- more epochs may still help, "
              f"see column 'final_train_acc'):")
        for _, r in low_train_acc.iterrows():
            print(f"  {r['history_file']:<70s} train_acc={r['final_train_acc']:.3f}")

    print(f"\n--- Corrected (final-epoch) WINDOW-level accuracy by target ---")
    for target, g in df.groupby("target"):
        print(f"  {target:<10s} n={len(g):<4d} mean_final_window_acc={g['final_window_acc'].mean():.3f}")

    print("\nNOTE: these are WINDOW-level numbers recovered for free from existing "
          "history JSONs. RUN-level majority-vote headline numbers (the ones actually "
          "quoted in the writeups/appendices) still need to be re-earned by retraining "
          "with the fixed cnn_train_param.py -- use "
          "'python cv_evaluate.py --target <t> --split standard --models cnn' per target.")


if __name__ == "__main__":
    main()
