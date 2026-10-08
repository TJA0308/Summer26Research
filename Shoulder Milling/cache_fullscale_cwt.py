"""
Cache the full 64-row CWT/feature images (before top-32 scale selection) as
.npy so nested_preproc.FeedoptNested can redo scale selection per LOCO fold.

Source: data/Side1..8.xlsx (one sheet per window; columns 64mexican / 64coif
are the CWT scale rows, already computed upstream -- the RAW vibration signals
and the CWT code are NOT in this repo, only these precomputed per-window
feature sheets). If data/Side*.xlsx is absent this script exits with an error.

Output (default Shoulder Milling/fullscale_cwt/):
    full_images.npy   float32 (72, 64, 12)  raw, un-normalised, FEATURE_COLS order
    sample_ids.npy    (72,) str  e.g. "s25f3y5z25_a" (join key to labels.csv)

Usage:
    python cache_fullscale_cwt.py [--out fullscale_cwt]
"""
import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="fullscale_cwt")
    args = ap.parse_args()

    missing = [f"Side{i}.xlsx" for i in range(1, 9) if not (DATA_DIR / f"Side{i}.xlsx").exists()]
    if not (DATA_DIR / "Surface Roughness_Data.xlsx").exists():
        missing.append("Surface Roughness_Data.xlsx")
    if missing:
        sys.exit(f"ERROR: raw data not found in {DATA_DIR}: {missing}. "
                 "Full-scale CWT cannot be built without these files.")

    from build_option_c_scalograms import load_all_sheets  # reuse the exact loader
    records = load_all_sheets()
    ids = np.array([f"{r['run_id']}_{r['window']}" for r in records])
    arr = np.stack([r["img"] for r in records]).astype(np.float32)

    out = ROOT / args.out
    out.mkdir(exist_ok=True)
    np.save(out / "full_images.npy", arr)
    np.save(out / "sample_ids.npy", ids)
    print(f"Saved {arr.shape} -> {out}/full_images.npy (+ sample_ids.npy)")


if __name__ == "__main__":
    main()
