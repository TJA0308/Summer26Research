"""
smote_signals.py — Synthetic scalogram generation via raw-signal SMOTE.

For each minority feed class, linearly interpolates between same-class
time-series signals at random alpha values, computes CWT, and saves
scalogram PNGs into the target scalogram directory. Also writes
smote_labels.csv so cnn_train.py can pick up the synthetic images.

Usage (from cnn_model/):
  python smote_signals.py \\
      --data_dir ../data \\
      --output_dir ../scalograms_10w \\
      --n_synthetic 4 \\
      --n_windows 10
"""

import argparse
import csv
import itertools
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from scalogram import (
    analytic_morlet_cwt, build_rgb_image,
    FS, DOWNSAMPLE, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE, CHANNELS,
)
from cnn_train import FEED_LABELS, FEED_TEST_RUNS, SPEED_LABELS, SPEED_TEST_RUNS, DOC_LABELS

SEED = 42


def load_signal(csv_path, channels):
    df = pd.read_csv(csv_path)
    return {ch: df[ch].values.astype(np.float32) for ch in channels}


def interpolate_signals(sig_a, sig_b, alpha):
    return {ch: alpha * sig_a[ch] + (1.0 - alpha) * sig_b[ch] for ch in sig_a}


def signal_to_powers(signal_dict, downsample, fs_eff, f_min, f_max, n_freqs, sigma):
    powers = []
    for ch in CHANNELS:
        sig = signal_dict[ch][::downsample]
        sig = sig - sig.mean()
        power, _ = analytic_morlet_cwt(
            sig, fs=fs_eff, n_freqs=n_freqs, f_min=f_min, f_max=f_max, sigma=sigma
        )
        powers.append(power)
    return powers


def save_windows(signal_dict, stem, output_dir, n_windows,
                 downsample, fs_eff, f_min, f_max, n_freqs, sigma, img_size,
                 freq_interleave=False):
    """
    Generate n_windows scalogram images from signal_dict.
    freq_interleave=True: compute CWT on full signal, slice every n-th frequency row.
    freq_interleave=False: split into overlapping half-signal time windows.
    """
    if freq_interleave and n_windows > 1:
        full_powers = signal_to_powers(signal_dict, downsample, fs_eff, f_min, f_max, n_freqs, sigma)
        for w in range(n_windows):
            powers = [p[w::n_windows, :] for p in full_powers]
            img    = build_rgb_image(powers, img_size)
            Image.fromarray(img).save(output_dir / f"{stem}_w{w + 1}.png")
        return

    N = len(next(iter(signal_dict.values())))
    window_size = N // 2
    hop = max(1, (N - window_size) // (n_windows - 1)) if n_windows > 1 else N

    for w in range(n_windows):
        start = w * hop
        end   = start + window_size
        if end > N:
            end   = N
            start = max(0, end - window_size)

        win    = {ch: signal_dict[ch][start:end] for ch in signal_dict}
        powers = signal_to_powers(win, downsample, fs_eff, f_min, f_max, n_freqs, sigma)
        img    = build_rgb_image(powers, img_size)
        Image.fromarray(img).save(output_dir / f"{stem}_w{w + 1}.png")


def main():
    parser = argparse.ArgumentParser(
        description="Generate synthetic scalogram images via signal-space SMOTE."
    )
    parser.add_argument("--data_dir",     required=True,
                        help="Folder of raw CSV files (run1.csv ... run45.csv)")
    parser.add_argument("--output_dir",   required=True,
                        help="Scalogram image folder to write synthetic PNGs into")
    parser.add_argument("--n_synthetic",  type=int, default=4,
                        help="Synthetic interpolations to generate per same-class run pair")
    parser.add_argument("--n_windows",    type=int, default=10,
                        help="Windows per synthetic run (must match --n_windows in scalogram.py)")
    parser.add_argument("--target",         default="feed", choices=["feed", "speed"],
                        help="Which prediction target to generate synthetics for")
    parser.add_argument("--target_count",   type=int, default=None,
                        help="Override per-class target run count (default: majority class size)")
    parser.add_argument("--freq_interleave", action="store_true",
                        help="Interleave frequency rows across windows instead of time windowing")
    args = parser.parse_args()

    random.seed(SEED)
    np.random.seed(SEED)

    data_dir   = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fs_eff = FS // DOWNSAMPLE

    # Select label map and test set based on target
    if args.target == "speed":
        all_labels = SPEED_LABELS
        test_runs  = SPEED_TEST_RUNS
        csv_name   = "smote_speed_labels.csv"
        csv_fields = ["run", "label", "parent_a", "parent_b"]
    else:
        all_labels = FEED_LABELS
        test_runs  = FEED_TEST_RUNS
        csv_name   = "smote_labels.csv"
        csv_fields = ["run", "label", "speed", "doc", "parent_a", "parent_b"]

    # Build class -> training-run list (exclude test runs)
    runs_by_class = {}
    for run, lbl in all_labels.items():
        if run not in test_runs:
            runs_by_class.setdefault(lbl, []).append(run)

    max_count = args.target_count if args.target_count else max(len(v) for v in runs_by_class.values())
    print("Class distribution (training runs):")
    for c in sorted(runs_by_class):
        status = "majority" if len(runs_by_class[c]) == max_count else f"need +{max_count - len(runs_by_class[c])}"
        print(f"  class {c}: {len(runs_by_class[c])} runs  [{status}]  {runs_by_class[c]}")
    print(f"Majority size: {max_count} runs\n")

    label_rows   = []
    total_images = 0

    for cls in sorted(runs_by_class):
        runs = runs_by_class[cls]
        if len(runs) >= max_count:
            continue
        if len(runs) < 2:
            print(f"Class {cls}: only 1 training run -- cannot interpolate, skipping")
            continue

        print(f"Class {cls}: generating synthetic runs ...")

        class_signals = {
            run: load_signal(data_dir / f"{run}.csv", CHANNELS)
            for run in runs
        }

        needed     = max_count - len(runs)
        pairs      = list(itertools.combinations(runs, 2))
        pair_cycle = itertools.cycle(pairs)
        # Generate exactly `needed` synthetics, cycling through pairs evenly
        for idx in range(needed):
            run_a, run_b = next(pair_cycle)
            alpha = random.uniform(0.1, 0.9)
            syn   = interpolate_signals(class_signals[run_a], class_signals[run_b], alpha)
            prefix = "smote_s" if args.target == "speed" else "smote_f"
            stem  = f"{prefix}{cls}_{idx}"

            save_windows(
                syn, stem, output_dir, args.n_windows,
                DOWNSAMPLE, fs_eff, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE,
                freq_interleave=args.freq_interleave,
            )
            if args.target == "speed":
                label_rows.append({"run": stem, "label": cls,
                                   "parent_a": run_a, "parent_b": run_b})
            else:
                dom = run_a if alpha >= 0.5 else run_b
                label_rows.append({
                    "run":      stem,
                    "label":    cls,
                    "speed":    SPEED_LABELS[dom],
                    "doc":      DOC_LABELS[dom],
                    "parent_a": run_a,
                    "parent_b": run_b,
                })
            total_images += args.n_windows
            print(f"  {stem}  alpha={alpha:.3f}  ({run_a} <-> {run_b})")

    lbl_path = output_dir / csv_name
    with open(lbl_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(label_rows)

    print(f"\n{len(label_rows)} synthetic runs -> {total_images} images saved to {output_dir}/")
    print(f"Labels written to {lbl_path}")
    print("Run cnn_train.py with the same --img_dir to use these automatically.")


if __name__ == "__main__":
    main()
