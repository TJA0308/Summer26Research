"""
Build condition-residual scalogram directories for End Milling, mirroring
Shoulder Milling's build_residual_scalograms.py: for each image, subtract the
mean of all images sharing the same nuisance condition, removing the
condition DC offset before classification.

Background: Shoulder Milling found its scalogram signal is dominated by the
machining condition (speed x depth-of-cut), not by feed rate -- ~10-45x
larger in magnitude -- and that condition-residual preprocessing (subtract
the per-condition mean) recovered feed from a ~42-54% honest leave-one-side-
out-CV ceiling to ~87.5%, and independently recovered roughness. This script
tests whether the same fix transfers to End Milling's raw-waveform-derived
scalograms, per residual_preprocessing_readme.md's comparison plan.

Grouping: End Milling's (DOC x Speed) condition is structurally identical to
Shoulder Milling's "side" -- confirmed against SPEED_LABELS/DOC_LABELS in
cnn_model/cnn_train.py: exactly 15 (DOC, speed) groups of 3 runs each, one
run per feed rate. feed_coarse and roughness (ra) share this nuisance
condition, same as Shoulder Milling's feed/roughness sharing "side". speed
and doc are NOT covered here, for the same reason Shoulder Milling's
finalized decision excluded them: cnn_model/README.md already reports both
near 100% run accuracy on raw features (model_speed.pt, model_doc.pt), so
there is nothing for residual correction to rescue.

Caveat, unlike Shoulder Milling (documented, not silently assumed away): each
(DOC, speed) condition's 3 runs don't always cover the SAME 3 feed classes
across conditions -- e.g. one condition's runs are feed classes {0,1,2}
(3-5 mm/rev), another's are {2,3,4} (5-7 mm/rev). Feed here is a 6-class
fine scale (3-8 mm/rev) that shifts with condition, not a fixed f3/f5/f7
alphabet present at every condition like Shoulder Milling. The per-condition
mean still removes the dominant condition signal, but doesn't cancel feed as
cleanly as Shoulder Milling's uniform-feed-set design -- worth checking
empirically rather than assuming an equally clean recovery.

Two source formats are auto-detected per --src_dirs entry:
  - Pipeline A (scalograms_10w): RGB PNGs, "run{N}_w{K}.png".
  - Pipeline D (scalograms_ses_10w): 4-channel float32 .npy arrays in [0,1],
    "run{N}_w{K}.npy" (see cnn_model/cnn_train_hilbert.py's NpyScalogramDataset
    -- it loads the .npy directly with no extra normalization, so residual
    output here is rescaled back to roughly [0,1] to match that expectation).
    The "_preview.png" files alongside each .npy are NOT regenerated -- they
    are cosmetic only (scalogram_hilbert.py, which built them, isn't present
    in this repo to replicate its exact rendering) and nothing in the
    training/eval pipeline reads them.

Usage:
    python build_residual_scalograms.py --target feed_coarse
    python build_residual_scalograms.py --target roughness
    python build_residual_scalograms.py --target feed_coarse --src_dirs scalograms_10w scalograms_ses_10w
"""
import argparse
import importlib.util
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).parent


