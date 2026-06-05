"""
SES-RGB scalogram generator: 3-channel PNG where each channel is a CWT of a
different signal representation, all fed through the same Morlet CWT pipeline
as scalogram.py so the output is drop-in compatible with cnn_train.py.

Channel layout (R / G / B):
    R : CWT of raw ai4            (same as Pipeline A, reference)
    G : CWT of SES(ai4)           (squared-envelope CWT, demodulated ai4)
    B : CWT of SES(ai6)           (squared-envelope CWT, demodulated ai6)

This creates "Pipeline C": SES information encoded directly in a standard
224x224 RGB PNG that any ImageNet-pretrained backbone can read without
modifying the first convolutional layer.

Usage (run from project root):
    python cnn_model/scalogram_ses_rgb.py \\
        --input_dir data \\
        --output_dir scalograms_ses_rgb_10w \\
        --n_windows 10

Train with the standard script (identical to Pipeline A):
    python cnn_model/cnn_train.py \\
        --img_dir scalograms_ses_rgb_10w \\
        --target speed --backbone resnet18 --epochs 30 \\
        --lr 1e-4 --augment light --optimizer adamw --split balanced
"""

import argparse
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from scalogram import (
    FS, DOWNSAMPLE, F_MIN, F_MAX, N_FREQS, SIGMA, IMG_SIZE,
    TIME_COL, analytic_morlet_cwt, power_to_uint8, build_rgb_image,
)
from hilbert_envelope import compute_envelope


def compute_powers_ses(df, fs_eff, f_min, f_max, n_freqs, sigma, downsample,
                       env_f_low=None, env_f_high=None):
    """
    Return three CWT power maps for one window DataFrame:
        [0] raw ai4   — same as Pipeline A
        [1] SES(ai4)  — CWT of |H{ai4}|^2
        [2] SES(ai6)  — CWT of |H{ai6}|^2
    """
    # R channel: raw ai4 CWT
    sig_raw = df["ai4"].values[::downsample].astype(np.float32)
    sig_raw -= sig_raw.mean()
    p_raw, _ = analytic_morlet_cwt(sig_raw, fs=fs_eff, n_freqs=n_freqs,
                                    f_min=f_min, f_max=f_max, sigma=sigma)

    # G channel: SES(ai4) CWT
    sig_ai4 = df["ai4"].values[::downsample].astype(np.float32)
    ses_ai4 = compute_envelope(sig_ai4, fs=fs_eff,
                               f_low=env_f_low, f_high=env_f_high) ** 2
    p_ses4, _ = analytic_morlet_cwt(ses_ai4, fs=fs_eff, n_freqs=n_freqs,
                                     f_min=f_min, f_max=f_max, sigma=sigma)

    # B channel: SES(ai6) CWT
    sig_ai6 = df["ai6"].values[::downsample].astype(np.float32)
    ses_ai6 = compute_envelope(sig_ai6, fs=fs_eff,
                               f_low=env_f_low, f_high=env_f_high) ** 2
    p_ses6, _ = analytic_morlet_cwt(ses_ai6, fs=fs_eff, n_freqs=n_freqs,
                                     f_min=f_min, f_max=f_max, sigma=sigma)

    return [p_raw, p_ses4, p_ses6]


