"""
Build condition-residual scalogram directories.

For each image, subtracts the mean of all windows that share the same
nuisance condition for the given target, removing the condition DC offset
so the classifier only sees target-relative signal.

Grouping logic per target:
  feed      -- group by side (= speed×doc). Within each side, feed varies
               over f3/f5/f7, so the per-side mean is the condition baseline.
  roughness -- same as feed (roughness co-varies with feed within a side).
  speed     -- group by (doc, feed). Within each (doc, feed) pair there are
               2 windows (s25 and s35), so the group mean is the non-speed
               baseline and the residual carries the speed contrast.
  doc       -- group by (speed, feed). Within each (speed, feed) pair there
               are 4 windows (4 doc levels), so the group mean is the
               non-doc baseline.

Note on test-time leakage: each residual image was normalized using the mean
of its group (which includes the image itself -- 1/N contribution). Accepted
as a minor simplification vs. per-fold recomputation inside cnn_train_param.

Usage:
    python build_residual_scalograms.py --target feed
    python build_residual_scalograms.py --target speed --src_dirs scalograms_32x3 scalograms_32x12
    python build_residual_scalograms.py --target doc   --src_dirs scalograms_32x3 scalograms_32x12
    python build_residual_scalograms.py --target roughness --src_dirs scalograms_32x3 scalograms_32x12
"""
import argparse
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from cnn_train_param import SIDE_TO_SPEED, SIDE_TO_DOC

ROOT = Path(__file__).parent


def group_key(row, target: str) -> tuple:
    """Return the nuisance-condition key for a given row and target."""
    side = int(row["side"])
    if target in ("feed", "roughness"):
        return (side,)                                          # per-side
    elif target == "speed":
        return (SIDE_TO_DOC[side], row["feed"])                # per-(doc, feed)
    elif target == "doc":
        return (SIDE_TO_SPEED[side], row["feed"])              # per-(speed, feed)
    else:
        raise ValueError(f"Unknown target: {target}")


def build_residual_dir(src_dir: Path, out_dir: Path, target: str):
    print(f"\n{src_dir.name}  ->  {out_dir.name}/  [target={target}]")
    out_dir.mkdir(exist_ok=True)

    df = pd.read_csv(src_dir / "labels.csv")

    print(f"  Loading {len(df)} images ...")
    imgs = {}
    for fn in df["filename"]:
        arr = np.asarray(Image.open(src_dir / fn).convert("L"), dtype=np.float32)
        imgs[fn] = arr

    # Compute per-group mean
    df["_group"] = df.apply(lambda r: group_key(r, target), axis=1)
    group_mean = {}
    for key, grp in df.groupby("_group"):
        group_mean[key] = np.mean([imgs[fn] for fn in grp["filename"]], axis=0)

    print(f"  {len(group_mean)} condition groups  ({len(df)//len(group_mean)} windows/group avg)")
    print(f"  Computing residuals and saving ...")

    residuals = []
    for _, row in df.iterrows():
        key = row["_group"]
        resid = imgs[row["filename"]] - group_mean[key]
        residuals.append(resid)

    residuals = np.stack(residuals)
    mu, sd = residuals.mean(), residuals.std()
    residuals_u8 = np.clip((residuals - mu) / (sd * 2 + 1e-6) * 127.5 + 127.5, 0, 255).astype(np.uint8)

    for i, (_, row) in enumerate(df.iterrows()):
        Image.fromarray(residuals_u8[i]).save(out_dir / row["filename"])

    shutil.copy(src_dir / "labels.csv", out_dir / "labels.csv")
    print(f"  Saved {len(df)} residual PNGs + labels.csv  ->  {out_dir}/")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--target", required=True, choices=["feed", "speed", "doc", "roughness"])
    parser.add_argument("--src_dirs", nargs="+",
                        default=["scalograms_32x3_feedopt", "scalograms_32x12_feedopt"])
    args = parser.parse_args()

    suffix = f"_residual_{args.target}" if args.target != "feed" else "_residual"

    for src_name in args.src_dirs:
        src_dir = ROOT / src_name
        out_dir = ROOT / (src_name + suffix)
        build_residual_dir(src_dir, out_dir, args.target)

    print("\nDone.")


if __name__ == "__main__":
    main()
