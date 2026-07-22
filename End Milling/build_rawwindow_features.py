"""
Build the 32x3 (FFT/mexican/coif) or 32x12 (all features) engineered
feature-image layout from REAL raw-signal time windows, instead of reading
End Milling's precomputed Excel measurement (build_32x3_features.py /
build_32x12_features.py) or building a plain CWT-image scalogram
(build_rawsignal_scalograms.py). This is the "best of both": the same
engineered-feature layout and per-target scale-selection methodology as the
Excel-based pipelines, but every window is a genuinely independent sample
computed fresh from a real, non-overlapping slice of the raw waveform --
not a row-split fragment of one measurement.

See rawwindow_feature_common.py for the actual FFT/CWT/DWT computation and
column semantics (including the coiflet-CWT and DWT-wavelet caveats).

Scale selection
----------------
Same method as em_feature_common.select_cwt_rows: average |Spearman rho|
of the 64 mexican/coif scale rows against the target, top-32 by score.
Here, each run's windows are averaged first (run-level mean mexican/coif
vectors) before correlating against the target across the 45 runs -- same
run-level-averaging rationale as Option D (avoids letting runs with more
windows dominate the 45-point correlation estimate).

Output naming: scalograms_<layout>[_feedopt|_speedopt|_docopt]_raw<n>w/
  e.g. scalograms_32x3_raw3w/            (layout=32x3, target=roughness, n_windows=3)
       scalograms_32x3_feedopt_raw9w/    (layout=32x3, target=feed_coarse, n_windows=9)
       scalograms_32x12_docopt_raw3w/    (layout=32x12, target=doc, n_windows=3)

  <out_dir>/run{N}_w{K}.png       grayscale uint8 PNG, (32, n_cols) -- no
                                   padding needed, every window is already
                                   a complete, real (32, n_cols) sample.
  <out_dir>/labels.csv            filename, sample_id, run, window, speed, doc,
                                   feed, feed_coarse, ra, ra_label, ra_class
  <out_dir>/selected_scales.json  selected/dropped CWT scale indices, all 64
                                   scores, feature_cols, n_cols, n_windows
  <out_dir>/features_raw.npz      pre-quantization float32 (32, n_cols) per
                                   real window -- for smote_generate_32x3.py
  <out_dir>/run_features_raw.npz  pre-quantization float32 (32, n_cols) per
                                   RUN (mean across that run's real windows)
                                   -- for pca_analysis_32x3.py

Usage:
    python build_rawwindow_features.py --target roughness   --layout 32x3  --n_windows 3
    python build_rawwindow_features.py --target feed_coarse --layout 32x3  --n_windows 9
    python build_rawwindow_features.py --target speed       --layout 32x12 --n_windows 3
    python build_rawwindow_features.py --target doc         --layout 32x12 --n_windows 9
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from em_feature_common import ROOT, FEATURE_COLS, COL_IDX, TARGET_DIR_SUFFIX
from rawwindow_feature_common import (
    RUNS, RA_VALUES, load_run_signal, split_windows, compute_window_features,
    select_cwt_rows, load_cnn_train_module, N_SELECT,
)

DATA_DIR = ROOT / "data"
DWT_ORDER = ["KA", "SA", "KD", "SD", "rmsA", "rmsD", "crestfactA", "crestfactD"]


def build_window_row(feats: dict, sel_rows: np.ndarray, layout: str) -> np.ndarray:
    """(32, n_cols) raw (unnormalised) image for one real window.
    layout='32x3': col0=FFT, col1=mexican[selected], col2=coif[selected].
    layout='32x12': all 12 columns, matching Option C's natural-truncation
    convention for the non-CWT columns (they're already <=10 real values,
    zero elsewhere)."""
    if layout == "32x3":
        out = np.zeros((N_SELECT, 3), dtype=np.float64)
        out[:, 0] = feats["fft"]
        out[:, 1] = feats["mex"][sel_rows]
        out[:, 2] = feats["coi"][sel_rows]
        return out

    out = np.zeros((N_SELECT, len(FEATURE_COLS)), dtype=np.float64)
    out[:, COL_IDX["32FFT"]] = feats["fft"]
    out[:len(feats["stats5"]), COL_IDX["5statistics"]] = feats["stats5"]
    out[:, COL_IDX["64mexican"]] = feats["mex"][sel_rows]
    out[:, COL_IDX["64coif"]] = feats["coi"][sel_rows]
    for name in DWT_ORDER:
        vals = feats["dwt"][name]
        out[:len(vals), COL_IDX[name]] = vals
    return out


def out_dir_name(layout: str, target: str, n_windows: int) -> str:
    return f"scalograms_{layout}{TARGET_DIR_SUFFIX[target]}_raw{n_windows}w"


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", required=True, choices=["roughness", "feed_coarse", "speed", "doc"])
    parser.add_argument("--layout", required=True, choices=["32x3", "32x12"])
    parser.add_argument("--n_windows", type=int, default=3,
                        help="Real, non-overlapping time windows per run")
    parser.add_argument("--channel", default="ai4", choices=["ai4", "ai5", "ai6"])
    args = parser.parse_args()

    out_dir = ROOT / out_dir_name(args.layout, args.target, args.n_windows)
    out_dir.mkdir(exist_ok=True)
    print(f"Target: {args.target}  Layout: {args.layout}  n_windows: {args.n_windows}  "
          f"channel: {args.channel}")
    print(f"Output dir: {out_dir}/")

    mod = load_cnn_train_module()

    print("\nComputing per-window FFT/CWT/DWT features from raw signal ...")
    runs_sorted = sorted(RUNS, key=lambda s: int(s[3:]))
    per_run_windows = {}   # run -> list of feats dicts (one per real window)
    for run in runs_sorted:
        signal = load_run_signal(DATA_DIR, run, args.channel)
        windows = split_windows(signal, args.n_windows)
        per_run_windows[run] = [compute_window_features(w) for w in windows]
        print(f"  {run}: {args.n_windows} windows featurised")

    print(f"\nSelecting top-{N_SELECT} of 64 CWT scale rows (target={args.target}) ...")
    run_mex_mean = {r: np.mean([f["mex"] for f in per_run_windows[r]], axis=0) for r in runs_sorted}
    run_coi_mean = {r: np.mean([f["coi"] for f in per_run_windows[r]], axis=0) for r in runs_sorted}
    sel_rows, scores = select_cwt_rows(run_mex_mean, run_coi_mean, mod, args.target, runs_sorted)
    dropped = sorted(set(range(64)) - set(sel_rows.tolist()))
    print(f"  Selected indices ({len(sel_rows)}): {sel_rows.tolist()}")

    n_cols = 3 if args.layout == "32x3" else len(FEATURE_COLS)
    feature_cols = ["FFT", "Mexican", "Coiflet"] if args.layout == "32x3" else FEATURE_COLS

    print(f"\nBuilding {args.layout} images ({n_cols} cols) ...")
    window_rows_raw = {}   # sample_id -> (32, n_cols) raw array
    run_avg_raw = {}       # run -> (32, n_cols) raw array (mean across its windows)
    for run in runs_sorted:
        run_imgs = []
        for k, feats in enumerate(per_run_windows[run]):
            img = build_window_row(feats, sel_rows, args.layout)
            window_rows_raw[f"{run}_w{k}"] = img
            run_imgs.append(img)
        run_avg_raw[run] = np.mean(run_imgs, axis=0)

    all_flat = np.stack(list(window_rows_raw.values())).reshape(-1, n_cols)
    mu = all_flat.mean(axis=0)
    sig = all_flat.std(axis=0)
    sig[sig < 1e-10] = 1.0

    rows = []
    window_npz, run_npz = {}, {}
    for run in runs_sorted:
        speed = mod.SPEED_LABELS[run]
        doc = mod.DOC_LABELS[run]
        feed = mod.FEED_LABELS[run]
        feed_coarse = mod.FEED_COARSE_LABELS[run]
        ra_label = mod.RA_LABELS[run]
        ra = RA_VALUES[run]

        run_npz[run] = run_avg_raw[run].astype(np.float32)

        for k in range(args.n_windows):
            sample_id = f"{run}_w{k}"
            raw = window_rows_raw[sample_id]
            norm = (raw - mu) / sig
            u8 = np.clip((norm + 3) / 6 * 255, 0, 255).astype(np.uint8)
            Image.fromarray(u8).save(out_dir / f"{sample_id}.png")
            window_npz[sample_id] = raw.astype(np.float32)
            rows.append({
                "filename": f"{sample_id}.png", "sample_id": sample_id, "run": run, "window": k,
                "speed": speed, "doc": doc, "feed": feed, "feed_coarse": feed_coarse,
                "ra": ra, "ra_label": ra_label, "ra_class": mod.RA_NAMES[ra_label],
            })

    labels_df = pd.DataFrame(rows)
    labels_df.to_csv(out_dir / "labels.csv", index=False)
    np.savez(out_dir / "features_raw.npz", **window_npz)
    np.savez(out_dir / "run_features_raw.npz", **run_npz)

    with open(out_dir / "selected_scales.json", "w") as f:
        json.dump({
            "n_selected": int(len(sel_rows)),
            "selected_indices": sel_rows.tolist(),
            "dropped_indices": dropped,
            "all_scores": [round(float(s), 4) for s in scores],
            "target": args.target,
            "layout": args.layout,
            "n_windows": args.n_windows,
            "channel": args.channel,
            "feature_cols": feature_cols,
            "n_cols": n_cols,
            "block_sizes": [N_SELECT] * args.n_windows,   # uniform, no padding needed
        }, f, indent=2)

    print(f"\nSaved {len(rows)} PNGs + labels.csv + selected_scales.json + "
          f"features_raw.npz + run_features_raw.npz -> {out_dir}/")
    print("\nClass distribution (by unique run):")
    for col, name in [("ra_class", "Ra class"), ("feed_coarse", "Feed coarse"),
                       ("speed", "Speed"), ("doc", "DOC")]:
        print(f"  {name}:")
        for cls, cnt in labels_df.groupby(col)["run"].nunique().items():
            print(f"    {cls}: {cnt} runs  ({cnt * args.n_windows} windows)")

    print("\nDone.")


if __name__ == "__main__":
    main()
