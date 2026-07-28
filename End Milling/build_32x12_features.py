"""
Build a 32x12 feature-image dataset for End Milling from the PRECOMPUTED
per-run feature spreadsheets in data/STLMILAE_DOC{015,03,06}.xlsx --
mirrors Shoulder Milling's Option C exactly (build_option_c_scalograms.py
-> scalograms_32x12/). See sibling build_32x3_features.py for the Option D
analog (FFT/mexican/coif only); both share loading/scale-selection/windowing
code in em_feature_common.py -- see that file and build_32x3_features.py's
docstring for the full data-source and windowing rationale, not repeated
here.

Image layout (32 rows x 12 columns), identical to Option C's build_opt_c():
  col 0  (32FFT)      -- native, complete (32 real values)
  col 1  (5statistics) -- natural truncation: rows 0-5 real, rows 6-31 zero
                          (the spreadsheet only has 6 real values in this
                          column; see em_feature_common's zero-padding note)
  col 2  (64mexican)  -- the SAME top-32-of-64 selected scale rows
  col 3  (64coif)     -- build_32x3_features.py uses, for the same reason
                          Option C did: consistent scale meaning across both
                          CWT columns and across the 32x3/32x12 pipelines
  cols 4-11 (KA, SA, KD, SD, rmsA, rmsD, crestfactA, crestfactD)
                      -- natural truncation: rows 0-9 real, rows 10-31 zero

speed/doc get their own dedicated scale selection (speedopt/docopt dirs)
rather than reusing roughness's or feed_coarse's top-32 rows -- see
build_32x3_features.py's docstring for the compare_scale_selection.py
efficiency numbers that motivated this.

Usage:
    python build_32x12_features.py --target roughness
    python build_32x12_features.py --target feed_coarse
    python build_32x12_features.py --target speed
    python build_32x12_features.py --target doc
    python build_32x12_features.py --target roughness --n_windows 9
"""
import argparse

import numpy as np

from em_feature_common import (
    ROOT, FEATURE_COLS, COL_IDX, N_SELECT,
    load_cnn_train_module, load_all_run_images, select_cwt_rows, write_dataset, out_dir_name,
)

CWT_COLS = {"64mexican", "64coif"}


def build_run_image(img64x12: np.ndarray, sel_rows: np.ndarray) -> np.ndarray:
    """(32, 12) image -- identical layout to Option C's build_opt_c():
    CWT columns get the selected scale rows, every other column is
    naturally truncated to its first 32 rows (already zero beyond its real
    length)."""
    out = np.zeros((N_SELECT, len(FEATURE_COLS)), dtype=np.float64)
    for col, ci in COL_IDX.items():
        if col in CWT_COLS:
            out[:, ci] = img64x12[sel_rows, ci]
        else:
            out[:, ci] = img64x12[:N_SELECT, ci]
    return out


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", choices=["roughness", "feed_coarse", "speed", "doc"], default="roughness",
                        help="Which quantity to correlate CWT scale rows against when "
                             "selecting the top-32 of 64 scales. roughness -> scalograms_32x12/, "
                             "feed_coarse -> scalograms_32x12_feedopt/, speed -> "
                             "scalograms_32x12_speedopt/, doc -> scalograms_32x12_docopt/")
    parser.add_argument("--n_windows", type=int, default=3,
                        help="Row-blocks to split each run's 32-row image into "
                             "(3 = baseline, replicating Shoulder Milling's 3 "
                             "windows/run; 9 -> writes the '_9win' variant)")
    parser.add_argument("--norm_mode", default="global", choices=["global", "per_doc"],
                        help="'global': z-score across all runs. 'per_doc': z-score within "
                             "each DOC group. Adds '_perdoc' suffix to output dir.")
    parser.add_argument("--scale_method", default="spearman", choices=["spearman", "fstat"],
                        help="Scale-row selection criterion. 'spearman' (default): |Spearman rho|. "
                             "'fstat': one-way ANOVA F-statistic across target classes. "
                             "fstat dirs get a '_fstat' suffix.")
    args = parser.parse_args()

    base = "scalograms_32x12"
    out_dir_base = out_dir_name(base, args.target, args.n_windows)
    if args.scale_method == "fstat":
        out_dir_base += "_fstat"
    if args.norm_mode == "per_doc":
        out_dir_base += "_perdoc"
    out_dir = ROOT / out_dir_base
    print(f"Target: {args.target}  |  n_windows={args.n_windows}  |  scale_method={args.scale_method}")
    print(f"Output dir: {out_dir}/")

    mod = load_cnn_train_module()

    print("\nLoading precomputed feature sheets (data/STLMILAE_DOC*.xlsx) ...")
    images = load_all_run_images(mod)
    print(f"  {len(images)} runs loaded")

    print(f"\nSelecting top-{N_SELECT} of 64 CWT scale rows (target={args.target}, method={args.scale_method}) ...")
    sel_rows, scores = select_cwt_rows(images, mod, args.target, method=args.scale_method)
    print(f"  Selected indices ({len(sel_rows)}): {sel_rows.tolist()}")

    print("\nBuilding 32x12 images (one per run) ...")
    runs_sorted = sorted(images.keys(), key=lambda s: int(s[3:]))
    run_imgs_raw = np.stack([build_run_image(images[r], sel_rows) for r in runs_sorted])   # (45, 32, 12)

    write_dataset(out_dir, mod, args.target, args.n_windows, FEATURE_COLS,
                  runs_sorted, run_imgs_raw, sel_rows, scores, norm_mode=args.norm_mode)

    print("\nDone.")


if __name__ == "__main__":
    main()
