"""
Shared constants/loading code for End Milling's precomputed-feature-based
scalogram builders (build_32x3_features.py -> Option D analog,
build_32x12_features.py -> Option C analog). Factored out so both builders
read the same Excel data, run/label wiring, and CWT scale-selection method
exactly once, rather than duplicating it.

Source data: data/STLMILAE_DOC{015,03,06}.xlsx -- confirmed by direct
inspection to have the identical 12-column feature schema Shoulder Milling's
Side*.xlsx use: 32FFT, 5statistics, 64mexican, 64coif, KA, SA, KD, SD, rmsA,
rmsD, crestfactA, crestfactD. One workbook per DOC level, 15 sheets each
("s{speed}f{feed}"), 45 sheets total = 45 runs. 64mexican/64coif are filled
for all 64 rows; every other column is genuinely shorter (32FFT: 32 real
values, 5statistics: 6, the 8 DWT-stat columns: 10) with the remaining rows
blank in the spreadsheet -- openpyxl reads those as None, converted to 0.0
here (`np.nan_to_num`), matching Shoulder Milling's own zero-padding
convention for the same columns.
"""
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
N_FULL = 64   # raw scale rows in the source spreadsheets
N_SELECT = 32  # selected CWT scales

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


def load_cnn_train_module():
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
    per-DOC workbooks. Blank cells (columns shorter than 64 real values)
    come back from openpyxl as None -> nan via the array constructor ->
    zeroed here, matching Shoulder Milling's zero-padding convention."""
    wb_cache = {}
    images = {}
    for run in RUNS:
        doc = mod.DOC_LABELS[run]
        fname = DOC_FILE[doc]
        if fname not in wb_cache:
            wb_cache[fname] = openpyxl.load_workbook(DATA_DIR / fname, read_only=True, data_only=True)
        ws = wb_cache[fname][sheet_name_for_run(run, mod)]
        data_rows = list(ws.iter_rows(min_row=2, max_row=1 + N_FULL, values_only=True))
        img = np.array(data_rows, dtype=np.float64)   # (64, 12), blanks -> nan
        images[run] = np.nan_to_num(img, nan=0.0)
    return images


def speed_rpm_value(run: str, mod) -> int:
    return int(mod.SPEED_NAMES[mod.SPEED_LABELS[run]].split()[0])


def doc_mm_value(run: str, mod) -> float:
    return float(mod.DOC_NAMES[mod.DOC_LABELS[run]].split()[0])


def target_values(images: dict, mod, target: str) -> np.ndarray:
    """Run-level continuous (or ordinal) value to correlate CWT scale rows
    against for a given target -- shared by select_cwt_rows() and the
    scale-selection comparison test (compare_scale_selection.py). speed/doc
    use their real physical values (rpm / mm), not the class index, so
    Spearman sees the true ordinal spacing (e.g. DOC classes 0/1/2 map to
    0.015/0.03/0.06 mm -- very unevenly spaced -- not 0/1/2)."""
    runs = sorted(images.keys(), key=lambda s: int(s[3:]))
    if target == "roughness":
        return np.array([RA_VALUES[r] for r in runs])
    if target == "feed_coarse":
        return np.array([mod.FEED_LABELS[r] + 3 for r in runs])   # FEED_LABELS 0..5 -> 3..8 mm/rev
    if target == "speed":
        return np.array([speed_rpm_value(r, mod) for r in runs])
    if target == "doc":
        return np.array([doc_mm_value(r, mod) for r in runs])
    raise ValueError(target)


def cwt_row_scores(images: dict, mod, target: str) -> np.ndarray:
    """Averaged |Spearman rho| of the 64 mexican/coif scale rows against
    the target, one score per row (not yet top-32 selected) -- factored out
    of select_cwt_rows() so compare_scale_selection.py can get scores for
    all 4 targets without re-deriving the correlation method."""
    runs = sorted(images.keys(), key=lambda s: int(s[3:]))
    mex = np.stack([images[r][:, COL_IDX["64mexican"]] for r in runs])   # (45, 64)
    coi = np.stack([images[r][:, COL_IDX["64coif"]] for r in runs])      # (45, 64)
    target_arr = target_values(images, mod, target)

    scores = np.zeros(N_FULL)
    for row_i in range(N_FULL):
        s_mex, _ = spearmanr(mex[:, row_i], target_arr)
        s_coi, _ = spearmanr(coi[:, row_i], target_arr)
        s_mex = 0.0 if np.isnan(s_mex) else abs(s_mex)
        s_coi = 0.0 if np.isnan(s_coi) else abs(s_coi)
        scores[row_i] = (s_mex + s_coi) / 2.0
    return scores


