"""
smote_ses_4ch.py — Synthetic Pipeline D (4-channel raw + SES) scalogram
generation via signal-space SMOTE.

Interpolates between same-class training signals, computes 4-channel CWT
(ai4_raw, ai6_raw, ses_ai4, ses_ai6), and saves as .npy arrays
(4, IMG_SIZE, IMG_SIZE) float32.  Writes a CSV so cnn_train_hilbert.py
can pick up the synthetics with --smote.

Uses the same balanced test splits as cnn_train_hilbert.py to avoid leakage.

Usage (from project root):
    python cnn_model/smote_ses_4ch.py --data_dir data --output_dir scalograms_ses_4ch_10w --target speed        --n_windows 10
    python cnn_model/smote_ses_4ch.py --data_dir data --output_dir scalograms_ses_4ch_10w --target doc          --n_windows 10
    python cnn_model/smote_ses_4ch.py --data_dir data --output_dir scalograms_ses_4ch_10w --target feed_coarse  --n_windows 10
    python cnn_model/smote_ses_4ch.py --data_dir data --output_dir scalograms_ses_4ch_10w --target roughness    --n_windows 10
"""
import argparse
import csv
import itertools
import random
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from scalogram import FS, DOWNSAMPLE, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE
from scalogram_ses_4ch import CHANNELS, compute_four_powers, powers_to_array
from cnn_train import (
    SPEED_LABELS, FEED_TEST_RUNS, FEED_COARSE_LABELS,
    DOC_LABELS, RA_LABELS, RA_TEST_RUNS,
)
from cnn_train_hilbert import SPEED_TEST_RUNS_H, DOC_TEST_RUNS_H

SEED = 42

TARGET_CONFIG = {
    "speed":       (SPEED_LABELS,       SPEED_TEST_RUNS_H, "smote_d4s",  "smote_h_speed_labels.csv"),
    "doc":         (DOC_LABELS,         DOC_TEST_RUNS_H,   "smote_d4d",  "smote_h_doc_labels.csv"),
    "feed_coarse": (FEED_COARSE_LABELS, FEED_TEST_RUNS,    "smote_d4fc", "smote_h_feed_coarse_labels.csv"),
    "roughness":   (RA_LABELS,          RA_TEST_RUNS,      "smote_d4r",  "smote_h_roughness_labels.csv"),
}


def load_signal(csv_path):
    df = pd.read_csv(csv_path)
    return {ch: df[ch].values.astype(np.float32) for ch in CHANNELS}


def interpolate_signals(sig_a, sig_b, alpha):
    return {ch: alpha * sig_a[ch] + (1.0 - alpha) * sig_b[ch] for ch in CHANNELS}


def save_windows_npy(signal_dict, stem, output_dir, n_windows,
                     fs_eff, f_min, f_max, n_freqs, sigma, img_size,
                     env_f_low=None, env_f_high=None):
    """Generate n_windows 4-channel .npy files from an interpolated signal dict."""
    N = len(next(iter(signal_dict.values())))
    window_size = N // 2
    hop = max(1, (N - window_size) // (n_windows - 1)) if n_windows > 1 else N

    saved = []
    for w in range(n_windows):
        start = w * hop
        end   = start + window_size
        if end > N:
            end   = N
            start = max(0, end - window_size)

        df_win = pd.DataFrame({ch: signal_dict[ch][start:end] for ch in CHANNELS})
        powers = compute_four_powers(df_win, fs_eff, f_min, f_max, n_freqs, sigma,
                                     DOWNSAMPLE, env_f_low, env_f_high)
        arr    = powers_to_array(powers, img_size)
        npy_out = output_dir / f"{stem}_w{w + 1}.npy"
        np.save(npy_out, arr)
        saved.append(npy_out)
    return saved


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline D: Generate synthetic 4-channel SES scalograms via signal SMOTE.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--data_dir",     required=True,  help="Raw CSV directory")
    parser.add_argument("--output_dir",   required=True,  help="4-ch .npy scalogram directory")
    parser.add_argument("--target",       default="speed", choices=list(TARGET_CONFIG.keys()))
    parser.add_argument("--n_synthetic",  type=int, default=4,
                        help="Synthetic interpolations per same-class run pair")
    parser.add_argument("--n_windows",    type=int, default=10,
                        help="Windows per synthetic run (must match scalogram_ses_4ch.py)")
    parser.add_argument("--target_count", type=int, default=None,
                        help="Override per-class target run count (default: majority class size)")
    parser.add_argument("--env_f_low",    type=float, default=None)
    parser.add_argument("--env_f_high",   type=float, default=None)
    args = parser.parse_args()

    random.seed(SEED)
    np.random.seed(SEED)

    data_dir   = Path(args.data_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fs_eff = FS // DOWNSAMPLE
    all_labels, test_runs, prefix, csv_name = TARGET_CONFIG[args.target]

    runs_by_class = {}
    for run, lbl in all_labels.items():
        if run not in test_runs:
            runs_by_class.setdefault(lbl, []).append(run)

    max_count = args.target_count or max(len(v) for v in runs_by_class.values())

    print(f"Target: {args.target}  |  Majority class size: {max_count}")
    for c in sorted(runs_by_class):
        needed = max_count - len(runs_by_class[c])
        status = "majority" if needed == 0 else f"need +{needed}"
        print(f"  class {c}: {len(runs_by_class[c])} runs  [{status}]")

    label_rows   = []
    total_images = 0

    for cls in sorted(runs_by_class):
        runs = runs_by_class[cls]
        if len(runs) >= max_count:
            continue
        if len(runs) < 2:
            print(f"\nClass {cls}: only 1 training run — cannot interpolate, skipping")
            continue

        print(f"\nClass {cls}: generating synthetic runs ...")
        class_signals = {run: load_signal(data_dir / f"{run}.csv") for run in runs}

        needed     = max_count - len(runs)
        pairs      = list(itertools.combinations(runs, 2))
        pair_cycle = itertools.cycle(pairs)

        for idx in range(needed):
            run_a, run_b = next(pair_cycle)
            alpha = random.uniform(0.1, 0.9)
            syn   = interpolate_signals(class_signals[run_a], class_signals[run_b], alpha)
            stem  = f"{prefix}{cls}_{idx}"

            save_windows_npy(
                syn, stem, output_dir, args.n_windows,
                fs_eff, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE,
                args.env_f_low, args.env_f_high,
            )
            label_rows.append({"run": stem, "label": cls,
                                "parent_a": run_a, "parent_b": run_b})
            total_images += args.n_windows
            print(f"  {stem}  alpha={alpha:.3f}  ({run_a} <-> {run_b})")

    lbl_path = output_dir / csv_name
    with open(lbl_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run", "label", "parent_a", "parent_b"])
        writer.writeheader()
        writer.writerows(label_rows)

    print(f"\n{len(label_rows)} synthetic runs -> {total_images} .npy files saved to {output_dir}/")
    print(f"Labels written to {lbl_path}")
    print("Train with: cnn_train_hilbert.py --img_dir <output_dir> --smote ...")


if __name__ == "__main__":
    main()
