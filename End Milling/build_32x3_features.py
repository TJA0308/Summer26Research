"""
Build a 32x3 (FFT / Mexican-hat CWT / Coiflet CWT) feature-image dataset for
End Milling from the PRECOMPUTED per-run feature spreadsheets in
data/STLMILAE_DOC{015,03,06}.xlsx -- mirrors Shoulder Milling's Option D
exactly (build_option_d_scalograms.py -> scalograms_32x3/). See sibling
build_32x12_features.py for the Option C analog (all 12 feature columns);
both share loading/scale-selection/windowing code in em_feature_common.py.

Confirmed by direct inspection (not assumed): those 3 workbooks have the
IDENTICAL 12-column feature schema Shoulder Milling's Side*.xlsx use --
32FFT, 5statistics, 64mexican, 64coif, KA, SA, KD, SD, rmsA, rmsD,
crestfactA, crestfactD -- 64 data rows each. One workbook per DOC level
(015/03/06 mm), 15 sheets each named "s{speed}f{feed}" (e.g. "s1500f3"),
45 sheets total = 45 runs. So the FFT/CWT numbers are READ here, exactly
like Option D, not recomputed from the raw waveform.

Windows -- why they're a row-split here, not a real time re-window
---------------------------------------------------------------------
Shoulder Milling's 3 "windows" per run (a/b/c) were 3 separate real
measurement sheets that existed before any row-splitting; only its `_9win`
variant (split_scalogram_windows.py) is a post-hoc row-split, done because
by that point there was no raw waveform left to re-derive real windows
from. End Milling's precomputed sheets are ONE block per run (no a/b/c
here) -- there is no separate real per-run window granularity in this data
to start from either. So both the 3-window baseline AND the 9-window
variant are produced the same way: split the final (32, 3) image's 32-row
axis into --n_windows row-blocks, zero-padded to a uniform shape (see
em_feature_common.normalize_and_window's docstring for why). This
replicates Shoulder Milling's sample-count structure (3x/9x more windows
than runs), not a claim that these are independent real measurements the
way Shoulder Milling's a/b/c windows were.

Scale selection (top-32-of-64)
-------------------------------
Identical method to Option D (`build_option_d_scalograms.py:select_cwt_rows`):
for each of the 64 scale rows, compute the Spearman |rho| between that row's
value and the target (Ra for --target roughness, feed mm/rev for
--target feed_coarse) across all 45 runs, average the 64mexican and 64coif
scores per row, take the top 32 by averaged |rho|, then sort back into
ascending (fine->coarse) order.

Output (directly consumable by this repo's existing cnn_model/cnn_train.py,
build_residual_scalograms.py, etc., which only care about "run{N}_w{K}.png"
filenames and a labels.csv):

    scalograms_32x3/                    --target roughness (default), n_windows=3
    scalograms_32x3_feedopt/            --target feed_coarse,          n_windows=3
    scalograms_32x3_9win/               --target roughness,            n_windows=9
    scalograms_32x3_feedopt_9win/       --target feed_coarse,          n_windows=9

  <out_dir>/run{N}_w{K}.png       grayscale uint8 PNG, uniform (padded_block_size, 3)
  <out_dir>/labels.csv            filename, sample_id, run, window, speed, doc,
                                   feed, feed_coarse, ra, ra_label, ra_class
  <out_dir>/selected_scales.json  selected/dropped CWT scale indices, all 64 scores,
                                   feature_cols, and the row-block sizes for this n_windows
  <out_dir>/features_raw.npz      pre-quantization float32 per-window blocks -- for
                                   smote_generate_32x3.py, which should not
                                   SMOTE-interpolate lossy uint8 pixels.
  <out_dir>/run_features_raw.npz  pre-quantization float32 (32, 3) arrays per RUN
                                   (the full image before any window split) -- for
                                   pca_analysis_32x3.py, which should analyse the
                                   real 32x3 feature space, not row fragments of it.

Usage:
    python build_32x3_features.py --target roughness
    python build_32x3_features.py --target feed_coarse
    python build_32x3_features.py --target roughness    --n_windows 9
    python build_32x3_features.py --target feed_coarse  --n_windows 9
"""
import argparse

import numpy as np

from em_feature_common import (
    ROOT, COL_IDX, N_SELECT,
    load_cnn_train_module, load_all_run_images, select_cwt_rows, write_dataset,
)

OUT_FEATURE_COLS = ["FFT", "Mexican", "Coiflet"]


def build_run_image(img64x12: np.ndarray, sel_rows: np.ndarray) -> np.ndarray:
    """(32, 3) image: col 0 = 32FFT (native, complete), col 1 = selected
    64mexican rows, col 2 = selected 64coif rows -- identical layout to
    Option D's build_opt_d_window()."""
    out = np.zeros((N_SELECT, 3), dtype=np.float64)
    out[:, 0] = img64x12[:N_SELECT, COL_IDX["32FFT"]]
    out[:, 1] = img64x12[sel_rows, COL_IDX["64mexican"]]
    out[:, 2] = img64x12[sel_rows, COL_IDX["64coif"]]
    return out


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", choices=["roughness", "feed_coarse"], default="roughness",
                        help="Which quantity to correlate CWT scale rows against when "
                             "selecting the top-32 of 64 scales. roughness -> "
                             "scalograms_32x3/, feed_coarse -> scalograms_32x3_feedopt/")
    parser.add_argument("--n_windows", type=int, default=3,
                        help="Row-blocks to split each run's 32-row image into "
                             "(3 = baseline, replicating Shoulder Milling's 3 "
                             "windows/run; 9 -> writes the '_9win' variant)")
    args = parser.parse_args()

    out_name = "scalograms_32x3" if args.target == "roughness" else "scalograms_32x3_feedopt"
    if args.n_windows != 3:
        out_name += f"_{args.n_windows}win"
    out_dir = ROOT / out_name
    print(f"Target: {args.target}  |  n_windows={args.n_windows}")
    print(f"Output dir: {out_dir}/")

    mod = load_cnn_train_module()

    print("\nLoading precomputed feature sheets (data/STLMILAE_DOC*.xlsx) ...")
    images = load_all_run_images(mod)
    print(f"  {len(images)} runs loaded")

    print(f"\nSelecting top-{N_SELECT} of 64 CWT scale rows (target={args.target}) ...")
    sel_rows, scores = select_cwt_rows(images, mod, args.target)
    print(f"  Selected indices ({len(sel_rows)}): {sel_rows.tolist()}")

    print("\nBuilding 32x3 images (one per run) ...")
    runs_sorted = sorted(images.keys(), key=lambda s: int(s[3:]))
    run_imgs_raw = np.stack([build_run_image(images[r], sel_rows) for r in runs_sorted])   # (45, 32, 3)

    write_dataset(out_dir, mod, args.target, args.n_windows, OUT_FEATURE_COLS,
                  runs_sorted, run_imgs_raw, sel_rows, scores)

    print("\nDone.")


if __name__ == "__main__":
    main()
