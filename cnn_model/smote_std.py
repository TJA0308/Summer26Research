"""
smote_std.py — Synthetic Pipeline A scalogram generation via signal-space SMOTE.

Interpolates between same-class training signals, computes standard 2-channel
CWT (ai4_raw → R, ai6_raw → G, B=0) RGB PNGs matching scalograms_10w/ format,
and writes the CSV files that cnn_train.py auto-loads when --img_dir is set.

CSV names written (same as cnn_train.py expects):
    smote_speed_labels.csv
    smote_doc_labels.csv
    smote_roughness_labels.csv
    smote_feed_coarse_labels.csv

Usage (from project root):
    python cnn_model/smote_std.py --data_dir data --output_dir scalograms_10w --target speed        --n_windows 10
    python cnn_model/smote_std.py --data_dir data --output_dir scalograms_10w --target doc          --n_windows 10
    python cnn_model/smote_std.py --data_dir data --output_dir scalograms_10w --target roughness    --n_windows 10
    python cnn_model/smote_std.py --data_dir data --output_dir scalograms_10w --target feed_coarse  --n_windows 10
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
    FS, DOWNSAMPLE, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE,
)
from cnn_train import (
    SPEED_LABELS,       SPEED_TEST_RUNS,
    FEED_COARSE_LABELS, FEED_COARSE_TEST_RUNS,
    DOC_LABELS,         DOC_TEST_RUNS,
    RA_LABELS,          RA_TEST_RUNS,
)

SEED     = 42
CHANNELS = ["ai4", "ai6"]

TARGET_CONFIG = {
    "speed":       (SPEED_LABELS,       SPEED_TEST_RUNS,       "smote_as",  "smote_speed_labels.csv"),
    "doc":         (DOC_LABELS,         DOC_TEST_RUNS,         "smote_ad",  "smote_doc_labels.csv"),
    "roughness":   (RA_LABELS,          RA_TEST_RUNS,          "smote_ar",  "smote_roughness_labels.csv"),
    "feed_coarse": (FEED_COARSE_LABELS, FEED_COARSE_TEST_RUNS, "smote_afc", "smote_feed_coarse_labels.csv"),
}


def load_signal(csv_path):
    df = pd.read_csv(csv_path)
    return {ch: df[ch].values.astype(np.float32) for ch in CHANNELS}


def interpolate_signals(sig_a, sig_b, alpha):
    return {ch: alpha * sig_a[ch] + (1.0 - alpha) * sig_b[ch] for ch in CHANNELS}


def signal_to_powers_std(signal_dict, fs_eff, f_min, f_max, n_freqs, sigma):
    """Return [p_ai4, p_ai6] — Pipeline A raw CWT channels (R=ai4, G=ai6, B=0)."""
    powers = []
    for ch in CHANNELS:
        sig = signal_dict[ch].copy()
        sig -= sig.mean()
        pw, _ = analytic_morlet_cwt(sig, fs=fs_eff, n_freqs=n_freqs,
                                     f_min=f_min, f_max=f_max, sigma=sigma)
        powers.append(pw)
    return powers  # [p_ai4, p_ai6]


def save_windows(signal_dict, stem, output_dir, n_windows,
                 fs_eff, f_min, f_max, n_freqs, sigma, img_size):
    N           = len(signal_dict["ai4"])
    window_size = N // 2
    hop         = max(1, (N - window_size) // (n_windows - 1)) if n_windows > 1 else N

    for w in range(n_windows):
        start = w * hop
        end   = start + window_size
        if end > N:
            end   = N
            start = max(0, end - window_size)
        win    = {ch: signal_dict[ch][start:end] for ch in CHANNELS}
        powers = signal_to_powers_std(win, fs_eff, f_min, f_max, n_freqs, sigma)
        img    = build_rgb_image(powers, img_size)
        Image.fromarray(img).save(output_dir / f"{stem}_w{w + 1}.png")


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline A: Generate synthetic RGB CWT scalogram PNGs via signal-space SMOTE.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--data_dir",     required=True,  help="Raw CSV directory (data/)")
    parser.add_argument("--output_dir",   required=True,  help="Pipeline A scalogram directory (scalograms_10w/)")
    parser.add_argument("--target",       default="speed", choices=list(TARGET_CONFIG.keys()))
    parser.add_argument("--n_windows",    type=int, default=10,
                        help="Windows per synthetic run (must match scalogram.py)")
    parser.add_argument("--target_count", type=int, default=None,
                        help="Override per-class target run count (default: majority class size)")
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

    print(f"Target      : {args.target}")
    print(f"Test runs   : {len(test_runs)}  |  Majority class: {max_count} training runs")
    for c in sorted(runs_by_class):
        needed = max_count - len(runs_by_class[c])
        status = "majority" if needed == 0 else f"need +{needed}"
        print(f"  class {c}: {len(runs_by_class[c])} runs  [{status}]")

    label_rows   = []
    total_images = 0

    for cls in sorted(runs_by_class):
        runs = runs_by_class[cls]
        if len(runs) >= max_count:
            print(f"\nClass {cls}: already at majority — skipping")
            continue
        if len(runs) < 2:
            print(f"\nClass {cls}: only 1 training run — cannot interpolate, skipping")
            continue

        print(f"\nClass {cls}: generating {max_count - len(runs)} synthetic run(s) ...")
        class_signals = {run: load_signal(data_dir / f"{run}.csv") for run in runs}

        needed     = max_count - len(runs)
        pairs      = list(itertools.combinations(runs, 2))
        pair_cycle = itertools.cycle(pairs)

        for idx in range(needed):
            run_a, run_b = next(pair_cycle)
            alpha = random.uniform(0.1, 0.9)
            syn   = interpolate_signals(class_signals[run_a], class_signals[run_b], alpha)
            stem  = f"{prefix}{cls}_{idx}"

            save_windows(syn, stem, output_dir, args.n_windows,
                         fs_eff, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE)
            label_rows.append({"run": stem, "label": cls,
                                "parent_a": run_a, "parent_b": run_b})
            total_images += args.n_windows
            print(f"  {stem}  alpha={alpha:.3f}  ({run_a} <-> {run_b})")

    lbl_path = output_dir / csv_name
    with open(lbl_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["run", "label", "parent_a", "parent_b"])
        writer.writeheader()
        writer.writerows(label_rows)

    print(f"\n{len(label_rows)} synthetic runs -> {total_images} PNGs saved to {output_dir}/")
    print(f"Labels written to {lbl_path}")
    print("cnn_train.py will auto-load these on next run with --img_dir pointing here.")


if __name__ == "__main__":
    main()
