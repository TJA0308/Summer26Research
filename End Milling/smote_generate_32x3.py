"""
Generates and persists synthetic SMOTE training samples for End Milling's
precomputed-feature scalogram pipelines -- scalograms_32x3*/scalograms_32x12*
(base, _feedopt, _9win, and combinations) -- mirrors Shoulder Milling's
smote_generate_param.py, adapted to End Milling's whole-RUN synthesis
convention (a "sample" here is one dataset run, made of --n_windows window
images that all share one label, not a single window image in isolation).
Column-count-agnostic (reads it from the arrays themselves), so the same
script serves both the 3-column and 12-column pipelines with no flag needed.

Why whole-run, not per-window (unlike Shoulder Milling)
--------------------------------------------------------
cnn_model/cnn_train.py's SMOTE consumers (`load_smote_map`,
`load_smote_cond_map`, and the --mil / --conditioned / --multitask code
paths) all key synthetic samples by a synthetic RUN id and then glob
"{run}_w*.png" -- i.e. this repo's existing SMOTE convention for End Milling
scalograms already operates at the run level, not the window level. This
script follows that same convention exactly so its output is a drop-in
replacement for smote_labels.csv / smote_speed_labels.csv / etc. across ANY
scalogram directory (scalograms_10w, scalograms_32x3, ...) -- no changes to
cnn_model/cnn_train.py are required.

Method
------
For each target (speed, doc, feed_coarse, roughness) and each real TRAINING
run (test runs excluded per cnn_model/cnn_train.py's *_TEST_RUNS sets),
concatenate that run's n_windows row-block arrays from features_raw.npz
(sizes vary per window index -- e.g. [11,11,10] rows for 3 windows -- but
always sum to the full 32 rows, see build_32x3_features.py) into one
96-length (32*3) vector. Within each class, find each run's k-nearest
same-class neighbor (k = min(5, class_size-1)) and interpolate (gap ~
U(0,1)) to synthesize new whole runs up to the majority class's run count.
Each synthetic run's window images are the interpolated vector split back
into the same row-block sizes (`selected_scales.json`'s "block_sizes"),
re-quantized with the SAME normalisation constants the real images were
saved with (so synthetic pixels sit in the same dynamic range), and saved
as smote<target><i>_w{K}.png.

`smote_labels.csv` additionally carries `speed` and `doc` columns (inherited
from parent_a) alongside the fine-grained (6-class) feed label, because
cnn_model/cnn_train.py's load_smote_cond_map() (used by --conditioned /
--multitask cascade training) reads exactly that file and those columns.
feed_coarse's own smote_feed_coarse_labels.csv is a separate, coarse-label
(3-class) balance for the plain (non-cascade) training path.

Usage (from this directory, after running build_32x3_features.py):
    python smote_generate_32x3.py                                  # all targets, scalograms_32x3/
    python smote_generate_32x3.py --img_dir scalograms_32x3_feedopt
    python smote_generate_32x3.py --img_dir scalograms_32x3_9win
    python smote_generate_32x3.py --target roughness
"""
import argparse
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.neighbors import NearestNeighbors

SEED = 42
ROOT = Path(__file__).parent

TARGET_CSV = {
    "speed":       "smote_speed_labels.csv",
    "doc":         "smote_doc_labels.csv",
    "feed_coarse": "smote_feed_coarse_labels.csv",
    "roughness":   "smote_roughness_labels.csv",
    "feed":        "smote_labels.csv",   # fine-grained (6-class); also feeds cascade conditioning
}


