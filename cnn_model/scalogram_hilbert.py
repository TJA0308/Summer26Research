"""
4-channel CWT scalogram generator: raw signal + squared envelope (SES) for ai4 and ai6.

Produces per-window .npy arrays of shape (4, IMG_SIZE, IMG_SIZE) float32 [0, 1]
and 2x2 composite PNG previews for inspection.

Channel layout (index 0-3, same order in .npy and PNG quadrants):
    0 / top-left     : ai4 raw CWT
    1 / top-right    : ai6 raw CWT
    2 / bottom-left  : SES(ai4) CWT  [squared envelope = |H{x}|^2]
    3 / bottom-right : SES(ai6) CWT  [squared envelope = |H{x}|^2]

Usage (run from project root):
    python cnn_model/scalogram_hilbert.py --input_dir data --output_dir scalograms_hilbert_10w --n_windows 10

To use with the CNN trainer, load .npy instead of PNG:

    class NpyScalogramDataset(Dataset):
        def __init__(self, paths, labels, transform=None):
            self.paths, self.labels, self.transform = paths, labels, transform
        def __len__(self): return len(self.paths)
        def __getitem__(self, idx):
            arr = torch.from_numpy(np.load(self.paths[idx]))  # (4, H, W) float32 [0,1]
            if self.transform:
                arr = self.transform(arr)
            return arr, self.labels[idx]

    # Normalise each channel with its own mean/std (compute from training set,
    # or use approximate ImageNet stats for ch0/ch1 and 0.5/0.5 for ch2/ch3):
    NORM_MEAN = [0.485, 0.456, 0.5, 0.5]
    NORM_STD  = [0.229, 0.224, 0.2, 0.2]

    # build_model needs in_channels=4:
    #   model.conv1 = nn.Conv2d(4, 64, kernel_size=7, stride=2, padding=3, bias=False)
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
    TIME_COL, analytic_morlet_cwt, power_to_uint8,
)
from hilbert_envelope import compute_envelope

CHANNELS = ["ai4", "ai6"]


def compute_four_powers(df, fs_eff, f_min, f_max, n_freqs, sigma,
                        downsample, env_f_low=None, env_f_high=None):
    """
    Compute 4 CWT power maps: [ai4_raw, ai6_raw, ses_ai4, ses_ai6].

    The SES (squared envelope spectrum) channels use |H{x}|^2 before CWT,
    which sharpens AM peaks and suppresses noise compared to the plain envelope.
    """
    powers = []

    # Raw signal CWT for each channel
    for ch in CHANNELS:
        sig = df[ch].values[::downsample].astype(np.float32)
        sig -= sig.mean()
        pw, _ = analytic_morlet_cwt(sig, fs=fs_eff, n_freqs=n_freqs,
                                     f_min=f_min, f_max=f_max, sigma=sigma)
        powers.append(pw)

    # Squared envelope (SES) CWT for each channel
    for ch in CHANNELS:
        sig = df[ch].values[::downsample].astype(np.float32)
        env = compute_envelope(sig, fs=fs_eff, f_low=env_f_low, f_high=env_f_high) ** 2
        pw, _ = analytic_morlet_cwt(env, fs=fs_eff, n_freqs=n_freqs,
                                     f_min=f_min, f_max=f_max, sigma=sigma)
        powers.append(pw)

    return powers  # [ai4_raw, ai6_raw, ses_ai4, ses_ai6]


def powers_to_array(powers, img_size, global_ranges=None):
    """
    Return float32 ndarray of shape (4, img_size, img_size) with values in [0, 1].
    Each channel is independently log-normalised and resized.
    """
    planes = []
    for i, pw in enumerate(powers):
        lo, hi = global_ranges[i] if global_ranges else (None, None)
        gray = power_to_uint8(pw, lo=lo, hi=hi)
        resized = np.array(
            Image.fromarray(gray).resize((img_size, img_size), resample=Image.LANCZOS),
            dtype=np.float32,
        ) / 255.0
        planes.append(resized)
    return np.stack(planes, axis=0)  # (4, H, W)


def build_preview_png(arr):
    """
    Build a 2x2 tiled RGB preview from a (4, H, W) float32 array.
    Each quadrant is rendered as grayscale. Total size: (2H x 2W).

    Layout:
        [ ai4_raw  | ai6_raw  ]
        [ env_ai4  | env_ai6  ]
    """
    _, h, w = arr.shape
    canvas = np.zeros((h * 2, w * 2, 3), dtype=np.uint8)
    positions = [(0, 0), (0, w), (h, 0), (h, w)]
    labels = ["ai4_raw", "ai6_raw", "ses_ai4", "ses_ai6"]
    for idx, (r0, c0) in enumerate(positions):
        g = (arr[idx] * 255).astype(np.uint8)
        canvas[r0:r0 + h, c0:c0 + w, 0] = g
        canvas[r0:r0 + h, c0:c0 + w, 1] = g
        canvas[r0:r0 + h, c0:c0 + w, 2] = g
        _ = labels[idx]  # kept for documentation clarity
    return canvas


def process_csv(csv_path, output_dir, fs=FS, downsample=DOWNSAMPLE,
                f_min=F_MIN, f_max=F_MAX, n_freqs=N_FREQS, sigma=SIGMA,
                img_size=IMG_SIZE, n_windows=1, global_ranges=None,
                env_f_low=None, env_f_high=None, save_preview=True):
    stem = csv_path.stem
    df   = pd.read_csv(csv_path)

    missing = [c for c in CHANNELS + [TIME_COL] if c not in df.columns]
    if missing:
        raise ValueError(f"{csv_path.name}: missing columns {missing}. "
                         f"Available: {df.columns.tolist()}")

    fs_eff    = fs // downsample
    f_max_use = f_max if f_max is not None else fs_eff / 2.5
    df        = df[[TIME_COL] + CHANNELS]
    N         = len(df)

    print(f"  {csv_path.name} ({N} samples) …", end=" ", flush=True)

    saved = []

    def _save_window(df_win, suffix):
        powers = compute_four_powers(df_win, fs_eff, f_min, f_max_use,
                                     n_freqs, sigma, downsample,
                                     env_f_low, env_f_high)
        arr     = powers_to_array(powers, img_size, global_ranges)
        npy_out = output_dir / f"{stem}{suffix}.npy"
        np.save(npy_out, arr)
        saved.append(npy_out)
        if save_preview:
            preview = build_preview_png(arr)
            Image.fromarray(preview).save(output_dir / f"{stem}{suffix}_preview.png")
        print(f"-> {npy_out.name}", end=" ", flush=True)

    if n_windows == 1:
        _save_window(df, "")
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
        _save_window(df_win, f"_w{w + 1}")

    print()
    return saved


def main():
    parser = argparse.ArgumentParser(
        description="Generate 4-channel (raw + Hilbert envelope) CWT scalograms as .npy files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--input_dir",  required=True,  help="Directory of raw CSV files")
    parser.add_argument("--output_dir", required=True,  help="Where to save .npy and preview PNGs")
    parser.add_argument("--single",     default=None,   help="Process one CSV file by name")
    parser.add_argument("--fs",         type=int,   default=FS)
    parser.add_argument("--downsample", type=int,   default=DOWNSAMPLE)
    parser.add_argument("--f_min",      type=float, default=F_MIN)
    parser.add_argument("--f_max",      type=float, default=F_MAX)
    parser.add_argument("--n_freqs",    type=int,   default=N_FREQS)
    parser.add_argument("--sigma",      type=float, default=SIGMA)
    parser.add_argument("--img_size",   type=int,   default=IMG_SIZE)
    parser.add_argument("--n_windows",  type=int,   default=1,
                        help="Windows per run (same semantics as scalogram.py)")
    parser.add_argument("--env_f_low",  type=float, default=None,
                        help="Bandpass lower cutoff Hz applied before Hilbert transform "
                             "(e.g. tooth-pass fundamental ~25-50 Hz for typical end mills)")
    parser.add_argument("--env_f_high", type=float, default=None,
                        help="Bandpass upper cutoff Hz applied before Hilbert transform")
    parser.add_argument("--no_preview", action="store_true",
                        help="Skip saving 2x2 composite PNG previews")
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
    print(f"  4-Channel CWT Scalogram Generator (raw + Hilbert envelope)")
    print(f"{'='*64}")
    print(f"  Input    : {input_dir}  ({len(csv_files)} files)")
    print(f"  Output   : {output_dir}")
    print(f"  Format   : .npy  shape=(4, {args.img_size}, {args.img_size})  float32 [0,1]")
    print(f"  Fs       : {args.fs} Hz -> {fs_eff} Hz  ({args.downsample}x downsample)")
    print(f"  Freqs    : {args.f_min}-{args.f_max} Hz  ({args.n_freqs} bins, log-spaced)")
    print(f"  Sigma    : {args.sigma}  |  Windows: {args.n_windows}")
    print(f"  Channels : [0] ai4_raw  [1] ai6_raw  [2] env_ai4  [3] env_ai6")
    if args.env_f_low or args.env_f_high:
        band = f"{args.env_f_low or 'DC'} – {args.env_f_high or 'Nyquist'} Hz"
        print(f"  Env band : {band}  (Butterworth 4th-order, zero-phase)")
    else:
        print(f"  Env band : full-band (no pre-filter)")
    print(f"  Previews : {'disabled' if args.no_preview else 'enabled (2x2 PNG, 448x448)'}")
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
                save_preview=not args.no_preview,
            )
            all_saved.extend(saved)
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\nDone. {len(all_saved)} .npy file(s) saved to {output_dir}/")


if __name__ == "__main__":
    main()
