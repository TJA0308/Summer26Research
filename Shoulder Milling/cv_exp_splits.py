"""
Feed classification on exp11/exp12 fixed splits using two approaches that
go beyond the raw-pixel HGB/tiny_cnn baseline:

  Approach 1 -- Conditioned HGB:
    StandardScaler + PCA(20) + HGB, BUT the feature vector is augmented with
    the TRUE speed and doc class labels (one-hot encoded) concatenated after
    the PCA components. This tests the ceiling for cascade conditioning --
    if perfect upstream predictions can't help, cascade is a dead end.

  Approach 2 -- Condition-invariant features:
    Instead of raw pixels, compute features that are designed to be stable
    across speed/doc conditions:
      a) Row-wise rank within each image (ordinal position of each CWT scale
         relative to others -- removes global amplitude shifts between conditions)
      b) Row-ratio features: each row divided by the column mean (removes
         condition-driven DC offsets)
      c) Within-image z-score (zero mean, unit std per image -- normalises
         the amplitude envelope that shifts with doc/speed)
    Then PCA(20) + HGB on these condition-normalised features.

Both approaches are evaluated on exp11 and exp12, for the two feedopt
scalogram dirs (32x3 and 32x12). Results are written to cv_exp_splits_summary.csv.

Usage:
    python cv_exp_splits.py
    python cv_exp_splits.py --img_dirs scalograms_32x3_feedopt scalograms_32x12_feedopt
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from cnn_train_param import (
    EXP_SPLITS, FEED_TO_CLASS, COND_FROM_SIDE_FEED,
    SIDE_TO_SPEED, SIDE_TO_DOC, TARGETS,
)

ROOT = Path(__file__).parent
RUN_TO_SIDE = {v: k[0] for k, v in COND_FROM_SIDE_FEED.items()}

N_SPEED = TARGETS["speed"]["num_classes"]   # 2
N_DOC   = TARGETS["doc"]["num_classes"]     # 4


# ── feature extractors ──────────────────────────────────────────────────────────

def load_pixels(paths):
    """Raw flattened grayscale pixels (float32)."""
    return np.stack([
        np.asarray(Image.open(p).convert("L"), dtype=np.float32).ravel()
        for p in paths
    ])


def condition_invariant_features(paths):
    """
    Per-image normalised features designed to be stable across speed/doc
    conditions. Each image is treated independently (no cross-image stats).
    Three feature blocks concatenated:
      1. Within-image z-score of flattened pixels (removes global amplitude)
      2. Row-wise rank / (n_rows-1) reshaped flat (removes inter-row ordering)
      3. Pixel / (col_mean + 1e-6) flattened (removes column-level DC offset)
    """
    feats = []
    for p in paths:
        arr = np.asarray(Image.open(p).convert("L"), dtype=np.float32)  # (H, W)
        flat = arr.ravel()

        # block 1: within-image z-score
        mu, sd = flat.mean(), flat.std()
        zscore = (flat - mu) / (sd + 1e-6)

        # block 2: row-wise rank (each row independently)
        from scipy.stats import rankdata
        ranked = np.stack([rankdata(row) / max(len(row), 1) for row in arr]).ravel()

        # block 3: divide each pixel by its column mean
        col_mean = arr.mean(axis=0, keepdims=True)  # (1, W)
        ratio = (arr / (col_mean + 1e-6)).ravel()

        feats.append(np.concatenate([zscore, ranked, ratio]))
    return np.stack(feats)


def onehot(label, n):
    v = np.zeros(n, dtype=np.float32)
    v[label] = 1.0
    return v


# ── HGB runner ──────────────────────────────────────────────────────────────────

def run_hgb(Xtr, ytr, Xte, seed, n_pca=20):
    n_components = min(n_pca, Xtr.shape[0] - 1, Xtr.shape[1])
    pipe = Pipeline([
        ("scale", StandardScaler()),
        ("pca",   PCA(n_components=n_components, random_state=seed)),
        ("clf",   HistGradientBoostingClassifier(max_iter=200, random_state=seed)),
    ])
    pipe.fit(Xtr, ytr)
    return pipe.predict_proba(Xte)


# ── run-level vote ───────────────────────────────────────────────────────────────

def run_vote(probs, labels, run_ids):
    run_probs, run_true = {}, {}
    for prob, true, run in zip(probs, labels, run_ids):
        run_probs.setdefault(run, []).append(prob)
        run_true[run] = true

    soft_correct, hard_correct = 0, 0
    details = []
    for run in sorted(run_true):
        soft_pred = int(np.argmax(np.mean(run_probs[run], axis=0)))
        votes     = [int(p.argmax()) for p in run_probs[run]]
        hard_pred = max(set(votes), key=votes.count)
        true      = run_true[run]
        soft_correct += int(soft_pred == true)
        hard_correct += int(hard_pred == true)
        details.append((run, true, hard_pred, soft_pred))

    n = len(run_true)
    return hard_correct / n, soft_correct / n, details


# ── main evaluation ──────────────────────────────────────────────────────────────

def evaluate_split(img_dir: Path, split_id: str, approach: str, seed: int):
    df = pd.read_csv(img_dir / "labels.csv")
    df["label"]  = df["feed"].map(FEED_TO_CLASS)
    df["run_id"] = df.apply(
        lambda r: COND_FROM_SIDE_FEED[(int(r["side"]), r["feed"])], axis=1
    )

    test_runs  = set(EXP_SPLITS[split_id]["test_runs"])
    test_df    = df[df["run_id"].isin(test_runs)].reset_index(drop=True)
    train_df   = df[~df["run_id"].isin(test_runs)].reset_index(drop=True)

    train_paths = [img_dir / fn for fn in train_df["filename"]]
    test_paths  = [img_dir / fn for fn in test_df["filename"]]
    train_labels = train_df["label"].to_numpy()
    test_labels  = test_df["label"].to_numpy()
    test_run_ids = test_df["run_id"].tolist()

    if approach == "conditioned_hgb":
        # Raw pixels + one-hot speed + one-hot doc
        Xtr_px = load_pixels(train_paths)
        Xte_px = load_pixels(test_paths)

        # True speed/doc for training windows
        tr_speed = np.stack([onehot(SIDE_TO_SPEED[int(r.side)], N_SPEED) for r in train_df.itertuples()])
        tr_doc   = np.stack([onehot(SIDE_TO_DOC[int(r.side)],   N_DOC)   for r in train_df.itertuples()])
        te_speed = np.stack([onehot(SIDE_TO_SPEED[int(r.side)], N_SPEED) for r in test_df.itertuples()])
        te_doc   = np.stack([onehot(SIDE_TO_DOC[int(r.side)],   N_DOC)   for r in test_df.itertuples()])

        # PCA on pixels only, then concatenate condition one-hots
        n_pca = min(20, Xtr_px.shape[0] - 1, Xtr_px.shape[1])
        scaler = StandardScaler()
        Xtr_sc = scaler.fit_transform(Xtr_px)
        Xte_sc = scaler.transform(Xte_px)
        pca = PCA(n_components=n_pca, random_state=seed)
        Xtr_pca = pca.fit_transform(Xtr_sc)
        Xte_pca = pca.transform(Xte_sc)

        Xtr = np.concatenate([Xtr_pca, tr_speed, tr_doc], axis=1)
        Xte = np.concatenate([Xte_pca, te_speed, te_doc], axis=1)

        from sklearn.ensemble import HistGradientBoostingClassifier
        clf = HistGradientBoostingClassifier(max_iter=200, random_state=seed)
        clf.fit(Xtr, train_labels)
        probs = clf.predict_proba(Xte)

    elif approach == "invariant_features":
        Xtr = condition_invariant_features(train_paths)
        Xte = condition_invariant_features(test_paths)
        probs = run_hgb(Xtr, train_labels, Xte, seed)

    else:
        raise ValueError(approach)

    run_hard, run_soft, details = run_vote(probs, test_labels, test_run_ids)

    feed_map = {0: "f3", 1: "f5", 2: "f7"}
    print(f"    {approach:<20s} split={split_id} seed={seed}  "
          f"run_hard={run_hard:.3f}  run_soft={run_soft:.3f}")
    print("      " + "  ".join(
        f"{r.split('f')[0]}+{r.split('f')[1][2:]}:"
        f"true={feed_map[t]} hard={feed_map[h]} soft={feed_map[s]}"
        for r, t, h, s in details
    ))
    return run_hard, run_soft


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--img_dirs", nargs="+",
                        default=["scalograms_32x3_feedopt", "scalograms_32x12_feedopt"])
    parser.add_argument("--splits",   nargs="+", default=["exp11", "exp12"])
    parser.add_argument("--seeds",    nargs="+", type=int, default=[42, 43, 44])
    args = parser.parse_args()

    approaches = ["conditioned_hgb", "invariant_features"]
    rows = []

    for img_dir_name in args.img_dirs:
        img_dir = ROOT / img_dir_name
        scalo_tag = img_dir_name.replace("scalograms_", "")
        print(f"\n=== {img_dir_name} ===")
        for split_id in args.splits:
            print(f"  -- {split_id} --")
            for approach in approaches:
                for seed in args.seeds:
                    run_hard, run_soft = evaluate_split(img_dir, split_id, approach, seed)
                    rows.append({
                        "scalogram": scalo_tag, "split": split_id,
                        "approach": approach, "seed": seed,
                        "run_acc_hard": round(run_hard, 4),
                        "run_acc_soft": round(run_soft, 4),
                    })

    out = pd.DataFrame(rows)
    out_path = ROOT / "cv_exp_splits_summary.csv"
    if out_path.exists():
        out = pd.concat([pd.read_csv(out_path), out], ignore_index=True)
    out.to_csv(out_path, index=False)
    print(f"\nWrote {len(rows)} rows -> {out_path.name}")

    print("\n--- Mean +/- std across seeds ---")
    for (scalo, split, approach), g in out.groupby(["scalogram", "split", "approach"]):
        print(f"  {scalo:<22s} {split:<6s} {approach:<22s} n={len(g)}  "
              f"run_hard={g['run_acc_hard'].mean():.3f}+/-{g['run_acc_hard'].std():.3f}  "
              f"run_soft={g['run_acc_soft'].mean():.3f}+/-{g['run_acc_soft'].std():.3f}")


if __name__ == "__main__":
    main()
