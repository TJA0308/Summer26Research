"""
Option C scalogram builder — 32 x 12 feature-selected images.

Algorithm
---------
1. Load all 72 sheets (8 sides x 9 sheets each).
2. For 64mexican (col 2) and 64coif (col 3), compute Spearman |rho|
   between each of the 64 scale rows and Ra using run-level averages
   (24 data points — one per physical run, not per window).
   Average the two channels' scores and pick the top-32 row indices.
3. Build a (32, 12) image per window:
     CWT cols (2, 3): 32 selected rows from 0-63
     FFT col  (0):    rows 0-31  (natural 32 bins, complete — no zero-pad)
     Other cols:      rows 0-31  (DWT stats end at row 9, stats end at row 5;
                                  rows beyond still zero but far fewer than in 64-row image)
4. Column-wise z-score normalise (fit on all 72 windows).
   Clip to +-3 sigma, rescale to [0, 255], save as grayscale PNG.
5. Output:
     scalograms_32x12/{side}{feed}{window}.png   72 images (32 x 12 px), e.g. "1a1.png"
     scalograms_32x12/labels.csv
     scalograms_32x12/selected_scales.json
     scalograms_32x12/scale_selection_summary.png
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from scipy.stats import spearmanr

DATA_DIR = Path(__file__).parent / "data"
OUT_DIR  = Path(__file__).parent / "scalograms_32x12"
OUT_DIR.mkdir(exist_ok=True)

FEATURE_COLS = [
    "32FFT", "5statistics", "64mexican", "64coif",
    "KA", "SA", "KD", "SD", "rmsA", "rmsD", "crestfactA", "crestfactD",
]
N_FULL  = 64   # original image height
N_OUT   = 32   # output image height
CWT_COLS = [2, 3]  # 64mexican, 64coif — data-driven row selection

SIDE_TO_RUNS = {
    1: (1,  2,  3),
    2: (13, 14, 15),
    3: (4,  5,  6),
    4: (16, 17, 18),
    5: (7,  8,  9),
    6: (19, 20, 21),
    7: (10, 11, 12),
    8: (22, 23, 24),
}

# Sample ID convention (shared with the train/test split README):
# [side 1-8][feed letter a=f3/b=f5/c=f7][time-window number 1/2/3]
FEED_TO_LETTER = {"f3": "a", "f5": "b", "f7": "c"}
WINDOW_TO_NUM  = {"a": "1", "b": "2", "c": "3"}


def sample_id(side: int, feed: str, window: str) -> str:
    return f"{side}{FEED_TO_LETTER[feed]}{WINDOW_TO_NUM[window]}"


def ra_class(ra: float) -> str:
    if ra <= 0.30:  return "Low"
    if ra <= 0.50:  return "Med"
    return "High"


def load_ra() -> dict:
    raw = pd.read_excel(DATA_DIR / "Surface Roughness_Data.xlsx", header=None)
    run_ra = {}
    for _, row in raw.iterrows():
        try:
            run_ra[int(float(row[1]))] = float(row[11])
        except Exception:
            pass
    return run_ra


def sheet_to_image(df_raw: pd.DataFrame) -> np.ndarray:
    df = df_raw.copy()
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    df = df.apply(pd.to_numeric, errors="coerce")
    img = np.zeros((N_FULL, len(FEATURE_COLS)), dtype=np.float32)
    for ci, col in enumerate(FEATURE_COLS):
        if col not in df.columns:
            continue
        vals = df[col].dropna().values.astype(np.float32)
        n = min(len(vals), N_FULL)
        img[:n, ci] = vals[:n]
    return img


def load_all_sheets() -> list:
    run_ra  = load_ra()
    records = []
    for side_num in range(1, 9):
        xl       = pd.ExcelFile(DATA_DIR / f"Side{side_num}.xlsx")
        run_nums = SIDE_TO_RUNS[side_num]
        for sheet in xl.sheet_names:
            fk      = "f3" if "f3" in sheet else ("f5" if "f5" in sheet else "f7")
            run_num = run_nums[{"f3": 0, "f5": 1, "f7": 2}[fk]]
            window  = sheet.split("_")[-1]
            img     = sheet_to_image(xl.parse(sheet, header=None))
            records.append({
                "img":    img,
                "run":    run_num,
                "side":   side_num,
                "feed":   fk,
                "window": window,
                "ra":     run_ra[run_num],
            })
    return records


def select_cwt_rows(records: list, n_select: int = 32):
    """
    Returns (selected_indices, all_scores).
    selected_indices: sorted array of 32 row indices chosen from 0-63.
    all_scores: (64,) averaged |rho| for each scale row.
    """
    unique_runs = sorted({r["run"] for r in records})
    run_idx     = {rn: i for i, rn in enumerate(unique_runs)}
    n_runs      = len(unique_runs)

    # Accumulate run-level means (average 3 windows per run)
    cwt_sum = np.zeros((n_runs, N_FULL, 2), dtype=np.float64)
    cnt     = np.zeros(n_runs, dtype=int)
    ra_arr  = np.zeros(n_runs, dtype=np.float64)

    for rec in records:
        ri = run_idx[rec["run"]]
        cwt_sum[ri, :, 0] += rec["img"][:, 2]  # 64mexican
        cwt_sum[ri, :, 1] += rec["img"][:, 3]  # 64coif
        cnt[ri]            += 1
        ra_arr[ri]          = rec["ra"]

    cwt_mean = cwt_sum / cnt[:, np.newaxis, np.newaxis]  # (24, 64, 2)

    scores = np.zeros(N_FULL)
    for row_i in range(N_FULL):
        s_mex, _ = spearmanr(cwt_mean[:, row_i, 0], ra_arr)
        s_coi, _ = spearmanr(cwt_mean[:, row_i, 1], ra_arr)
        s_mex = 0.0 if np.isnan(s_mex) else abs(s_mex)
        s_coi = 0.0 if np.isnan(s_coi) else abs(s_coi)
        scores[row_i] = (s_mex + s_coi) / 2.0

    top_idx = np.sort(np.argsort(scores)[::-1][:n_select])
    return top_idx, scores


def build_opt_c(full_img: np.ndarray, sel_rows: np.ndarray) -> np.ndarray:
    """Build (32, 12) Option-C image from full (64, 12) image."""
    out = np.zeros((N_OUT, len(FEATURE_COLS)), dtype=np.float32)
    for c in CWT_COLS:
        out[:, c] = full_img[sel_rows, c]
    for c in range(len(FEATURE_COLS)):
        if c not in CWT_COLS:
            out[:, c] = full_img[:N_OUT, c]
    return out


def main():
    print("Loading 72 sheets ...")
    records = load_all_sheets()
    print(f"  {len(records)} sheets loaded")

    print("\nSelecting 32 CWT scale rows ...")
    sel_rows, scores = select_cwt_rows(records)
    dropped = sorted(set(range(64)) - set(sel_rows.tolist()))

    print(f"  Selected indices ({len(sel_rows)}): {sel_rows.tolist()}")
    print(f"  Score range (selected): {scores[sel_rows].min():.3f} – {scores[sel_rows].max():.3f}")
    print(f"  Score range (dropped):  {scores[dropped].min():.3f} – {scores[dropped].max():.3f}")
    print(f"  Threshold: {scores[sel_rows].min():.3f}")

    # Save scale selection metadata
    with open(OUT_DIR / "selected_scales.json", "w") as f:
        json.dump({
            "n_selected":       int(len(sel_rows)),
            "selected_indices": sel_rows.tolist(),
            "dropped_indices":  dropped,
            "all_scores":       [round(float(s), 4) for s in scores],
        }, f, indent=2)

    # Build all 32x12 images
    print("\nBuilding 32x12 images ...")
    imgs_raw = np.stack([build_opt_c(r["img"], sel_rows) for r in records])  # (72,32,12)

    # Column-wise z-score normalisation (fit on all 72 windows)
    flat = imgs_raw.reshape(-1, len(FEATURE_COLS))
    mu   = flat.mean(axis=0)
    sig  = flat.std(axis=0)
    sig[sig < 1e-10] = 1.0
    imgs_norm = (imgs_raw - mu) / sig  # (72,32,12)

    # Clip to +-3 sigma, map to [0,255] uint8
    imgs_u8 = np.clip((imgs_norm + 3) / 6 * 255, 0, 255).astype(np.uint8)

    # Save PNGs + labels
    rows = []
    for i, rec in enumerate(records):
        sid   = sample_id(rec["side"], rec["feed"], rec["window"])
        fname = f"{sid}.png"
        Image.fromarray(imgs_u8[i]).save(OUT_DIR / fname)
        rows.append({
            "filename":  fname,
            "sample_id": sid,
            "run":       rec["run"],
            "window":    f"w{WINDOW_TO_NUM[rec['window']]}",
            "side":      rec["side"],
            "feed":      rec["feed"],
            "ra":        rec["ra"],
            "ra_class":  ra_class(rec["ra"]),
        })

    labels_df = pd.DataFrame(rows)
    labels_df.to_csv(OUT_DIR / "labels.csv", index=False)

    print(f"  Saved {len(records)} PNGs  ->  {OUT_DIR}/")
    print(f"  Labels written to {OUT_DIR/'labels.csv'}")

    # Ra class summary
    print("\nRa class distribution (by unique runs):")
    for cls, cnt in labels_df.groupby("ra_class")["run"].nunique().items():
        print(f"  {cls:4s}: {cnt} runs  ({cnt*3} windows)")

    # ── visualisation ─────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 5))
    gs  = fig.add_gridspec(1, 3, hspace=0.45, wspace=0.35)

    # Panel 1: score bar chart for all 64 scales
    ax1 = fig.add_subplot(gs[0, :2])
    colors = ["tomato" if i in sel_rows else "steelblue" for i in range(64)]
    ax1.bar(range(64), scores, color=colors, alpha=0.85, width=0.9)
    ax1.axhline(scores[sel_rows].min(), color="tomato", linestyle="--",
                linewidth=0.9, label=f"threshold = {scores[sel_rows].min():.3f}")
    ax1.set_xlabel("CWT scale row index  (0 = finest / high-freq)")
    ax1.set_ylabel("Avg Spearman |rho| with Ra")
    ax1.set_title("Scale-row selection: Spearman |rho| averaged over 64mexican + 64coif\n"
                  "Red = top-32 selected   Blue = dropped")
    ax1.legend(fontsize=8)

    # Panel 2: selected vs dropped counts per zone
    ax2 = fig.add_subplot(gs[0, 2])
    zones = ["0-9 (DWT+)", "10-31 (FFT+)", "32-63 (CWT only)"]
    ranges = [(0, 10), (10, 32), (32, 64)]
    sel_set = set(sel_rows.tolist())
    sel_cnt = [sum(1 for i in range(a,b) if i in sel_set) for a,b in ranges]
    drp_cnt = [(b-a)-s for (a,b),s in zip(ranges, sel_cnt)]
    x = np.arange(len(zones))
    ax2.bar(x - 0.2, sel_cnt, width=0.35, color="tomato",  label="selected")
    ax2.bar(x + 0.2, drp_cnt, width=0.35, color="steelblue", label="dropped")
    ax2.set_xticks(x)
    ax2.set_xticklabels(zones, fontsize=8, rotation=15)
    ax2.set_ylabel("Number of rows")
    ax2.set_title("Selection by zone")
    ax2.legend(fontsize=8)

    fig.suptitle("Option C — scale row selection\n"
                 "CWT rows: top-32 Spearman scales  |  FFT: natural 32 bins  |  Other: rows 0-31",
                 fontsize=11, y=1.03)

    out_plot = OUT_DIR / "scale_selection_summary.png"
    fig.savefig(out_plot, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nSummary plot saved to {out_plot}")
    print("\nDone.")


if __name__ == "__main__":
    main()
