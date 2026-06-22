"""
Splits each existing scalogram window image into 3 row-blocks along the
32-scale-row axis, tripling the sample count per run: 3 windows/run -> 9
sub-windows/run.

This is a POST-GENERATION split of the already-built (32, C) scalogram
PNGs, not a re-derivation from raw signal -- the upstream data/Side*.xlsx
sheets only contain pre-computed per-window CWT/FFT/DWT feature vectors
(65x12, no raw waveform), so there is nothing to re-window in time. Each
of the 32 scale rows already corresponds to one CWT/wavelet scale; cutting
that axis into three contiguous scale-bands turns one window into three
narrower-bandwidth samples that still share the parent window's label.

Reads any of the 4 existing scalogram dirs (scalograms_32x12,
scalograms_32x3, scalograms_32x12_feedopt, scalograms_32x3_feedopt) and
writes a sibling "<dir>_9win" directory with the same labels.csv schema
(filename, sample_id, run, window, side, feed, ra, ra_class). Windows are
relabelled w1..w9 per run, in parent-window order (original w1 -> w1-w3,
w2 -> w4-w6, w3 -> w7-w9), so existing run-level majority-vote grouping
(by the numeric "run" column) and per-run reporting work unmodified.

Usage:
    python split_scalogram_windows.py
    python split_scalogram_windows.py --dirs scalograms_32x12 scalograms_32x12_feedopt
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

ROOT = Path(__file__).parent

DEFAULT_DIRS = [
    "scalograms_32x12", "scalograms_32x3",
    "scalograms_32x12_feedopt", "scalograms_32x3_feedopt",
]


def split_one(img_dir: Path, out_dir: Path):
    df = pd.read_csv(img_dir / "labels.csv")
    out_dir.mkdir(exist_ok=True)

    rows = []
    for _, row in df.iterrows():
        img = np.array(Image.open(img_dir / row["filename"]))
        orig_win_num = int(str(row["window"])[1:])  # "w1" -> 1
        blocks = np.array_split(img, 3, axis=0)
        for sub_i, block in enumerate(blocks, start=1):
            new_win_num = (orig_win_num - 1) * 3 + sub_i
            stem  = Path(row["filename"]).stem
            fname = f"{stem}_{sub_i}.png"
            Image.fromarray(block).save(out_dir / fname)
            rows.append({
                "filename":  fname,
                "sample_id": f"{row['sample_id']}_{sub_i}",
                "run":       row["run"],
                "window":    f"w{new_win_num}",
                "side":      row["side"],
                "feed":      row["feed"],
                "ra":        row["ra"],
                "ra_class":  row["ra_class"],
            })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(out_dir / "labels.csv", index=False)
    print(f"  {img_dir.name}: {len(df)} windows -> {len(out_df)} sub-windows  ({out_dir.name}/)")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dirs", nargs="+", default=DEFAULT_DIRS)
    args = parser.parse_args()

    for dir_name in args.dirs:
        img_dir = ROOT / dir_name
        if not img_dir.exists():
            print(f"  skip {dir_name}: not found")
            continue
        out_dir = ROOT / f"{dir_name}_9win"
        split_one(img_dir, out_dir)


if __name__ == "__main__":
    main()
