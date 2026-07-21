"""
Build a 32x3 (FFT / Mexican-hat CWT / Coiflet CWT) feature-image dataset for
End Milling from the PRECOMPUTED per-run feature spreadsheets in
data/STLMILAE_DOC{015,03,06}.xlsx -- mirrors Shoulder Milling's Option D
exactly (build_option_d_scalograms.py -> scalograms_32x3/).

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
axis into --n_windows row-blocks (`np.array_split`, deterministic block
sizes for a given n_windows -- e.g. 3 -> [11, 11, 10] rows, 9 ->
[4,4,4,4,4,3,3,3,3] rows), each block saved as one training sample. This is
a deliberate choice to replicate Shoulder Milling's sample-count structure
(3x/9x more windows than runs), not a claim that these are independent real
measurements the way Shoulder Milling's a/b/c windows were.

32 doesn't divide evenly by 3 or 9, so the row-blocks aren't all the same
size -- every window image is zero-padded (extra rows appended, values 0)
up to the largest block's size so every "run{N}_w{K}.png" for a given
n_windows has an IDENTICAL shape. This is required because
build_residual_scalograms.py (reused unmodified downstream) averages every
image sharing a (DOC, speed) condition group and needs a uniform array
shape to do that; padding here avoids having to touch that shared script.

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

  <out_dir>/run{N}_w{K}.png       grayscale uint8 PNG (rows_K, 3), K = 0..n_windows-1
  <out_dir>/labels.csv            filename, sample_id, run, window, speed, doc,
                                   feed, feed_coarse, ra, ra_label, ra_class
  <out_dir>/selected_scales.json  selected/dropped CWT scale indices, all 64 scores,
                                   and the row-block sizes for this n_windows
  <out_dir>/features_raw.npz      pre-quantization float32 (rows_K, 3) arrays per
                                   sample_id -- for smote_generate_32x3.py, which
                                   should not SMOTE-interpolate lossy uint8 pixels.
  <out_dir>/run_features_raw.npz  pre-quantization float32 (32, 3) arrays per RUN
                                   (i.e. the full image before any window split) --
                                   for pca_analysis_32x3.py, which should analyse
                                   the real 32x3 feature space, not row fragments
                                   of it.

Usage:
    python build_32x3_features.py --target roughness
    python build_32x3_features.py --target feed_coarse
    python build_32x3_features.py --target roughness    --n_windows 9
    python build_32x3_features.py --target feed_coarse  --n_windows 9
"""
import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd
from PIL import Image
from scipy.stats import spearmanr

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
N_FULL = 64      # raw scale rows in the source spreadsheets
N_SELECT = 32    # selected CWT scales (rows of the output image)

FEATURE_COLS = [
    "32FFT", "5statistics", "64mexican", "64coif",
    "KA", "SA", "KD", "SD", "rmsA", "rmsD", "crestfactA", "crestfactD",
]
COL_IDX = {c: i for i, c in enumerate(FEATURE_COLS)}

# One workbook per DOC level -- confirmed present with 15 sheets each,
# "s{speed_rpm}f{feed_mmrev}", covering all 45 (DOC, speed, feed) runs.
DOC_FILE = {0: "STLMILAE_DOC015.xlsx", 1: "STLMILAE_DOC03.xlsx", 2: "STLMILAE_DOC06.xlsx"}

RUNS = [f"run{i}" for i in range(1, 46)]

# Continuous surface roughness Ra (um) per run -- transcribed from the
# per-run comments in cnn_model/cnn_train.py's RA_LABELS (that file only
# stores the discretized 3-class label; the um values live in its comments).
RA_VALUES = {
    "run1": 0.392, "run2": 0.282, "run3": 0.328,
    "run4": 0.302, "run5": 0.424, "run6": 0.448,
    "run7": 0.930, "run8": 0.852, "run9": 0.558,
    "run10": 0.640, "run11": 0.896, "run12": 0.902,
    "run13": 0.494, "run14": 0.418, "run15": 0.482,
    "run16": 0.834, "run17": 0.678, "run18": 0.384,
    "run19": 0.864, "run20": 1.048, "run21": 1.638,
    "run22": 1.186, "run23": 0.814, "run24": 0.726,
    "run25": 0.596, "run26": 0.838, "run27": 0.868,
    "run28": 1.340, "run29": 1.108, "run30": 1.010,
    "run31": 0.820, "run32": 1.612, "run33": 1.490,
    "run34": 2.084, "run35": 1.980, "run36": 1.790,
    "run37": 0.416, "run38": 0.302, "run39": 0.326,
    "run40": 0.328, "run41": 0.304, "run42": 0.454,
    "run43": 0.364, "run44": 0.314, "run45": 0.414,
}


