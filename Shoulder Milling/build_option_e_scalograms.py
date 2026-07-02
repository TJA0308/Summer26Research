"""
Option E scalogram builder -- 64 x 2 FULL-resolution CWT images, NO scale
selection at all.

Motivation: experiments_writeup.md S3 found the Ra-tuned top-32 selection
throws away ~8 coarse CWT rows (36-50) that carry real feed signal;
scalograms_*_feedopt/ fixed that with a top-32-by-feed-Spearman selection
instead, but still caps at exactly 32 of 64 rows, and Spearman is a LINEAR
per-row correlation metric -- it can still miss coarse-scale information
that's predictive of feed non-linearly, or that only shows up jointly
across rows rather than in any single row's correlation score. Option E
skips row selection entirely: keep all 64 CWT scale rows, from both
wavelet families (64mexican, 64coif). No FFT/DWT/time-stat columns --
those only have 32 or fewer valid rows and would reintroduce the "dead
zone" zero-padding Option D (scalograms_32x3) was built to avoid (see
scalogram_readme.md).

Algorithm
---------
1. Load all 72 sheets (reuses build_option_c_scalograms.load_all_sheets()).
2. Build a (64, 2) image per window: rows 0-63 = all CWT scales,
   cols = [64mexican, 64coif]. No row selection, no Spearman scoring.
3. Column-wise z-score normalise (fit on all 72 windows), clip to +-3
   sigma, rescale to [0, 255], save as grayscale PNG.
4. Output:
     scalograms_64x2_full/{run_id}_{window}.png   72 images (64 x 2 px)
     scalograms_64x2_full/labels.csv

Usage:
    python build_option_e_scalograms.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from build_option_c_scalograms import load_all_sheets, ra_class

CWT_COLS = [2, 3]   # 64mexican, 64coif


def build_opt_e(full_img: np.ndarray) -> np.ndarray:
    return full_img[:, CWT_COLS]   # (64, 2): all 64 rows, both CWT wavelet columns


def main():
    OUT_DIR = Path(__file__).parent / "scalograms_64x2_full"
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Output dir: {OUT_DIR.name}/")

    print("Loading 72 sheets ...")
    records = load_all_sheets()
    print(f"  {len(records)} sheets loaded")

    print("\nBuilding 64x2 images (no scale selection) ...")
    imgs_raw = np.stack([build_opt_e(r["img"]) for r in records])  # (72, 64, 2)

    flat = imgs_raw.reshape(-1, 2)
    mu, sig = flat.mean(axis=0), flat.std(axis=0)
    sig[sig < 1e-10] = 1.0
    imgs_norm = (imgs_raw - mu) / sig
    imgs_u8 = np.clip((imgs_norm + 3) / 6 * 255, 0, 255).astype(np.uint8)

    rows = []
    for i, rec in enumerate(records):
        sid   = f"{rec['run_id']}_{rec['window']}"
        fname = f"{sid}.png"
        Image.fromarray(imgs_u8[i]).save(OUT_DIR / fname)
        rows.append({
            "filename": fname, "sample_id": sid, "run_id": rec["run_id"],
            "window": rec["window"], "run": rec["run"], "side": rec["side"],
            "feed": rec["feed"], "ra": rec["ra"], "ra_class": ra_class(rec["ra"]),
        })

    labels_df = pd.DataFrame(rows)
    labels_df.to_csv(OUT_DIR / "labels.csv", index=False)
    print(f"  Saved {len(records)} PNGs  ->  {OUT_DIR}/")
    print(f"  Labels written to {OUT_DIR / 'labels.csv'}")
    print("\nDone.")


if __name__ == "__main__":
    main()
