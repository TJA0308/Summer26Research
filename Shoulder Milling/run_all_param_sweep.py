"""
Runs all 48 cnn_train_param.py combinations (3 targets x 2 scalogram
folders x 4 backbones x 2 learning rates) sequentially and aggregates
each model's best window-level accuracy and run-level majority-vote
accuracy into one summary CSV.

Usage:
    python run_all_param_sweep.py                 # epochs=50 for every model
    python run_all_param_sweep.py --epochs 20      # shorter sweep
    python run_all_param_sweep.py --no_smote
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

TARGETS  = ["speed", "feed", "doc"]
IMG_DIRS = ["scalograms_32x12", "scalograms_32x3"]
ARCHS    = ["resnet18", "resnet50", "efficientnet_b0", "convnext_tiny"]
LRS      = ["1e-3", "1e-4"]

HERE = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--no_smote", action="store_true")
    args = parser.parse_args()

    combos = [
        (t, d, a, lr)
        for t in TARGETS
        for d in IMG_DIRS
        for a in ARCHS
        for lr in LRS
    ]
    print(f"Running {len(combos)} model combinations, {args.epochs} epochs each ...\n")

    results = []
    for i, (target, img_dir, arch, lr) in enumerate(combos, 1):
        scalo_tag = img_dir.replace("scalograms_", "")
        print(f"[{i}/{len(combos)}] target={target} scalogram={scalo_tag} arch={arch} lr={lr}")

        cmd = [
            sys.executable, str(HERE / "cnn_train_param.py"),
            "--target", target, "--img_dir", img_dir,
            "--arch", arch, "--lr", lr, "--epochs", str(args.epochs),
        ]
        if args.no_smote:
            cmd.append("--no_smote")

        proc = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"  FAILED:\n{proc.stderr[-1500:]}")
            results.append({
                "target": target, "scalogram": scalo_tag, "arch": arch, "lr": lr,
                "best_window_acc": None, "run_level_acc": None, "status": "failed",
            })
            continue

        hist_path = HERE / f"models_{target}_{scalo_tag}" / f"{arch}_lr{lr}_history.json"
        with open(hist_path) as f:
            hist = json.load(f)

        results.append({
            "target": target, "scalogram": scalo_tag, "arch": arch, "lr": lr,
            "best_window_acc": hist["best_window_acc"],
            "run_level_acc": hist["run_level_acc"],
            "best_epoch": hist["best_epoch"], "status": "ok",
        })
        print(f"  best_window_acc={hist['best_window_acc']:.3f}  "
              f"run_level_acc={hist['run_level_acc']:.3f}")

    df = pd.DataFrame(results)
    out_csv = HERE / "param_sweep_summary.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSummary written to {out_csv}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
