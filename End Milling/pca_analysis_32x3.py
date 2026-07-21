"""
PCA analysis of End Milling's precomputed-feature scalogram matrices --
mirrors Shoulder Milling's pca_analysis.py. Works for either pipeline: pass
--img_dir pointing at a scalograms_32x3* (FFT/mexican/coif, 3 columns) or
scalograms_32x12* (all 12 feature columns) directory -- the column names and
count are read from that directory's selected_scales.json, not hardcoded.

Difference from Shoulder Milling's version
--------------------------------------------
Shoulder Milling's PCA ran on the PRE-selection 64x12 image (all 64 raw CWT
scale rows, all 12 feature columns) specifically to help decide which 32-of-
64 rows to keep (see Shoulder Milling/scalogram_readme.md Section 4) -- scale
selection happened AFTER that PCA, and it distinguished "window-level" (72
samples) from "run-level" (24 runs, averaged) because Shoulder Milling's
windows were real independent measurements.

Here, scale selection already happened inside build_32x3_features.py (top-32-
of-64 by Spearman |rho|, same method), and there is only one real sample per
run -- the "windows" build_32x3_features.py writes for CNN training are row-
fragments of that single run-level image (see its docstring), not
independent measurements. So this script has no separate window-level vs
run-level PCA to run: it loads `run_features_raw.npz` (one full, pre-
quantization (32, 3) float array per run -- NOT `features_raw.npz`, which
holds the fragmented per-window blocks used for SMOTE/training) and runs a
single PCA over the 45 runs.

Usage:
    python pca_analysis_32x3.py --img_dir scalograms_32x3 --target roughness
    python pca_analysis_32x3.py --img_dir scalograms_32x3_feedopt --target feed_coarse
    python pca_analysis_32x3.py --img_dir scalograms_32x3_speedopt --target speed
    python pca_analysis_32x3.py --img_dir scalograms_32x3_docopt --target doc
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from em_feature_common import load_cnn_train_module

ROOT = Path(__file__).parent
N_ROWS = 32


def load_feature_cols(img_dir: Path) -> list:
    """Reads the column names/count this directory's builder actually used
    (["FFT","Mexican","Coiflet"] for scalograms_32x3*, the full 12-name list
    for scalograms_32x12*) from selected_scales.json -- written by
    build_32x3_features.py / build_32x12_features.py via em_feature_common
    .write_dataset()."""
    with open(img_dir / "selected_scales.json") as f:
        return json.load(f)["feature_cols"]


def load_dataset(img_dir: Path, n_cols: int):
    """Returns (X [45, 32*n_cols] float, per_run DataFrame indexed by run,
    one row each -- since every window of a run shares the same run-level
    labels)."""
    df = pd.read_csv(img_dir / "labels.csv")
    per_run = df.drop_duplicates(subset="run").set_index("run").sort_index(
        key=lambda idx: idx.map(lambda r: int(r[3:])))
    npz = np.load(img_dir / "run_features_raw.npz")
    runs = list(per_run.index)
    X = np.stack([npz[r] for r in runs]).reshape(len(runs), -1)   # (45, 32*n_cols)
    return X, runs, per_run


def class_names_for(target: str, row: pd.Series, mod) -> str:
    if target == "roughness":
        return row["ra_class"]
    if target == "feed_coarse":
        return {0: "Low (3-4)", 1: "Med (5-6)", 2: "High (7-8)"}[row["feed_coarse"]]
    if target == "speed":
        return mod.SPEED_NAMES[row["speed"]]
    if target == "doc":
        return mod.DOC_NAMES[row["doc"]]
    raise ValueError(target)


def continuous_value(target: str, per_run: pd.DataFrame, mod) -> np.ndarray:
    if target == "roughness":
        return per_run["ra"].to_numpy()
    if target == "feed_coarse":
        return (per_run["feed"].to_numpy() + 3)   # FEED_LABELS 0..5 -> mm/rev 3..8
    if target == "speed":
        return np.array([int(mod.SPEED_NAMES[c].split()[0]) for c in per_run["speed"]])
    if target == "doc":
        return np.array([float(mod.DOC_NAMES[c].split()[0]) for c in per_run["doc"]])
    raise ValueError(target)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                      description=__doc__)
    parser.add_argument("--img_dir", default="scalograms_32x3",
                        help="scalograms_32x3, scalograms_32x3_feedopt, or a _9win variant "
                             "(run_features_raw.npz is identical for a base dir and its "
                             "_9win sibling -- only the window split differs -- so either works)")
    parser.add_argument("--target", default="roughness",
                        choices=["roughness", "feed_coarse", "speed", "doc"],
                        help="Which target to color/correlate PCs against")
    args = parser.parse_args()

    img_dir = ROOT / args.img_dir
    out_dir = ROOT / f"pca_plots_{img_dir.name}"
    out_dir.mkdir(exist_ok=True)

    mod = load_cnn_train_module()
    feature_cols = load_feature_cols(img_dir)
    print(f"Loading {img_dir.name} ...")
    X, runs, per_run = load_dataset(img_dir, len(feature_cols))
    target_val = continuous_value(args.target, per_run, mod)
    classes = np.array([class_names_for(args.target, per_run.loc[r], mod) for r in runs])
    print(f"  Loaded {X.shape[0]} runs, {X.shape[1]}-dim feature vector each "
          f"({N_ROWS} rows x {len(feature_cols)} cols)")
    print(f"  Target ({args.target}) range: {target_val.min():.3f} - {target_val.max():.3f}  "
          f"mean={target_val.mean():.3f}")

    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)

    pca = PCA(n_components=min(X.shape[0], X_sc.shape[1]))
    pca.fit(X_sc)
    Z = pca.transform(X_sc)

    ev = pca.explained_variance_ratio_
    cev = np.cumsum(ev)

    # ═══ Plot 1 — explained variance ═══════════════════════════════════════
    n_show = min(20, len(ev))
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(range(1, n_show + 1), ev[:n_show] * 100, color="steelblue", alpha=0.8, label="Individual")
    ax2 = ax.twinx()
    ax2.plot(range(1, n_show + 1), cev[:n_show] * 100, "o-", color="darkorange", label="Cumulative")
    ax2.axhline(90, color="gray", linestyle="--", linewidth=0.8)
    ax2.set_ylabel("Cumulative variance (%)", color="darkorange")
    ax.set_xlabel("Principal component")
    ax.set_ylabel("Individual variance (%)", color="steelblue")
    n90 = int(np.searchsorted(cev, 0.90)) + 1
    ax.set_title(f"PCA explained variance — {n90} PCs reach 90%  ({img_dir.name}, target={args.target})")
    l1, lb1 = ax.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax.legend(l1 + l2, lb1 + lb2, loc="center right")
    fig.tight_layout()
    fig.savefig(out_dir / "1_explained_variance.png", dpi=150)
    plt.close(fig)
    print(f"  PCs to reach 90% variance: {n90}")

    # ═══ Plot 2 — PC1 vs PC2 by class ═══════════════════════════════════════
    fig, ax = plt.subplots(figsize=(8, 6))
    palette = ["steelblue", "darkorange", "crimson", "forestgreen"]
    markers = ["o", "s", "^", "D"]
    for i, cls in enumerate(sorted(set(classes))):
        mask = classes == cls
        ax.scatter(Z[mask, 0], Z[mask, 1], c=palette[i % 4], marker=markers[i % 4],
                   label=cls, alpha=0.7, edgecolors="k", linewidths=0.4)
    ax.set_xlabel(f"PC1 ({ev[0] * 100:.1f}%)")
    ax.set_ylabel(f"PC2 ({ev[1] * 100:.1f}%)")
    ax.set_title(f"PC1 vs PC2 — all {len(runs)} runs coloured by {args.target} class")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_dir / "2_pc1_pc2_class.png", dpi=150)
    plt.close(fig)

    # ═══ Plot 3 — PC1 vs PC2, continuous target, run numbers annotated ═════
    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(Z[:, 0], Z[:, 1], c=target_val, cmap="plasma",
                     s=80, edgecolors="k", linewidths=0.5)
    plt.colorbar(sc, ax=ax, label=args.target)
    for i, r in enumerate(runs):
        ax.annotate(r.replace("run", ""), (Z[i, 0], Z[i, 1]),
                    fontsize=7, textcoords="offset points", xytext=(4, 3))
    ax.set_xlabel(f"PC1 ({ev[0] * 100:.1f}%)")
    ax.set_ylabel(f"PC2 ({ev[1] * 100:.1f}%)")
    ax.set_title(f"PC1 vs PC2 — coloured by {args.target}")
    fig.tight_layout()
    fig.savefig(out_dir / "3_pc1_pc2_continuous.png", dpi=150)
    plt.close(fig)

    # ═══ Plot 4 — loading heatmaps PC1-4, reshaped (32, n_cols) ════════════
    n_pcs = 4
    fig, axes = plt.subplots(1, n_pcs, figsize=(4 * n_pcs, 6))
    for pc_idx, ax in enumerate(axes):
        loading = pca.components_[pc_idx].reshape(N_ROWS, len(feature_cols))
        vmax = np.abs(loading).max()
        im = ax.imshow(loading, aspect="auto", cmap="RdBu_r", vmin=-vmax, vmax=vmax, origin="upper")
        ax.set_title(f"PC{pc_idx + 1} ({ev[pc_idx] * 100:.1f}%)")
        ax.set_xlabel("Feature column")
        ax.set_ylabel("Selected scale row")
        ax.set_xticks(range(len(feature_cols)))
        ax.set_xticklabels(feature_cols, rotation=45, fontsize=8)
        plt.colorbar(im, ax=ax, fraction=0.05)
    fig.suptitle(f"PC loadings reshaped to ({N_ROWS} rows x {len(feature_cols)} cols)", y=1.02)
    fig.tight_layout()
    fig.savefig(out_dir / "4_loading_heatmaps.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ═══ Plot 5 — PC score vs target ═══════════════════════════════════════
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    for pc_idx, ax in enumerate(axes.flat):
        ax.scatter(Z[:, pc_idx], target_val, c=target_val, cmap="plasma",
                   edgecolors="k", linewidths=0.4, s=60)
        corr = np.corrcoef(Z[:, pc_idx], target_val)[0, 1]
        ax.set_xlabel(f"PC{pc_idx + 1} score")
        ax.set_ylabel(args.target)
        ax.set_title(f"PC{pc_idx + 1}  r={corr:.3f}")
    fig.suptitle(f"PC score vs {args.target} ({len(runs)} runs)")
    fig.tight_layout()
    fig.savefig(out_dir / "5_pc_vs_target.png", dpi=150)
    plt.close(fig)

    # ═══ Plot 6 — column importance (top-5 PCs, variance-weighted) ═════════
    n_top = 5
    col_importance = np.zeros(len(feature_cols))
    for pc_idx in range(min(n_top, pca.n_components_)):
        loading = pca.components_[pc_idx].reshape(N_ROWS, len(feature_cols))
        col_importance += ev[pc_idx] * np.abs(loading).sum(axis=0)

    fig, ax = plt.subplots(figsize=(max(6, len(feature_cols)), 4))
    ax.bar(feature_cols, col_importance, color=plt.cm.tab20.colors[:len(feature_cols)])
    ax.set_xlabel("Feature column")
    ax.set_ylabel(f"Sum |loading| x variance (top {n_top} PCs)")
    ax.set_title(f"Feature column importance via PCA ({img_dir.name})")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(out_dir / "6_column_importance.png", dpi=150)
    plt.close(fig)

    # ═══ Plot 7 — row importance (selected scale rows) ═════════════════════
    row_importance = np.zeros(N_ROWS)
    for pc_idx in range(min(n_top, pca.n_components_)):
        loading = pca.components_[pc_idx].reshape(N_ROWS, len(feature_cols))
        row_importance += ev[pc_idx] * np.abs(loading).sum(axis=1)

    with open(img_dir / "selected_scales.json") as f:
        sel = json.load(f)
    row_labels = sel["selected_indices"]   # original 0-63 scale index for each of the 32 rows

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(N_ROWS), row_importance, color="steelblue", alpha=0.85)
    ax.set_xlabel(f"Row index within the selected {N_ROWS}x{len(feature_cols)} image"
                  "  (label = original 0-63 CWT scale index)")
    ax.set_ylabel(f"Sum |loading| x variance (top {n_top} PCs)")
    ax.set_title(f"Row-index importance via PCA ({img_dir.name}, target={args.target})")
    ax.set_xticks(range(N_ROWS))
    ax.set_xticklabels(row_labels, rotation=90, fontsize=6)
    fig.tight_layout()
    fig.savefig(out_dir / "7_row_importance.png", dpi=150)
    plt.close(fig)

    # ── summary ──────────────────────────────────────────────────────────
    print("\n-- Column importance (variance-weighted, top-5 PCs) --")
    for i in np.argsort(col_importance)[::-1]:
        print(f"  {feature_cols[i]:12s}: {col_importance[i]:.4f}")

    print(f"\n-- Top-10 most important rows (row index within the {N_ROWS}x{len(feature_cols)} image) --")
    for r in np.argsort(row_importance)[::-1][:10]:
        label = f" (orig scale {row_labels[r]})" if row_labels else ""
        print(f"  Row {r:2d}{label}: {row_importance[r]:.4f}")

    print(f"\n-- PC-{args.target} correlation --")
    for pc_idx in range(min(6, pca.n_components_)):
        r = np.corrcoef(Z[:, pc_idx], target_val)[0, 1]
        print(f"  PC{pc_idx + 1}: r={r:.3f}  ({ev[pc_idx] * 100:.1f}% variance)")

    print(f"\nPlots saved to {out_dir}/")


if __name__ == "__main__":
    main()