TARGET_DIR_SUFFIX = {
    "roughness": "",             # scalograms_32x3 / scalograms_32x12 (the original default)
    "feed_coarse": "_feedopt",
    "speed": "_speedopt",
    "doc": "_docopt",
}


def out_dir_name(base_name: str, target: str, n_windows: int) -> str:
    """base_name: 'scalograms_32x3' or 'scalograms_32x12'. Shared naming
    convention between build_32x3_features.py and build_32x12_features.py so
    both pipelines' directory names only ever differ by the base_name."""
    name = base_name + TARGET_DIR_SUFFIX[target]
    if n_windows != 3:
        name += f"_{n_windows}win"
    return name


def select_cwt_rows(images: dict, mod, target: str) -> tuple:
    """Top-32-of-64 mexican/coif scale rows by averaged |Spearman rho|
    against the target, re-sorted ascending. target: 'roughness' -> Ra (um),
    'feed_coarse' -> feed rate (mm/rev), 'speed' -> rpm, 'doc' -> mm.
    Identical method regardless of output layout (32x3 or 32x12) -- scale
    selection only ever concerns the two CWT columns."""
    scores = cwt_row_scores(images, mod, target)
    top_idx = np.sort(np.argsort(scores)[::-1][:N_SELECT])
    return top_idx, scores


def normalize_and_window(run_imgs_raw: np.ndarray, n_windows: int) -> tuple:
    """Shared normalisation + windowing for both builders. run_imgs_raw:
    (45, 32, n_cols) float64, one full image per run (rows sorted by run
    number). Returns (run_imgs_u8, block_idx, real_block_sizes, pad_size):

    - Column-wise z-score (fit on all 45 runs), clip +-3 sigma, rescale to
      [0, 255] -- identical convention to Shoulder Milling's Option C/D.
    - 32-row axis split into n_windows row-blocks via np.array_split
      (deterministic, e.g. 3 -> [11,11,10], 9 -> [4,4,4,4,4,3,3,3,3] -- 32
      doesn't divide evenly by 3 or 9). block_idx/real_block_sizes describe
      the true (unpadded) split; pad_size is the largest block, since every
      window image gets zero-padded up to that size for a uniform shape
      (build_residual_scalograms.py, reused unmodified downstream, averages
      images per condition group and needs one).
    """
    n_cols = run_imgs_raw.shape[-1]
    flat = run_imgs_raw.reshape(-1, n_cols)
    mu = flat.mean(axis=0)
    sig = flat.std(axis=0)
    sig[sig < 1e-10] = 1.0
    run_imgs_norm = (run_imgs_raw - mu) / sig
    run_imgs_u8 = np.clip((run_imgs_norm + 3) / 6 * 255, 0, 255).astype(np.uint8)

    block_idx = [b.tolist() for b in np.array_split(np.arange(N_SELECT), n_windows)]
    real_block_sizes = [len(b) for b in block_idx]
    pad_size = max(real_block_sizes)
    return run_imgs_u8, block_idx, real_block_sizes, pad_size


def write_dataset(out_dir: Path, mod, target: str, n_windows: int, feature_cols: list,
                   runs_sorted: list, run_imgs_raw: np.ndarray, sel_rows: np.ndarray,
                   scores: np.ndarray):
    """Shared write path for both builders: normalises + windows
    run_imgs_raw, writes run{N}_w{K}.png (zero-padded to a uniform shape),
    labels.csv, selected_scales.json, features_raw.npz (per-window blocks),
    and run_features_raw.npz (full per-run image, pre-window-split -- for
    PCA)."""
    out_dir.mkdir(exist_ok=True)
    n_cols = run_imgs_raw.shape[-1]
    run_imgs_u8, block_idx, real_block_sizes, pad_size = normalize_and_window(run_imgs_raw, n_windows)
    print(f"  Row-block sizes for n_windows={n_windows}: {real_block_sizes}  "
          f"(zero-padded to {pad_size} rows each for uniform image shape)")

    dropped = sorted(set(range(N_FULL)) - set(sel_rows.tolist()))
    with open(out_dir / "selected_scales.json", "w") as f:
        json.dump({
            "n_selected": int(len(sel_rows)),
            "selected_indices": sel_rows.tolist(),
            "dropped_indices": dropped,
            "all_scores": [round(float(s), 4) for s in scores],
            "target": target,
            "n_windows": n_windows,
            "feature_cols": feature_cols,
            "n_cols": n_cols,
            "block_row_indices": block_idx,
            "real_block_sizes": real_block_sizes,
            "padded_block_size": pad_size,
            "block_sizes": [pad_size] * n_windows,
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
            print(f"    {cls}: {cnt} runs  ({cnt * n_windows} windows)")
