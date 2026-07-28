"""
Build frequency-band statistical feature images from raw vibration CSVs.

Divides the vibration spectrum into frequency bands and computes 4 statistics
per band per channel: RMS, peak amplitude, kurtosis, spectral centroid.
Selects the top-32 (band x stat x channel) features by F-statistic against
the target, then builds a 32x3 image (same format as existing pipelines).

Why this for feed_coarse / roughness:
  - Feed rate changes the chip load per tooth → changes force magnitude and
    spectrum shape in the cutting process band (200-2000 Hz).
  - Surface roughness correlates with high-frequency vibration (>1000 Hz):
    rougher surfaces → more high-freq chatter/ploughing energy.
  - Neither of these signals is captured in the precomputed Excel features
    (which already average over the full measurement window and only track
    CWT scale energies and a handful of statistics).

Frequency bands (6 bands, tuned to end milling physics):
  0:    0-50 Hz     machine/spindle resonance
  1:   50-200 Hz    spindle harmonics (25/33/50/67/83 Hz + overtones)
  2:  200-500 Hz    tooth-passing frequency zone (spindle × n_teeth)
  3:  500-2000 Hz   cutting process dynamics, workpiece modes
  4: 2000-5000 Hz   surface texture, chatter, high-freq cutting
  5: 5000-8196 Hz   ultrasonic / sensor noise floor

Statistics per band per channel:
  rms, peak, kurtosis, spectral_centroid

Total raw features: 6 bands × 4 stats × 3 channels = 72
After top-32 F-stat selection → 32×3 image (3 columns = ai4/ai5/ai6).

Output dirs:
  scalograms_band_feedopt/           --target feed_coarse
  scalograms_band_roughness/         --target roughness
  scalograms_band_speedopt/          --target speed
  scalograms_band_feedopt_perdoc/    --target feed_coarse --norm_mode per_doc

Usage:
    python build_band_features.py --target feed_coarse
    python build_band_features.py --target roughness
    python build_band_features.py --target speed
    python build_band_features.py --target feed_coarse --norm_mode per_doc
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import kurtosis, f_oneway

from em_feature_common import (
    ROOT, DATA_DIR, RUNS, RA_VALUES, N_SELECT,
    load_cnn_train_module, normalize_and_window,
)

BANDS_HZ = [(0, 50), (50, 200), (200, 500), (500, 2000), (2000, 5000), (5000, 9000)]
STATS    = ["rms", "peak", "kurtosis", "spectral_centroid"]
CHANNELS = ["ai4", "ai5", "ai6"]

TARGET_SUFFIX = {
    "speed":       "speedopt",
    "feed_coarse": "feedopt",
    "roughness":   "roughness",
    "doc":         "docopt",
}

TARGET_VALUES = {
    "speed":       lambda mod, run: mod.SPEED_LABELS[run],
    "feed_coarse": lambda mod, run: mod.FEED_COARSE_LABELS[run],
    "roughness":   lambda mod, run: mod.RA_LABELS[run],
    "doc":         lambda mod, run: mod.DOC_LABELS[run],
}


def load_signal(run: str):
    df = pd.read_csv(DATA_DIR / f"{run}.csv")
    sig = df[CHANNELS].values.astype(np.float64)
    times = df["time"].values
    fs = 1.0 / (times[1] - times[0])
    return sig, fs


def band_stats(signal: np.ndarray, fs: float) -> np.ndarray:
    """Returns (n_bands, n_stats, n_channels) = (6, 4, 3) float64."""
    N = signal.shape[0]
    freqs = np.fft.rfftfreq(N, d=1.0 / fs)
    out = np.zeros((len(BANDS_HZ), len(STATS), signal.shape[1]))

    for bi, (f_lo, f_hi) in enumerate(BANDS_HZ):
        mask = (freqs >= f_lo) & (freqs < f_hi)
        for ci in range(signal.shape[1]):
            ch = signal[:, ci]
            # Time-domain bandpass approximation via FFT masking
            fft = np.fft.rfft(ch)
            fft_band = np.zeros_like(fft)
            fft_band[mask] = fft[mask]
            band_sig = np.fft.irfft(fft_band, n=N)

            rms_val  = np.sqrt(np.mean(band_sig ** 2))
            peak_val = np.max(np.abs(band_sig))
            kurt_val = float(kurtosis(band_sig))

            mag = np.abs(fft)[mask]
            f_b = freqs[mask]
            centroid = float(np.sum(f_b * mag) / (np.sum(mag) + 1e-12))

            out[bi, 0, ci] = rms_val
            out[bi, 1, ci] = peak_val
            out[bi, 2, ci] = kurt_val
            out[bi, 3, ci] = centroid

    return out   # (6, 4, 3)


def select_rows_fstat(all_feats: np.ndarray, target_arr: np.ndarray) -> np.ndarray:
    """all_feats: (n_runs, n_rows, n_cols). Returns sorted top-N_SELECT row indices."""
    n_rows  = all_feats.shape[1]
    n_cols  = all_feats.shape[2]
    classes = np.unique(target_arr)
    scores  = np.zeros(n_rows)
    for ri in range(n_rows):
        col_scores = []
        for ci in range(n_cols):
            vals = all_feats[:, ri, ci]
            groups = [vals[target_arr == c] for c in classes]
            f, _ = f_oneway(*groups)
            col_scores.append(0.0 if (np.isnan(f) or np.isinf(f)) else f)
        scores[ri] = np.mean(col_scores)
    top_idx = np.sort(np.argsort(scores)[::-1][:N_SELECT])
    return top_idx, scores


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description=__doc__)
    parser.add_argument("--target", default="feed_coarse",
                        choices=["speed", "feed_coarse", "roughness", "doc"])
    parser.add_argument("--n_windows", type=int, default=3)
    parser.add_argument("--norm_mode", default="global", choices=["global", "per_doc"])
    args = parser.parse_args()

    suffix = TARGET_SUFFIX[args.target]
    out_name = f"scalograms_band_{suffix}"
    if args.norm_mode == "per_doc":
        out_name += "_perdoc"
    if args.n_windows != 3:
        out_name += f"_{args.n_windows}win"
    out_dir = ROOT / out_name
    out_dir.mkdir(exist_ok=True)

    print(f"Target   : {args.target}")
    print(f"Norm mode: {args.norm_mode}")
    print(f"Out dir  : {out_dir}/")

    mod = load_cnn_train_module()
    runs_sorted = sorted(RUNS, key=lambda s: int(s[3:]))

    print("\nComputing frequency-band statistics from raw CSVs ...")
    raw_feats = []   # (45, 24, 3) — 6 bands × 4 stats = 24 rows, 3 channels
    for run in runs_sorted:
        sig, fs = load_signal(run)
        bs = band_stats(sig, fs)                    # (6, 4, 3)
        flat = bs.reshape(-1, bs.shape[-1])         # (24, 3)
        raw_feats.append(flat)
        print(f"  {run}: fs={fs:.0f} Hz  bands×stats={flat.shape}")

    all_feats = np.stack(raw_feats)   # (45, 24, 3)

    tgt_fn = TARGET_VALUES[args.target]
    target_arr = np.array([tgt_fn(mod, r) for r in runs_sorted])

    print(f"\nSelecting top-{N_SELECT} of {all_feats.shape[1]} rows by F-stat ...")
    sel_rows, scores = select_rows_fstat(all_feats, target_arr)
    print(f"  Selected row indices: {sel_rows.tolist()}")

    run_imgs_raw = all_feats[:, sel_rows, :]   # (45, 32, 3)

    doc_labels = [mod.DOC_LABELS[r] for r in runs_sorted]
    run_imgs_u8, block_idx, real_block_sizes, pad_size = normalize_and_window(
        run_imgs_raw, args.n_windows, norm_mode=args.norm_mode, doc_labels=doc_labels)
    print(f"  Block sizes: {real_block_sizes}  padded to {pad_size}")

    rows_csv, window_npz, run_npz = [], {}, {}
    for ri, run in enumerate(runs_sorted):
        run_npz[run] = run_imgs_raw[ri]
        speed = mod.SPEED_LABELS[run]; doc = mod.DOC_LABELS[run]
        feed = mod.FEED_LABELS[run]; fc = mod.FEED_COARSE_LABELS[run]
        ra_lbl = mod.RA_LABELS[run]; ra = RA_VALUES[run]
        for k, idx in enumerate(block_idx):
            sid = f"{run}_w{k}"; fname = f"{sid}.png"
            pad = pad_size - len(idx)
            bu = np.pad(run_imgs_u8[ri, idx, :],  ((0, pad), (0, 0))) if pad else run_imgs_u8[ri, idx, :]
            br = np.pad(run_imgs_raw[ri, idx, :].astype(np.float32), ((0, pad), (0, 0))) if pad else run_imgs_raw[ri, idx, :].astype(np.float32)
            Image.fromarray(bu).save(out_dir / fname)
            window_npz[sid] = br
            rows_csv.append({"filename": fname, "sample_id": sid, "run": run, "window": k,
                             "speed": speed, "doc": doc, "feed": feed, "feed_coarse": fc,
                             "ra": ra, "ra_label": ra_lbl, "ra_class": mod.RA_NAMES[ra_lbl]})

    pd.DataFrame(rows_csv).to_csv(out_dir / "labels.csv", index=False)
    np.savez(out_dir / "features_raw.npz", **window_npz)
    np.savez(out_dir / "run_features_raw.npz", **run_npz)

    # Row label lookup
    row_labels_all = [(b, s, BANDS_HZ[b], STATS[s])
                      for b in range(len(BANDS_HZ)) for s in range(len(STATS))]
    with open(out_dir / "band_layout.json", "w") as f:
        json.dump({
            "target": args.target, "norm_mode": args.norm_mode,
            "bands_hz": BANDS_HZ, "stats": STATS, "channels": CHANNELS,
            "n_raw_rows": all_feats.shape[1],
            "selected_row_indices": sel_rows.tolist(),
            "all_scores": [round(float(s), 4) for s in scores],
            "selected_rows_decoded": [
                {"band": row_labels_all[i][0], "stat": row_labels_all[i][1],
                 "band_hz": row_labels_all[i][2], "stat_name": row_labels_all[i][3]}
                for i in sel_rows
            ],
        }, f, indent=2)

    print(f"\nSaved {len(rows_csv)} PNGs + labels.csv -> {out_dir}/")


if __name__ == "__main__":
    main()
