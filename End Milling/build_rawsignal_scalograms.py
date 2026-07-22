"""
Build real time-windowed CWT scalograms from End Milling's RAW waveform
files (data/run1.csv-run45.csv, ~16,393 Hz, ~65,000 samples/run) -- the
structural fix for the biggest limitation of the scalograms_32x3/32x12
pipelines: those are built from precomputed Excel features with only ONE
real measurement per run, so their "windows" are row-splits of that single
measurement, not independent samples. This script instead splits the raw
signal into N real, non-overlapping time windows per run and computes a
FRESH continuous wavelet transform for each -- genuinely new information
per window, the way Shoulder Milling's real a/b/c measurements were.

IMPORTANT caveat about "matching cnn_model/scalogram.py"
-----------------------------------------------------------
`cnn_model/scalogram.py` -- the script README.md's Pipeline section
describes as building `scalograms_ai4_ai6/` ("Converts each CSV into a
224x224 RGB scalogram PNG using an analytic Morlet CWT") -- does **not
exist in this repository checkout**. It was never committed (same
situation as `scalogram_hilbert.py`, noted missing in
build_residual_scalograms.py's docstring). So this script cannot literally
reproduce its exact CWT scale range -- there is nothing to read.

What IS verifiable and was checked directly against the real
`scalograms_ai4_ai6/run1.png` output before writing this script:
  - Image size: 224x224 RGB (confirmed via PIL).
  - Channel layout: R and G channels have real, varying content; B is
    IDENTICALLY ZERO across the whole image (confirmed via numpy min/max).
    This matches Shoulder Milling's own documented analogy table for End
    Milling's Option A design (Shoulder Milling/plot_option_a.py's
    end-milling-vs-option-A comparison): R = CWT(ai4), G = CWT(ai6),
    B = unused. This script reproduces that channel layout exactly.

The actual CWT parameters (wavelet family, scale/frequency range, number
of scales) are NOT recoverable and are chosen fresh here, documented
honestly rather than silently guessed to look like a reproduction:
  - Wavelet: complex ("analytic") Morlet, `cmor1.5-1.0` (bandwidth 1.5,
    center frequency 1.0) -- matches README's "analytic Morlet CWT"
    wording; pywt's plain 'morl' is real-valued, not analytic.
  - Frequency range: 20 Hz - 4000 Hz (log-spaced, --n_scales scales,
    default 128). Lower bound excludes near-DC drift; upper bound is half
    the ~8196 Hz Nyquist, covering spindle rotation frequencies (25-83 Hz
    for 1500-5000 rpm), tooth-passing frequencies and their harmonics, and
    into the low-kHz range associated with chatter/tool-wear vibration,
    without pushing into the noisier top octave near Nyquist.
  - Per-window magnitude scalogram: |CWT coefficients|, log1p-compressed,
    min-max normalised to [0, 255] per window (independently per channel).

Windows
-------
Each run's raw signal is split into --n_windows equal, non-overlapping,
REAL time segments (default 10, matching this repo's existing "_10w"
naming convention for the original CWT pipeline). Unlike the
scalograms_32x3/32x12 pipelines' fabricated row-splits, every window here
is an actual different slice of the recorded signal.

Output:
    scalograms_raw_10w/run{N}_w{K}.png   224x224 RGB PNG, K = 0..n_windows-1
                                          (R=ai4 CWT, G=ai6 CWT, B=0)

Usage:
    python build_rawsignal_scalograms.py
    python build_rawsignal_scalograms.py --n_windows 5
    python build_rawsignal_scalograms.py --n_scales 64 --f_min 10 --f_max 2000
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import pywt
from PIL import Image

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
FS = 16393.0   # Hz, per README.md / confirmed from stlml files' Delta_X=6.1e-5s
N_RUNS = 45
IMG_SIZE = 224
WAVELET = "cmor1.5-1.0"   # complex (analytic) Morlet


def compute_scales(n_scales: int, f_min: float, f_max: float) -> np.ndarray:
    """Log-spaced target frequencies f_min..f_max (Hz) converted to CWT
    scales for `WAVELET` at sampling rate FS."""
    freqs = np.geomspace(f_min, f_max, n_scales)
    return pywt.frequency2scale(WAVELET, freqs / FS)


def channel_scalogram_u8(signal: np.ndarray, scales: np.ndarray) -> np.ndarray:
    """(len(scales), IMG_SIZE) -> resized to (IMG_SIZE, IMG_SIZE) uint8:
    |CWT coefficients|, log1p-compressed, min-max normalised per window."""
    coeffs, _ = pywt.cwt(signal, scales, WAVELET, sampling_period=1.0 / FS)
    mag = np.log1p(np.abs(coeffs))
    lo, hi = mag.min(), mag.max()
    norm = (mag - lo) / (hi - lo + 1e-9)
    u8 = (norm * 255).astype(np.uint8)
    return np.array(Image.fromarray(u8).resize((IMG_SIZE, IMG_SIZE), Image.BILINEAR))


def build_window_image(ai4_window: np.ndarray, ai6_window: np.ndarray, scales: np.ndarray) -> np.ndarray:
    """(224, 224, 3) uint8: R=CWT(ai4), G=CWT(ai6), B=0 -- matches the
    confirmed channel layout of the existing scalograms_ai4_ai6/ output."""
    r = channel_scalogram_u8(ai4_window, scales)
    g = channel_scalogram_u8(ai6_window, scales)
    b = np.zeros_like(r)
    return np.stack([r, g, b], axis=-1)


def split_windows(signal: np.ndarray, n_windows: int) -> list:
    n = len(signal)
    chunk = n // n_windows
    return [signal[i * chunk:(i + 1) * chunk] for i in range(n_windows)]


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--n_windows", type=int, default=10,
                        help="Real, non-overlapping time windows per run")
    parser.add_argument("--n_scales", type=int, default=128,
                        help="Number of log-spaced CWT scales (frequency rows)")
    parser.add_argument("--f_min", type=float, default=20.0, help="Lowest CWT frequency (Hz)")
    parser.add_argument("--f_max", type=float, default=4000.0, help="Highest CWT frequency (Hz)")
    parser.add_argument("--out_dir", default=None,
                        help="Default: scalograms_raw_<n_windows>w")
    parser.add_argument("--resume", action="store_true", default=True,
                        help="Skip a run entirely if all its window PNGs already exist "
                             "(default on -- CWT is slow, ~2-6s/window, so a killed/"
                             "interrupted run can just be re-invoked to continue)")
    parser.add_argument("--no_resume", dest="resume", action="store_false",
                        help="Regenerate every run even if its PNGs already exist")
    args = parser.parse_args()

    out_dir = ROOT / (args.out_dir or f"scalograms_raw_{args.n_windows}w")
    out_dir.mkdir(exist_ok=True)
    print(f"n_windows={args.n_windows}  n_scales={args.n_scales}  "
          f"freq_range=[{args.f_min}, {args.f_max}] Hz  resume={args.resume}")
    print(f"Output dir: {out_dir}/")

    scales = compute_scales(args.n_scales, args.f_min, args.f_max)

    n_saved, n_skipped_missing, n_skipped_done = 0, 0, 0
    for i in range(1, N_RUNS + 1):
        run = f"run{i}"
        csv_path = DATA_DIR / f"{run}.csv"
        if not csv_path.exists():
            print(f"  skip {run}: {csv_path} not found -- run convert_stml_to_csv.py first")
            n_skipped_missing += 1
            continue

        out_paths = [out_dir / f"{run}_w{k}.png" for k in range(args.n_windows)]
        if args.resume and all(p.exists() for p in out_paths):
            print(f"  {run}: all {args.n_windows} windows already exist -- skipping")
            n_skipped_done += 1
            continue

        df = pd.read_csv(csv_path)
        ai4 = df["ai4"].to_numpy(dtype=np.float64)
        ai6 = df["ai6"].to_numpy(dtype=np.float64)
        ai4_windows = split_windows(ai4, args.n_windows)
        ai6_windows = split_windows(ai6, args.n_windows)

        for k in range(args.n_windows):
            if args.resume and out_paths[k].exists():
                continue
            img = build_window_image(ai4_windows[k], ai6_windows[k], scales)
            Image.fromarray(img).save(out_paths[k])
            n_saved += 1
        print(f"  {run}: {args.n_windows} windows saved", flush=True)

    print(f"\nSaved {n_saved} new PNGs ({n_skipped_done} runs already done, "
          f"{n_skipped_missing} runs missing CSV) -> {out_dir}/")
    print("Done.")


if __name__ == "__main__":
    main()
