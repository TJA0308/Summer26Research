"""
Generates and persists synthetic SMOTE training samples for the Shoulder
Milling parameter models (speed/feed/doc), instead of generating them
in-memory at training time (mirrors End Milling's smote_std.py-style
persisted files, so the synthetic samples can be inspected and aren't
regenerated from scratch on every one of the 8 arch x LR training runs).

For each target x scalogram pipeline, balances the training-split window
classes up to the majority class count by interpolating a real sample with
one of its k-nearest same-class neighbors (a manual SMOTE re-implementation
so the two parent sample_ids can be tracked -- imblearn's fit_resample()
does not expose this). Synthetic images are saved as grayscale PNGs at the
same native resolution as the real scalograms (32x12 or 32x3), named
smote_<target>_<class>_<i>.png, alongside a smote_<target>_labels.csv
(filename,label,parent_a,parent_b) in the same scalogram directory.
cnn_train_param.py loads these via load_smote_samples().

Usage (from this directory):
    python smote_generate_param.py                            # all 3 targets x both pipelines
    python smote_generate_param.py --target feed              # one target, both pipelines
    python smote_generate_param.py --img_dir scalograms_32x12  # one pipeline, all targets
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.neighbors import NearestNeighbors

from cnn_train_param import TARGETS, EXP_SPLITS, COND_FROM_SIDE_FEED, label_for

SEED = 42
HERE = Path(__file__).parent


def load_train_samples(img_dir: Path, target: str, split_id: str = ""):
    """Returns (vectors [n, H*W] float32, labels [n] int, sample_ids [n] str, img_h, img_w)."""
    df = pd.read_csv(img_dir / "labels.csv")
    df["run_id"] = df.apply(lambda r: COND_FROM_SIDE_FEED[(int(r["side"]), r["feed"])], axis=1)
    df["label"] = df.apply(lambda r: label_for(target, r["side"], r["feed"], r.get("ra")), axis=1)

    if split_id in EXP_SPLITS:
        test_runs  = EXP_SPLITS[split_id]["test_runs"]
        train_runs = [r for r in df["run_id"].unique() if r not in test_runs]
    else:
        train_runs = TARGETS[target]["train_runs"]
    train_df   = df[df["run_id"].isin(train_runs)].reset_index(drop=True)

    vectors, labels, sample_ids = [], [], []
    img_h = img_w = None
    for _, row in train_df.iterrows():
        img = Image.open(img_dir / row.filename).convert("L")
        if img_h is None:
            img_w, img_h = img.size
        elif img.size != (img_w, img_h):
            img = img.resize((img_w, img_h), Image.LANCZOS)
        vectors.append(np.asarray(img, dtype=np.float32).flatten())
        labels.append(int(row.label))
        sample_ids.append(row.sample_id)

    return np.stack(vectors), np.array(labels, dtype=int), sample_ids, img_h, img_w


def smote_balance(vectors, labels, sample_ids, rng):
    """
    Manual SMOTE: for each minority class, generate enough synthetic samples
    to match the majority class count by interpolating a random base sample
    with one of its k-nearest same-class neighbors. Returns
    (synthetic_vectors, synthetic_labels, parent_a_ids, parent_b_ids).
    """
    counts    = np.bincount(labels)
    min_count = counts[counts > 0].min()
    max_count = counts.max()
    if min_count < 2:
        print("  [SMOTE] Skipped -- a class has fewer than 2 samples")
        return [], [], [], []
    k = min(5, int(min_count) - 1)
    print(f"  [SMOTE] Before: {dict(enumerate(counts.tolist()))}  (k_neighbors={k})")

    syn_vecs, syn_labels, parent_a, parent_b = [], [], [], []
    for cls in range(len(counts)):
        n_needed = int(max_count) - int(counts[cls])
        if n_needed <= 0:
            continue
        idx       = np.where(labels == cls)[0]
        X_class   = vectors[idx]
        ids_class = [sample_ids[i] for i in idx]
        k_cls     = min(k, len(idx) - 1)

        if k_cls < 1:
            # Only one real sample in this class -- no interpolation partner available.
            for _ in range(n_needed):
                syn_vecs.append(X_class[0].copy())
                syn_labels.append(cls)
                parent_a.append(ids_class[0])
                parent_b.append(ids_class[0])
            continue

        nn_model   = NearestNeighbors(n_neighbors=k_cls + 1).fit(X_class)
        _, nbr_idx = nn_model.kneighbors(X_class)

        for _ in range(n_needed):
            base = rng.integers(0, len(idx))
            nbr  = rng.choice(nbr_idx[base][1:])   # exclude self (distance 0)
            gap  = rng.random()
            vec  = X_class[base] + gap * (X_class[nbr] - X_class[base])
            syn_vecs.append(vec)
            syn_labels.append(cls)
            parent_a.append(ids_class[base])
            parent_b.append(ids_class[nbr])

    counts_after = counts.copy()
    for lbl in syn_labels:
        counts_after[lbl] += 1
    print(f"  [SMOTE] After:  {dict(enumerate(counts_after.tolist()))}  (+{len(syn_vecs)} synthetic)")
    return syn_vecs, syn_labels, parent_a, parent_b


def generate_for(img_dir: Path, target: str, rng, split_id: str = ""):
    label = f"{img_dir.name} / {target}" + (f" / {split_id}" if split_id else "")
    print(f"\n=== {label} ===")
    vectors, labels, sample_ids, img_h, img_w = load_train_samples(img_dir, target, split_id)
    syn_vecs, syn_labels, parent_a, parent_b = smote_balance(vectors, labels, sample_ids, rng)

    suffix = f"_{split_id}" if split_id else ""
    rows = []
    for i, (vec, lbl, pa, pb) in enumerate(zip(syn_vecs, syn_labels, parent_a, parent_b)):
        arr      = np.clip(vec, 0, 255).reshape(img_h, img_w).astype(np.uint8)
        filename = f"smote_{target}{suffix}_{lbl}_{i:03d}.png"
        Image.fromarray(arr).save(img_dir / filename)
        rows.append({"filename": filename, "label": lbl, "parent_a": pa, "parent_b": pb})

    out_csv = img_dir / f"smote_{target}{suffix}_labels.csv"
    pd.DataFrame(rows, columns=["filename", "label", "parent_a", "parent_b"]).to_csv(out_csv, index=False)
    print(f"  Saved {len(rows)} synthetic images + labels -> {out_csv}")


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--target",   default=None, choices=list(TARGETS.keys()),
                        help="Limit to one target (default: all four)")
    parser.add_argument("--img_dir",  default=None,
                        help="Limit to one scalogram dir, e.g. scalograms_32x12 (default: both)")
    parser.add_argument("--split_id", default="", choices=["", "exp11", "exp12"],
                        help="Experimental unified split (see experimental_splits.md). "
                             "Outputs smote_<target>_<split_id>_labels.csv when set.")
    args = parser.parse_args()

    targets  = [args.target] if args.target else list(TARGETS.keys())
    img_dirs = [HERE / args.img_dir] if args.img_dir else [HERE / "scalograms_32x12", HERE / "scalograms_32x3"]

    rng = np.random.default_rng(SEED)
    for img_dir in img_dirs:
        for target in targets:
            generate_for(img_dir, target, rng, args.split_id)

    print("\nDone.")


if __name__ == "__main__":
    main()