def process_csv(csv_path, output_dir, fs=FS, downsample=DOWNSAMPLE,
                f_min=F_MIN, f_max=F_MAX, n_freqs=N_FREQS, sigma=SIGMA,
                img_size=IMG_SIZE, n_windows=1, global_ranges=None,
                env_f_low=None, env_f_high=None):
    stem = csv_path.stem
    df   = pd.read_csv(csv_path)

    required = [TIME_COL, "ai4", "ai6"]
    missing  = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"{csv_path.name}: missing columns {missing}. "
                         f"Available: {df.columns.tolist()}")

    fs_eff    = fs // downsample
    f_max_use = f_max if f_max is not None else fs_eff / 2.5
    df        = df[[TIME_COL, "ai4", "ai6"]]
    N         = len(df)

    print(f"  {csv_path.name} ({N} samples) …", end=" ", flush=True)

    def _save_window(df_win, suffix):
        powers = compute_powers_ses(df_win, fs_eff, f_min, f_max_use,
                                    n_freqs, sigma, downsample,
                                    env_f_low, env_f_high)
        img = build_rgb_image(powers, img_size, global_ranges=global_ranges)
        out = output_dir / f"{stem}{suffix}.png"
        Image.fromarray(img).save(out)
        print(f"-> {out.name}", end=" ", flush=True)
        return out

    saved = []
    if n_windows == 1:
        saved.append(_save_window(df, ""))
        print()
        return saved

    window_size = N // 2
    hop         = max(1, (N - window_size) // (n_windows - 1)) if n_windows > 1 else N
    for w in range(n_windows):
        start  = w * hop
        end    = start + window_size
        if end > N:
            end   = N
            start = max(0, end - window_size)
        df_win = df.iloc[start:end].reset_index(drop=True)
        print(f"\n    w{w + 1} [{start}:{end}]", end=" ")
        saved.append(_save_window(df_win, f"_w{w + 1}"))

    print()
    return saved


def main():
    parser = argparse.ArgumentParser(
        description="Generate SES-RGB scalograms: R=CWT(raw ai4), G=CWT(SES ai4), B=CWT(SES ai6).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input_dir",  required=True,  help="Directory of raw CSV files")
    parser.add_argument("--output_dir", required=True,  help="Where to save PNG scalograms")
    parser.add_argument("--single",     default=None,   help="Process one CSV file by name")
    parser.add_argument("--fs",         type=int,   default=FS)
    parser.add_argument("--downsample", type=int,   default=DOWNSAMPLE)
    parser.add_argument("--f_min",      type=float, default=F_MIN)
    parser.add_argument("--f_max",      type=float, default=F_MAX)
    parser.add_argument("--n_freqs",    type=int,   default=N_FREQS)
    parser.add_argument("--sigma",      type=float, default=SIGMA)
    parser.add_argument("--img_size",   type=int,   default=IMG_SIZE)
    parser.add_argument("--n_windows",  type=int,   default=1,
                        help="Overlapping time windows per run (same as scalogram.py)")
    parser.add_argument("--env_f_low",  type=float, default=None,
                        help="Bandpass lower cutoff Hz before Hilbert (e.g. 25 for tooth-pass)")
    parser.add_argument("--env_f_high", type=float, default=None,
                        help="Bandpass upper cutoff Hz before Hilbert")
    args = parser.parse_args()

    input_dir  = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_files = ([input_dir / args.single] if args.single
                 else sorted(input_dir.glob("*.csv")))
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return

    fs_eff = args.fs // args.downsample

    print(f"\n{'='*64}")
    print(f"  SES-RGB CWT Scalogram Generator (Pipeline C)")
    print(f"{'='*64}")
    print(f"  Input    : {input_dir}  ({len(csv_files)} files)")
    print(f"  Output   : {output_dir}")
    print(f"  Format   : 3-channel RGB PNG, {args.img_size}x{args.img_size}")
    print(f"  Fs       : {args.fs} Hz -> {fs_eff} Hz  ({args.downsample}x downsample)")
    print(f"  Freqs    : {args.f_min}-{args.f_max} Hz  ({args.n_freqs} bins)")
    print(f"  Sigma    : {args.sigma}  |  Windows: {args.n_windows}")
    print(f"  R channel: CWT(raw ai4)")
    print(f"  G channel: CWT(SES ai4)  [|H{{ai4}}|^2]")
    print(f"  B channel: CWT(SES ai6)  [|H{{ai6}}|^2]")
    if args.env_f_low or args.env_f_high:
        band = f"{args.env_f_low or 'DC'} – {args.env_f_high or 'Nyquist'} Hz"
        print(f"  Env band : {band}")
    else:
        print(f"  Env band : full-band (no pre-filter)")
    print(f"{'='*64}\n")

    all_saved = []
    for i, csv_path in enumerate(csv_files, 1):
        print(f"[{i}/{len(csv_files)}]", end=" ")
        try:
            saved = process_csv(
                csv_path, output_dir,
                fs=args.fs, downsample=args.downsample,
                f_min=args.f_min, f_max=args.f_max,
                n_freqs=args.n_freqs, sigma=args.sigma,
                img_size=args.img_size, n_windows=args.n_windows,
                env_f_low=args.env_f_low, env_f_high=args.env_f_high,
            )
            all_saved.extend(saved)
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\nDone. {len(all_saved)} scalogram(s) saved to {output_dir}/")


if __name__ == "__main__":
    main()