def _load_cnn_train_module():
    spec = importlib.util.spec_from_file_location("cnn_train", ROOT / "cnn_model" / "cnn_train.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_run_to_condition(mod) -> dict:
    """(DOC, speed) pair per run -- the shared nuisance condition for feed_coarse/roughness."""
    return {run: (mod.DOC_LABELS[run], mod.SPEED_LABELS[run]) for run in mod.SPEED_LABELS}


def _group_and_subtract(items: dict, run_of: dict, run_to_condition: dict):
    """Shared grouping/residual math for both PNG and npy paths.

    items: {filename: ndarray}. Returns (group_mean_count, residual_stats_fn)
    where residual_stats_fn(fn) recomputes that file's residual on demand
    (avoids holding two full copies of every array in memory at once).
    """
    group_of = {fn: run_to_condition[run] for fn, run in run_of.items()}
    groups = {}
    for fn, key in group_of.items():
        groups.setdefault(key, []).append(fn)
    group_mean = {key: np.mean([items[fn] for fn in fns], axis=0) for key, fns in groups.items()}

    def residual_of(fn):
        return items[fn] - group_mean[group_of[fn]]

    return group_mean, residual_of


def build_residual_dir_png(src_dir: Path, out_dir: Path, run_to_condition: dict):
    print(f"\n{src_dir.name}  ->  {out_dir.name}/  [format=png]")
    out_dir.mkdir(exist_ok=True)

    pngs = [p for p in sorted(src_dir.glob("*.png")) if "_preview" not in p.stem]
    print(f"  Loading {len(pngs)} images ...")

    imgs, run_of = {}, {}
    for p in pngs:
        run = p.stem.split("_w")[0]
        if run not in run_to_condition:
            continue
        imgs[p.name] = np.asarray(Image.open(p).convert("RGB"), dtype=np.float32)
        run_of[p.name] = run

    if not imgs:
        print(f"  No images matched a known run -- skipping {src_dir.name}")
        return

    group_mean, residual_of = _group_and_subtract(imgs, run_of, run_to_condition)
    print(f"  {len(group_mean)} condition groups  ({len(imgs)//len(group_mean)} windows/group avg)")
    print(f"  Computing residuals and saving ...")

    # Stats computed incrementally, one image at a time -- these images are
    # much larger than Shoulder Milling's, so holding a second full-size
    # residual array per image (on top of imgs) risks running out of memory
    # just to get two scalars.
    n_pixels, total, total_sq = 0, 0.0, 0.0
    for fn in imgs:
        resid = residual_of(fn)
        total += resid.sum(dtype=np.float64)
        total_sq += np.square(resid, dtype=np.float64).sum()
        n_pixels += resid.size
    mu = total / n_pixels
    sd = np.sqrt(total_sq / n_pixels - mu ** 2)

    for fn in imgs:
        resid = residual_of(fn)
        resid_u8 = np.clip((resid - mu) / (sd * 2 + 1e-6) * 127.5 + 127.5, 0, 255).astype(np.uint8)
        Image.fromarray(resid_u8).save(out_dir / fn)

    print(f"  Saved {len(imgs)} residual PNGs  ->  {out_dir}/")


def build_residual_dir_npy(src_dir: Path, out_dir: Path, run_to_condition: dict):
    print(f"\n{src_dir.name}  ->  {out_dir.name}/  [format=npy, 4-channel]")
    out_dir.mkdir(exist_ok=True)

    npys = sorted(src_dir.glob("*.npy"))
    print(f"  Loading {len(npys)} arrays ...")

    arrs, run_of = {}, {}
    for p in npys:
        run = p.stem.split("_w")[0]
        if run not in run_to_condition:
            continue
        arrs[p.name] = np.load(p).astype(np.float32)  # (4, H, W), already [0,1]
        run_of[p.name] = run

    if not arrs:
        print(f"  No arrays matched a known run -- skipping {src_dir.name}")
        return

    group_mean, residual_of = _group_and_subtract(arrs, run_of, run_to_condition)
    print(f"  {len(group_mean)} condition groups  ({len(arrs)//len(group_mean)} windows/group avg)")
    print(f"  Computing residuals and saving ...")

    n_vals, total, total_sq = 0, 0.0, 0.0
    for fn in arrs:
        resid = residual_of(fn)
        total += resid.sum(dtype=np.float64)
        total_sq += np.square(resid, dtype=np.float64).sum()
        n_vals += resid.size
    mu = total / n_vals
    sd = np.sqrt(total_sq / n_vals - mu ** 2)

    # Rescale back to roughly [0,1] (centered at 0.5) so NpyScalogramDataset
    # -- which applies no further normalization -- sees a comparable dynamic
    # range to the original SES arrays, instead of a signed [-1,1]-ish residual.
    for fn in arrs:
        resid = residual_of(fn)
        resid_01 = np.clip((resid - mu) / (sd * 2 + 1e-6) * 0.5 + 0.5, 0.0, 1.0).astype(np.float32)
        np.save(out_dir / fn, resid_01)

    print(f"  Saved {len(arrs)} residual .npy arrays  ->  {out_dir}/")


def build_residual_dir(src_dir: Path, out_dir: Path, run_to_condition: dict):
    """Dispatch to the PNG or npy path based on what src_dir actually contains."""
    has_npy = any(src_dir.glob("*.npy"))
    has_png = any(p for p in src_dir.glob("*.png") if "_preview" not in p.stem)
    if has_npy:
        build_residual_dir_npy(src_dir, out_dir, run_to_condition)
    elif has_png:
        build_residual_dir_png(src_dir, out_dir, run_to_condition)
    else:
        print(f"\n{src_dir.name}: no .npy or .png files found -- skipping")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--target", required=True, choices=["feed_coarse", "roughness", "feed"])
    parser.add_argument("--src_dirs", nargs="+", default=["scalograms_10w", "scalograms_ses_10w"])
    args = parser.parse_args()

    mod = _load_cnn_train_module()
    run_to_condition = build_run_to_condition(mod)

    suffix = "_residual" if args.target == "feed_coarse" else f"_residual_{args.target}"


    for src_name in args.src_dirs:
        src_dir = ROOT / src_name
        if not src_dir.exists():
            print(f"skip {src_name}: not found")
            continue
        out_dir = ROOT / (src_name + suffix)
        build_residual_dir(src_dir, out_dir, run_to_condition)

    print("\nDone.")


if __name__ == "__main__":
    main()
