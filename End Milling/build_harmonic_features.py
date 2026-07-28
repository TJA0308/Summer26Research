"""
Build harmonic-amplitude feature images from raw vibration CSVs.

For each run, reads data/run{N}.csv (columns: time, ai4, ai5, ai6) and computes
two sets of spindle-harmonic features from the FFT of each channel:

  Feature set 1 -- Harmonic amplitudes
    For each of the 5 spindle speeds (1500/2000/3000/4000/5000 rpm) and each
    of N_HARMONICS harmonic orders (1x, 2x, 3x, 4x), extract the FFT magnitude
    at the exact frequency bin. Rows in the output image correspond to
    (speed_idx x harmonic_order) pairs -- 5x4=20 rows total.

  Feature set 2 -- Harmonic ratios
    Same bins, but expressed as amplitude / local spectral mean (±LOCAL_BINS
    bins around the harmonic). A high ratio means the spectrum has a clear peak
    at that frequency, independent of the absolute amplitude level.

Output image shape: (20, 3)
  col 0: mean harmonic amplitude across channels
  col 1: mean harmonic ratio across channels
  col 2: max harmonic amplitude across channels

The 3-column layout keeps this compatible with the existing CNN pipeline
(scalograms_32x3*) -- same Resize(224,224) path, same transforms.

Option 3 -- Per-DOC normalization:
  When --norm_mode per_doc is set, z-scoring is done within each DOC group
  (0.015 / 0.030 / 0.060 mm, 15 runs each) instead of globally across all 45.
  This strips out DOC-driven mean shifts in the features before the CNN sees
  them, which is useful for feed_coarse where DOC is the main confound.

Output dirs:
  scalograms_harmonic_speedopt/         --target speed (default)
  scalograms_harmonic_feedopt/          --target feed_coarse
  scalograms_harmonic_speedopt_perdoc/  --target speed --norm_mode per_doc
  scalograms_harmonic_feedopt_perdoc/   --target feed_coarse --norm_mode per_doc

Usage:
    python build_harmonic_features.py --target speed
    python build_harmonic_features.py --target feed_coarse
    python build_harmonic_features.py --target speed --norm_mode per_doc
    python build_harmonic_features.py --target feed_coarse --norm_mode per_doc
    python build_harmonic_features.py --target speed --n_harmonics 6
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from em_feature_common import (
    ROOT, DATA_DIR, RUNS, RA_VALUES,
    load_cnn_train_module,
)

N_HARMONICS = 4
LOCAL_BINS  = 10   # ±bins for ratio denominator
SPINDLE_RPM = [1500, 2000, 3000, 4000, 5000]
SPINDLE_HZ  = [rpm / 60.0 for rpm in SPINDLE_RPM]
N_ROWS      = len(SPINDLE_HZ) * N_HARMONICS   # 20

TARGET_SUFFIX = {
    "speed":       "speedopt",
    "feed_coarse": "feedopt",
    "roughness":   "",
    "doc":         "docopt",
}


def load_raw_signal(run: str) -> tuple:
    """Returns (signal_matrix: (N, 3), fs: float) from data/run{N}.csv."""
    csv_path = DATA_DIR / f"{run}.csv"
    df = pd.read_csv(csv_path)
    signal = df[["ai4", "ai5", "ai6"]].values.astype(np.float64)
    times = df["time"].values
    fs = 1.0 / (times[1] - times[0])
    return signal, fs


def harmonic_features_for_run(signal: np.ndarray, fs: float, n_harmonics: int = N_HARMONICS) -> np.ndarray:
    """Returns (N_ROWS, 3) float64 array:
      col 0: mean amplitude across channels
      col 1: mean harmonic ratio across channels
      col 2: max amplitude across channels
    """
    N = signal.shape[0]
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)   # (N//2+1,)

    amps  = np.zeros((N_ROWS, signal.shape[1]))   # (20, 3)
    ratios = np.zeros_like(amps)

    row = 0
    for f0 in SPINDLE_HZ:
        for h in range(1, n_harmonics + 1):
            target_freq = f0 * h
            for ch in range(signal.shape[1]):
                fft_mag = np.abs(np.fft.rfft(signal[:, ch])) / N
                bin_idx = int(np.argmin(np.abs(freqs - target_freq)))
                amp = fft_mag[bin_idx]
                lo = max(0, bin_idx - LOCAL_BINS)
                hi = min(len(fft_mag), bin_idx + LOCAL_BINS + 1)
                local_mean = fft_mag[lo:hi].mean()
                amps[row, ch]   = amp
                ratios[row, ch] = amp / (local_mean + 1e-12)
            row += 1

    out = np.stack([
        amps.mean(axis=1),    # col 0: mean amp
        ratios.mean(axis=1),  # col 1: mean ratio
        amps.max(axis=1),     # col 2: max amp
    ], axis=1)   # (20, 3)
    return out


def normalize_images(run_imgs_raw: np.ndarray, doc_labels: list,
                     norm_mode: str) -> np.ndarray:
    """Normalize (45, 20, 3) float64 array.
    norm_mode='global': z-score across all 45 runs (original convention).
    norm_mode='per_doc': z-score within each DOC group (0/1/2) separately.
    Both clip to ±3 sigma and rescale to [0, 255] uint8.
    """
    n_cols = run_imgs_raw.shape[-1]

    if norm_mode == "per_doc":
        doc_arr = np.array(doc_labels)
        normed = np.zeros_like(run_imgs_raw)
        for doc_cls in np.unique(doc_arr):
            idx = np.where(doc_arr == doc_cls)[0]
            group = run_imgs_raw[idx]
            flat = group.reshape(-1, n_cols)
            mu  = flat.mean(axis=0)
            sig = flat.std(axis=0)
            sig[sig < 1e-10] = 1.0
            normed[idx] = (group - mu) / sig
    else:
        flat = run_imgs_raw.reshape(-1, n_cols)
        mu  = flat.mean(axis=0)
        sig = flat.std(axis=0)
        sig[sig < 1e-10] = 1.0
        normed = (run_imgs_raw - mu) / sig

    return np.clip((normed + 3) / 6 * 255, 0, 255).astype(np.uint8)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=__doc__)
    parser.add_argument("--target", default="speed",
                        choices=["speed", "feed_coarse", "roughness", "doc"])
    parser.add_argument("--n_windows", type=int, default=3)
    parser.add_argument("--n_harmonics", type=int, default=N_HARMONICS,
                        help="Number of harmonic orders to extract per spindle speed")
    parser.add_argument("--norm_mode", default="global", choices=["global", "per_doc"],
                        help="'global': z-score across all runs (default). "
                             "'per_doc': z-score within each DOC group to remove DOC confound.")
    args = parser.parse_args()

    suffix = TARGET_SUFFIX[args.target]
    out_name = f"scalograms_harmonic_{suffix}" if suffix else "scalograms_harmonic"
    if args.norm_mode == "per_doc":
        out_name += "_perdoc"
    if args.n_windows != 3:
        out_name += f"_{args.n_windows}win"
    out_dir = ROOT / out_name
    out_dir.mkdir(exist_ok=True)

    n_rows = len(SPINDLE_HZ) * args.n_harmonics
    print(f"Target      : {args.target}")
    print(f"N harmonics : {args.n_harmonics}  (rows per image: {n_rows})")
    print(f"Norm mode   : {args.norm_mode}")
    print(f"Output dir  : {out_dir}/")

    mod = load_cnn_train_module()
    runs_sorted = sorted(RUNS, key=lambda s: int(s[3:]))

    print("\nComputing harmonic features from raw CSVs ...")
    run_imgs_raw = []
    for run in runs_sorted:
        signal, fs = load_raw_signal(run)
        feat = harmonic_features_for_run(signal, fs, n_harmonics=args.n_harmonics)
        run_imgs_raw.append(feat)
        print(f"  {run}: fs={fs:.0f} Hz  feat shape={feat.shape}")

    run_imgs_raw = np.stack(run_imgs_raw)   # (45, n_rows, 3)
    doc_labels = [mod.DOC_LABELS[r] for r in runs_sorted]

    print(f"\nNormalising ({args.norm_mode}) ...")
    run_imgs_u8 = normalize_images(run_imgs_raw, doc_labels, args.norm_mode)

    # Window split
    block_idx = [b.tolist() for b in np.array_split(np.arange(n_rows), args.n_windows)]
    real_block_sizes = [len(b) for b in block_idx]
    pad_size = max(real_block_sizes)
    print(f"  Window block sizes: {real_block_sizes}  (padded to {pad_size})")

    print("\nWriting images + labels ...")
    rows_csv = []
    window_npz = {}
    run_npz = {}

    for ri, run in enumerate(runs_sorted):
        run_npz[run] = run_imgs_raw[ri]
        speed      = mod.SPEED_LABELS[run]
        doc        = mod.DOC_LABELS[run]
        feed       = mod.FEED_LABELS[run]
        feed_coarse = mod.FEED_COARSE_LABELS[run]
        ra_label   = mod.RA_LABELS[run]
        ra         = RA_VALUES[run]

        for k, idx in enumerate(block_idx):
            sample_id = f"{run}_w{k}"
            fname = f"{sample_id}.png"
            pad_rows = pad_size - len(idx)

            block_u8  = run_imgs_u8[ri, idx, :]
            block_raw = run_imgs_raw[ri, idx, :].astype(np.float32)
            if pad_rows > 0:
                block_u8  = np.pad(block_u8,  ((0, pad_rows), (0, 0)))
                block_raw = np.pad(block_raw, ((0, pad_rows), (0, 0)))

            Image.fromarray(block_u8).save(out_dir / fname)
            window_npz[sample_id] = block_raw
            rows_csv.append({
                "filename": fname, "sample_id": sample_id, "run": run, "window": k,
                "speed": speed, "doc": doc, "feed": feed, "feed_coarse": feed_coarse,
                "ra": ra, "ra_label": ra_label, "ra_class": mod.RA_NAMES[ra_label],
            })

    pd.DataFrame(rows_csv).to_csv(out_dir / "labels.csv", index=False)
    np.savez(out_dir / "features_raw.npz", **window_npz)
    np.savez(out_dir / "run_features_raw.npz", **run_npz)

    # Row labels for reference
    row_labels = []
    for rpm, f0 in zip(SPINDLE_RPM, SPINDLE_HZ):
        for h in range(1, args.n_harmonics + 1):
            row_labels.append({"rpm": rpm, "harmonic": h, "freq_hz": round(f0 * h, 2)})

    with open(out_dir / "harmonic_layout.json", "w") as f:
        json.dump({
            "target": args.target, "norm_mode": args.norm_mode,
            "n_harmonics": args.n_harmonics, "n_rows": n_rows,
            "spindle_rpm": SPINDLE_RPM, "spindle_hz": SPINDLE_HZ,
            "local_bins_for_ratio": LOCAL_BINS,
            "columns": ["mean_amp", "mean_ratio", "max_amp"],
            "row_layout": row_labels,
            "block_row_indices": block_idx,
            "real_block_sizes": real_block_sizes,
            "padded_block_size": pad_size,
        }, f, indent=2)

    print(f"\nSaved {len(rows_csv)} PNGs + labels.csv + features_raw.npz -> {out_dir}/")


if __name__ == "__main__":
    main()