def _load_cnn_train_module():
    spec = importlib.util.spec_from_file_location("cnn_train", ROOT / "cnn_model" / "cnn_train.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sheet_name_for_run(run: str, mod) -> str:
    speed_rpm = int(mod.SPEED_NAMES[mod.SPEED_LABELS[run]].split()[0])
    feed_mmrev = mod.FEED_LABELS[run] + 3   # FEED_LABELS 0..5 -> 3..8 mm/rev
    return f"s{speed_rpm}f{feed_mmrev}"


def load_all_run_images(mod) -> dict:
    """Returns {run: (64, 12) float64 array} read straight from the 3
    per-DOC workbooks -- no padding needed, every sheet is exactly 64 rows."""
    wb_cache = {}
    images = {}
    for run in RUNS:
        doc = mod.DOC_LABELS[run]
        fname = DOC_FILE[doc]
        if fname not in wb_cache:
            wb_cache[fname] = openpyxl.load_workbook(DATA_DIR / fname, read_only=True, data_only=True)
        ws = wb_cache[fname][sheet_name_for_run(run, mod)]
        data_rows = list(ws.iter_rows(min_row=2, max_row=1 + N_FULL, values_only=True))
        images[run] = np.array(data_rows, dtype=np.float64)   # (64, 12)
    return images


def select_cwt_rows(images: dict, mod, target: str) -> tuple:
    """Identical method to Option D's select_cwt_rows(): Spearman |rho| of
    each of the 64 mexican/coif scale rows against the target, averaged,
    top-32, re-sorted ascending. target: 'roughness' -> Ra (um),
    'feed_coarse' -> feed rate (mm/rev)."""
    runs = sorted(images.keys(), key=lambda s: int(s[3:]))
    mex = np.stack([images[r][:, COL_IDX["64mexican"]] for r in runs])   # (45, 64)
    coi = np.stack([images[r][:, COL_IDX["64coif"]] for r in runs])      # (45, 64)

    if target == "roughness":
        target_arr = np.array([RA_VALUES[r] for r in runs])
    elif target == "feed_coarse":
        target_arr = np.array([mod.FEED_LABELS[r] + 3 for r in runs])
    else:
        raise ValueError(target)

    scores = np.zeros(N_FULL)
    for row_i in range(N_FULL):
        s_mex, _ = spearmanr(mex[:, row_i], target_arr)
        s_coi, _ = spearmanr(coi[:, row_i], target_arr)
        s_mex = 0.0 if np.isnan(s_mex) else abs(s_mex)
        s_coi = 0.0 if np.isnan(s_coi) else abs(s_coi)
        scores[row_i] = (s_mex + s_coi) / 2.0

    top_idx = np.sort(np.argsort(scores)[::-1][:N_SELECT])
    return top_idx, scores


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
    out_dir.mkdir(exist_ok=True)
    print(f"Target: {args.target}  |  n_windows={args.n_windows}")
    print(f"Output dir: {out_dir}/")

    mod = _load_cnn_train_module()

    print("\nLoading precomputed feature sheets (data/STLMILAE_DOC*.xlsx) ...")
    images = load_all_run_images(mod)
    print(f"  {len(images)} runs loaded")

    print(f"\nSelecting top-{N_SELECT} of {N_FULL} CWT scale rows (target={args.target}) ...")
    sel_rows, scores = select_cwt_rows(images, mod, args.target)
    dropped = sorted(set(range(N_FULL)) - set(sel_rows.tolist()))
    print(f"  Selected indices ({len(sel_rows)}): {sel_rows.tolist()}")

    print("\nBuilding 32x3 images (one per run) ...")
    runs_sorted = sorted(images.keys(), key=lambda s: int(s[3:]))
    run_imgs_raw = np.stack([build_run_image(images[r], sel_rows) for r in runs_sorted])   # (45, 32, 3)

    # Column-wise z-score normalisation (fit on all 45 runs), clip +-3 sigma,
    # rescale to [0, 255] -- identical convention to Option D.
    flat = run_imgs_raw.reshape(-1, 3)
    mu = flat.mean(axis=0)
    sig = flat.std(axis=0)
    sig[sig < 1e-10] = 1.0
    run_imgs_norm = (run_imgs_raw - mu) / sig
    run_imgs_u8 = np.clip((run_imgs_norm + 3) / 6 * 255, 0, 255).astype(np.uint8)

    # Row-blocks for this n_windows -- deterministic, identical across every
    # run (depends only on 32 and n_windows, not on the data). 32 doesn't
    # divide evenly by 3 or 9, so np.array_split gives uneven block sizes
    # (e.g. [11,11,10] for 3, [4,4,4,4,4,3,3,3,3] for 9). Every window image
    # is zero-padded to the SAME (largest) block size -- not left uneven --
    # because build_residual_scalograms.py (reused unmodified downstream)
    # averages all images sharing a (DOC, speed) condition group and requires
    # a uniform array shape to do so; padding here keeps that script working
    # without touching it. The padded rows carry no signal (documented, not
    # silently different from the real 32-row image).
    block_idx = [b.tolist() for b in np.array_split(np.arange(N_SELECT), args.n_windows)]
    real_block_sizes = [len(b) for b in block_idx]
    pad_size = max(real_block_sizes)
    print(f"  Row-block sizes for n_windows={args.n_windows}: {real_block_sizes}  "
          f"(zero-padded to {pad_size} rows each for uniform image shape)")

    with open(out_dir / "selected_scales.json", "w") as f:
        json.dump({
            "n_selected": int(len(sel_rows)),
            "selected_indices": sel_rows.tolist(),
            "dropped_indices": dropped,
            "all_scores": [round(float(s), 4) for s in scores],
            "target": args.target,
            "n_windows": args.n_windows,
            "block_row_indices": block_idx,
            "real_block_sizes": real_block_sizes,
            "padded_block_size": pad_size,
            "block_sizes": [pad_size] * args.n_windows,
        }, f, indent=2)

    rows = []
    window_npz = {}
    run_npz = {}
    for ri, run in enumerate(runs_sorted):
        run_npz[run] = run_imgs_raw[ri]
        speed = mod.SPEED_LABELS[run]
        doc = mod.DOC_LABELS[run]
        feed = mod.FEED_LABELS[run]
        feed_coarse = mod.FEED_COARSE_LABELS[run]
        ra_label = mod.RA_LABELS[run]
        ra = RA_VALUES[run]

        for k, idx in enumerate(block_idx):
            sample_id = f"{run}_w{k}"
            fname = f"{sample_id}.png"
            pad_rows = pad_size - len(idx)

            block_u8 = run_imgs_u8[ri, idx, :]
            block_raw = run_imgs_raw[ri, idx, :].astype(np.float32)
            if pad_rows > 0:
                block_u8 = np.pad(block_u8, ((0, pad_rows), (0, 0)))
                block_raw = np.pad(block_raw, ((0, pad_rows), (0, 0)))

            Image.fromarray(block_u8).save(out_dir / fname)
            window_npz[sample_id] = block_raw
            rows.append({
                "filename": fname, "sample_id": sample_id, "run": run, "window": k,
                "speed": speed, "doc": doc, "feed": feed, "feed_coarse": feed_coarse,
                "ra": ra, "ra_label": ra_label, "ra_class": mod.RA_NAMES[ra_label],
            })

    labels_df = pd.DataFrame(rows)
    labels_df.to_csv(out_dir / "labels.csv", index=False)
    np.savez(out_dir / "features_raw.npz", **window_npz)
    np.savez(out_dir / "run_features_raw.npz", **run_npz)

    print(f"  Saved {len(rows)} PNGs + labels.csv + features_raw.npz + "
          f"run_features_raw.npz -> {out_dir}/")
    print("\nClass distribution (by unique run):")
    for col, name in [("ra_class", "Ra class"), ("feed_coarse", "Feed coarse"),
                       ("speed", "Speed"), ("doc", "DOC")]:
        print(f"  {name}:")
        for cls, cnt in labels_df.groupby(col)["run"].nunique().items():
            print(f"    {cls}: {cnt} runs  ({cnt * args.n_windows} windows)")

    print("\nDone.")


if __name__ == "__main__":
    main()