def _load_cnn_train_module():
    spec = importlib.util.spec_from_file_location("cnn_train", ROOT / "cnn_model" / "cnn_train.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def label_map_and_test_runs(target: str, mod):
    if target == "speed":
        return mod.SPEED_LABELS, mod.SPEED_TEST_RUNS
    if target == "doc":
        return mod.DOC_LABELS, mod.DOC_TEST_RUNS
    if target == "feed_coarse":
        return mod.FEED_COARSE_LABELS, mod.FEED_COARSE_TEST_RUNS
    if target == "roughness":
        return mod.RA_LABELS, mod.RA_TEST_RUNS
    if target == "feed":
        return mod.FEED_LABELS, mod.FEED_TEST_RUNS
    raise ValueError(target)


def load_block_sizes(img_dir: Path) -> list:
    """Row-block sizes for this directory's n_windows (e.g. [11,11,10] for 3,
    [4,4,4,4,4,3,3,3,3] for 9) -- identical across every run, only the row
    COUNT per window index varies, so this must be read (not assumed 32)
    before reshaping any per-window array back to (rows_k, 3)."""
    with open(img_dir / "selected_scales.json") as f:
        return json.load(f)["block_sizes"]


def load_run_vectors(img_dir: Path, train_runs: set, n_windows: int):
    """Returns (vectors [n_runs, 32*3] float32, run_ids [n_runs] str) from
    features_raw.npz, restricted to train_runs, sorted for determinism.
    Each run's vector is its window blocks concatenated in order -- total
    length is always 32*3=96 regardless of how those 32 rows are divided
    into n_windows blocks, since the blocks are a partition of the same 32
    rows (see build_32x3_features.py)."""
    npz = np.load(img_dir / "features_raw.npz")
    runs = sorted(train_runs, key=lambda s: int(s[3:]))
    vecs = []
    for run in runs:
        window_arrs = [npz[f"{run}_w{k}"] for k in range(n_windows)]
        vecs.append(np.concatenate([w.reshape(-1) for w in window_arrs]))
    return np.stack(vecs).astype(np.float32), runs


def split_vector_into_windows(vec: np.ndarray, block_sizes: list, n_cols: int) -> list:
    """Inverse of load_run_vectors' concatenation: splits a flat
    (32*n_cols)-length vector back into its n_windows (rows_k, n_cols)
    blocks using the same row-block sizes every run shares."""
    windows = []
    offset = 0
    for size in block_sizes:
        n_vals = size * n_cols
        windows.append(vec[offset:offset + n_vals].reshape(size, n_cols))
        offset += n_vals
    return windows


def smote_balance_runs(vectors: np.ndarray, labels: np.ndarray, run_ids: list, rng):
    """Manual whole-run SMOTE: balances run counts per class up to the
    majority class. Returns (syn_vectors, syn_labels, parent_a, parent_b)."""
    counts = np.bincount(labels)
    present = counts[counts > 0]
    if len(present) < 2 or present.min() < 2:
        print("  [SMOTE] Skipped -- fewer than 2 classes, or a class has <2 runs")
        return [], [], [], []
    max_count = counts.max()
    k = min(5, int(present.min()) - 1)
    print(f"  [SMOTE] Before (runs): {dict(enumerate(counts.tolist()))}  (k_neighbors={k})")

    syn_vecs, syn_labels, parent_a, parent_b = [], [], [], []
    for cls in range(len(counts)):
        n_needed = int(max_count) - int(counts[cls])
        if n_needed <= 0:
            continue
        idx = np.where(labels == cls)[0]
        X_cls = vectors[idx]
        ids_cls = [run_ids[i] for i in idx]
        k_cls = min(k, len(idx) - 1)

        if k_cls < 1:
            for _ in range(n_needed):
                syn_vecs.append(X_cls[0].copy())
                syn_labels.append(cls)
                parent_a.append(ids_cls[0]); parent_b.append(ids_cls[0])
            continue

        nn_model = NearestNeighbors(n_neighbors=k_cls + 1).fit(X_cls)
        _, nbr_idx = nn_model.kneighbors(X_cls)

        for _ in range(n_needed):
            base = rng.integers(0, len(idx))
            nbr = rng.choice(nbr_idx[base][1:])
            gap = rng.random()
            vec = X_cls[base] + gap * (X_cls[nbr] - X_cls[base])
            syn_vecs.append(vec)
            syn_labels.append(cls)
            parent_a.append(ids_cls[base]); parent_b.append(ids_cls[nbr])

    counts_after = counts.copy()
    for lbl in syn_labels:
        counts_after[lbl] += 1
    print(f"  [SMOTE] After (runs):  {dict(enumerate(counts_after.tolist()))}  (+{len(syn_vecs)} synthetic runs)")
    return syn_vecs, syn_labels, parent_a, parent_b


def quantize_like_real(raw_window: np.ndarray, mu: np.ndarray, sig: np.ndarray) -> np.ndarray:
    """Re-applies the exact z-score -> [0,255] mapping build_32x3_features.py
    used for the real images, so synthetic pixels share the real dynamic range."""
    norm = (raw_window - mu) / sig
    return np.clip((norm + 3) / 6 * 255, 0, 255).astype(np.uint8)


def generate_for(img_dir: Path, target: str, n_windows: int, mod, rng):
    print(f"\n=== {img_dir.name} / {target} ===")
    label_map, test_runs = label_map_and_test_runs(target, mod)
    train_runs = set(label_map.keys()) - set(test_runs)

    block_sizes = load_block_sizes(img_dir)
    vectors, run_ids = load_run_vectors(img_dir, train_runs, n_windows)
    labels = np.array([label_map[r] for r in run_ids], dtype=int)

    syn_vecs, syn_labels, parent_a, parent_b = smote_balance_runs(vectors, labels, run_ids, rng)

    # Re-derive the same column-wise normalisation constants used when the
    # real PNGs were quantized, so synthetic images are saved consistently.
    all_windows = np.load(img_dir / "features_raw.npz")
    n_cols = all_windows[all_windows.files[0]].shape[-1]
    all_flat = np.concatenate([all_windows[k].reshape(-1, n_cols) for k in all_windows.files])
    mu, sig = all_flat.mean(axis=0), all_flat.std(axis=0)
    sig[sig < 1e-10] = 1.0

    rows = []
    speed_map = mod.SPEED_LABELS
    doc_map = mod.DOC_LABELS
    for i, (vec, lbl, pa, pb) in enumerate(zip(syn_vecs, syn_labels, parent_a, parent_b)):
        synth_run = f"smote{target}{i:03d}"
        windows = split_vector_into_windows(vec, block_sizes, n_cols)
        for k in range(n_windows):
            img_u8 = quantize_like_real(windows[k], mu, sig)
            Image.fromarray(img_u8).save(img_dir / f"{synth_run}_w{k}.png")
        rows.append({
            "run": synth_run, "label": lbl,
            "speed": speed_map[pa], "doc": doc_map[pa],
            "parent_a": pa, "parent_b": pb,
        })

    out_csv = img_dir / TARGET_CSV[target]
    pd.DataFrame(rows, columns=["run", "label", "speed", "doc", "parent_a", "parent_b"]).to_csv(
        out_csv, index=False)
    print(f"  Saved {len(rows)} synthetic runs ({len(rows) * n_windows} window images) -> {out_csv}")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--target", default=None, choices=list(TARGET_CSV.keys()),
                        help="Limit to one target (default: all five)")
    parser.add_argument("--img_dir", default="scalograms_32x3",
                        help="scalograms_32x3, scalograms_32x3_feedopt, scalograms_32x3_9win, "
                             "or scalograms_32x3_feedopt_9win (relative to this script)")
    parser.add_argument("--n_windows", type=int, default=None,
                        help="Windows per run in --img_dir. Auto-detected from "
                             "selected_scales.json if omitted.")
    args = parser.parse_args()

    img_dir = ROOT / args.img_dir
    if not img_dir.exists():
        raise FileNotFoundError(f"{img_dir} not found -- run build_32x3_features.py first")

    n_windows = args.n_windows
    if n_windows is None:
        import json
        with open(img_dir / "selected_scales.json") as f:
            n_windows = json.load(f)["n_windows"]

    mod = _load_cnn_train_module()
    targets = [args.target] if args.target else list(TARGET_CSV.keys())

    rng = np.random.default_rng(SEED)
    for target in targets:
        generate_for(img_dir, target, n_windows, mod, rng)

    print("\nDone.")


if __name__ == "__main__":
    main()
