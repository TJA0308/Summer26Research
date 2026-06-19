"""
Option D scalogram builder -- 32 x 3 grayscale images, one per window (72 total).

Same per-window layout as Option C (build_option_c_scalograms.py) but
restricted to only the 3 feature columns the user wants: FFT, Mexican
hat CWT, and Coiflet CWT. The 32 rows for the two CWT columns are the
same Ra-correlated scale rows Option C selects; the FFT column already
has exactly 32 bins, so no zero-padding or truncation is needed there.

Algorithm
---------
1. Load all 72 sheets (8 sides x 9 sheets each = 24 runs x 3 windows).
2. Select the top-32 64mexican/64coif scale rows by averaged Spearman
   |rho| with Ra (run-level averages, 24 points) -- identical method
   to Option C.
3. For each of the 72 windows, build a (32, 3) image:
     col 0 = 32FFT[0:32]              (native, complete)
     col 1 = 64mexican[selected_rows]
     col 2 = 64coif[selected_rows]
4. Column-wise z-score normalise (fit on all 72 windows), clip +-3
   sigma, rescale to [0, 255], save as grayscale PNG.
5. Output:
     scalograms_32x3/{side}{feed}{window}.png   72 images (32 x 3 px, grayscale), e.g. "1a1.png"
     scalograms_32x3/labels.csv
     scalograms_32x3/selected_scales.json
     scalograms_32x3/option_d_all_windows.png   diagnostic grid
"""

import argparse
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from scipy.stats import spearmanr

DATA_DIR = Path(__file__).parent / "data"

FEATURE_COLS = [
    "32FFT", "5statistics", "64mexican", "64coif",
    "KA", "SA", "KD", "SD", "rmsA", "rmsD", "crestfactA", "crestfactD",
]
N_FULL = 64   # original image height
N_OUT  = 32   # output image height
OUT_COLS = ["32FFT", "64mexican", "64coif"]
FEED_NUM = {"f3": 3, "f5": 5, "f7": 7}  # ordinal feed value, used when --target feed

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


def select_cwt_rows(records: list, n_select: int = 32, target: str = "ra"):
    """Identical method to Option C: returns (selected_indices, all_scores).
    target: "ra" (default) or "feed" -- which run-level quantity to
    correlate each CWT scale row against."""
    unique_runs = sorted({r["run"] for r in records})
    run_idx     = {rn: i for i, rn in enumerate(unique_runs)}
    n_runs      = len(unique_runs)

    cwt_sum    = np.zeros((n_runs, N_FULL, 2), dtype=np.float64)
    cnt        = np.zeros(n_runs, dtype=int)
    target_arr = np.zeros(n_runs, dtype=np.float64)

    for rec in records:
        ri = run_idx[rec["run"]]
        cwt_sum[ri, :, 0] += rec["img"][:, 2]  # 64mexican
        cwt_sum[ri, :, 1] += rec["img"][:, 3]  # 64coif
        cnt[ri]            += 1
        target_arr[ri]      = rec["ra"] if target == "ra" else FEED_NUM[rec["feed"]]

    cwt_mean = cwt_sum / cnt[:, np.newaxis, np.newaxis]  # (24, 64, 2)

    scores = np.zeros(N_FULL)
    for row_i in range(N_FULL):
        s_mex, _ = spearmanr(cwt_mean[:, row_i, 0], target_arr)
        s_coi, _ = spearmanr(cwt_mean[:, row_i, 1], target_arr)
        s_mex = 0.0 if np.isnan(s_mex) else abs(s_mex)
        s_coi = 0.0 if np.isnan(s_coi) else abs(s_coi)
        scores[row_i] = (s_mex + s_coi) / 2.0

    top_idx = np.sort(np.argsort(scores)[::-1][:n_select])
    return top_idx, scores


def build_opt_d_window(full_img: np.ndarray, sel_rows: np.ndarray) -> np.ndarray:
    """Build (32, 3) Option-D image from one window's full (64, 12) image."""
    out = np.zeros((N_OUT, 3), dtype=np.float32)
    out[:, 0] = full_img[:N_OUT, 0]      # 32FFT, native complete
    out[:, 1] = full_img[sel_rows, 2]    # 64mexican, selected rows
    out[:, 2] = full_img[sel_rows, 3]    # 64coif, selected rows
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["ra", "feed"], default="ra",
                        help="Which run-level quantity to correlate CWT scale rows against "
                             "when selecting the top-32 rows (default: ra / surface roughness). "
                             "target=feed writes to scalograms_32x3_feedopt/ instead.")
    args = parser.parse_args()

    out_dir_name = "scalograms_32x3" if args.target == "ra" else "scalograms_32x3_feedopt"
    OUT_DIR = Path(__file__).parent / out_dir_name
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Target: {args.target}  ->  output dir: {OUT_DIR.name}/")

    print("Loading 72 sheets ...")
    records = load_all_sheets()
    print(f"  {len(records)} sheets loaded")

    print(f"\nSelecting 32 CWT scale rows (target={args.target}) ...")
    sel_rows, scores = select_cwt_rows(records, target=args.target)
    dropped = sorted(set(range(64)) - set(sel_rows.tolist()))
    print(f"  Selected indices ({len(sel_rows)}): {sel_rows.tolist()}")

    with open(OUT_DIR / "selected_scales.json", "w") as f:
        json.dump({
            "n_selected":       int(len(sel_rows)),
            "selected_indices": sel_rows.tolist(),
            "dropped_indices":  dropped,
            "all_scores":       [round(float(s), 4) for s in scores],
        }, f, indent=2)

    print("\nBuilding 32x3 images, one per window ...")
    imgs_raw = np.stack([build_opt_d_window(r["img"], sel_rows) for r in records])  # (72,32,3)

    # Column-wise z-score normalisation (fit on all 72 windows)
    flat = imgs_raw.reshape(-1, 3)
    mu   = flat.mean(axis=0)
    sig  = flat.std(axis=0)
    sig[sig < 1e-10] = 1.0
    imgs_norm = (imgs_raw - mu) / sig

    imgs_u8 = np.clip((imgs_norm + 3) / 6 * 255, 0, 255).astype(np.uint8)

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

    print("\nRa class distribution (by unique runs):")
    for cls, cnt in labels_df.groupby("ra_class")["run"].nunique().items():
        print(f"  {cls:4s}: {cnt} runs  ({cnt*3} windows)")

    # ── diagnostic grid: one example window per run, upsampled ─────────────
    class_color = {"Low": "steelblue", "Med": "darkorange", "High": "crimson"}
    first_per_run = {}
    for i, rec in enumerate(records):
        if rec["run"] not in first_per_run:
            first_per_run[rec["run"]] = i
    run_nums = sorted(first_per_run.keys())

    fig, axes = plt.subplots(4, 6, figsize=(14, 10))
    for k, rn in enumerate(run_nums):
        i = first_per_run[rn]
        row = rows[i]
        pil = Image.fromarray(imgs_u8[i]).resize((96, 96 * 32 // 3), Image.NEAREST)
        ax = axes[k // 6, k % 6]
        ax.imshow(np.array(pil), cmap="gray", origin="upper")
        cls = row["ra_class"]
        ax.set_title(f"Run {rn} ({row['window']})\nRa={row['ra']:.2f} ({cls})", fontsize=7,
                     color=class_color[cls], pad=2)
        ax.set_xticks([]); ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_edgecolor(class_color[cls])
            spine.set_linewidth(2)
    fig.suptitle("Option D: 32x3 grayscale scalograms (cols = FFT, 64mexican, 64coif)\n"
                 "32 rows = top Spearman-correlated CWT scales (same selection as Option C) | one example window per run",
                 fontsize=11, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "option_d_all_windows.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nDiagnostic grid saved to {OUT_DIR/'option_d_all_windows.png'}")
    print("Done.")


if __name__ == "__main__":
    main()
