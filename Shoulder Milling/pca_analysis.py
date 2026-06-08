"""
PCA analysis of shoulder milling feature matrices.

Loads all 72 sheets (8 sides × 9 sheets = 3 feed rates × 3 windows),
builds a 64×12 padded feature image per sheet, flattens to a 768-dim vector,
and runs PCA to understand:
  - How much variance each PC captures
  - Which feature types / row indices drive each PC
  - How well Ra separates in PC space
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# ── paths ──────────────────────────────────────────────────────────────────────
DATA_DIR  = Path(__file__).parent / "data"
OUT_DIR   = Path(__file__).parent / "pca_plots"
OUT_DIR.mkdir(exist_ok=True)

# ── feature column metadata ────────────────────────────────────────────────────
FEATURE_COLS = [
    "32FFT", "5statistics", "64mexican", "64coif",
    "KA", "SA", "KD", "SD", "rmsA", "rmsD", "crestfactA", "crestfactD",
]
N_ROWS = 64   # max feature length; shorter ones are zero-padded below

# ── roughness table ────────────────────────────────────────────────────────────
def load_ra() -> dict[int, float]:
    """Return {run_number: avg_Ra}."""
    raw = pd.read_excel(DATA_DIR / "Surface Roughness_Data.xlsx", header=None)
    run_ra = {}
    for _, row in raw.iterrows():
        try:
            rn  = int(float(row[1]))
            ra  = float(row[11])
            run_ra[rn] = ra
        except Exception:
            pass
    return run_ra

# Side file → (run_index_for_f3, run_index_for_f5, run_index_for_f7)
# From roughness spreadsheet order (sides appear in the order 1,3,5,7,2,4,6,8)
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

# ── sheet parser ───────────────────────────────────────────────────────────────
def sheet_to_image(df_raw: pd.DataFrame) -> np.ndarray:
    """
    Convert one sheet (65×12, row 0 = header) to a (64, 12) float32 image.
    Shorter feature vectors are zero-padded to length 64.
    """
    df = df_raw.copy()
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True)
    df = df.apply(pd.to_numeric, errors="coerce")

    img = np.zeros((N_ROWS, len(FEATURE_COLS)), dtype=np.float32)
    for col_idx, col in enumerate(FEATURE_COLS):
        if col not in df.columns:
            continue
        vals = df[col].dropna().values.astype(np.float32)
        n = min(len(vals), N_ROWS)
        img[:n, col_idx] = vals[:n]
    return img

# ── load all sheets ────────────────────────────────────────────────────────────
def load_dataset():
    run_ra   = load_ra()
    images   = []   # (64, 12) arrays
    ra_vals  = []   # float
    run_ids  = []   # int  (for GroupKFold later)
    side_ids = []   # int  (physical side)
    sheet_labels = []

    for side_num in range(1, 9):
        xl       = pd.ExcelFile(DATA_DIR / f"Side{side_num}.xlsx")
        run_nums = SIDE_TO_RUNS[side_num]   # (run_f3, run_f5, run_f7)

        for sheet in xl.sheet_names:
            feed_key = "f3" if "f3" in sheet else ("f5" if "f5" in sheet else "f7")
            run_num  = run_nums[{"f3": 0, "f5": 1, "f7": 2}[feed_key]]

            df_raw = xl.parse(sheet, header=None)
            img    = sheet_to_image(df_raw)

            images.append(img)
            ra_vals.append(run_ra[run_num])
            run_ids.append(run_num)
            side_ids.append(side_num)
            sheet_labels.append(f"S{side_num}/{sheet}")

    X     = np.stack(images).reshape(len(images), -1)   # (72, 768)
    ra    = np.array(ra_vals)
    runs  = np.array(run_ids)
    sides = np.array(side_ids)
    return X, ra, runs, sides, sheet_labels

# ── Ra → class label ──────────────────────────────────────────────────────────
def ra_to_class(ra: np.ndarray) -> np.ndarray:
    cls = np.empty(len(ra), dtype=object)
    cls[ra <= 0.30] = "Low (≤0.30)"
    cls[(ra > 0.30) & (ra <= 0.50)] = "Med (0.31–0.50)"
    cls[ra > 0.50] = "High (>0.50)"
    return cls

# ── main ───────────────────────────────────────────────────────────────────────
def main():
    print("Loading dataset …")
    X, ra, runs, sides, sheet_labels = load_dataset()
    print(f"  Loaded {X.shape[0]} samples, {X.shape[1]}-dim feature vector each")
    print(f"  Ra range: {ra.min():.2f} – {ra.max():.2f}  mean={ra.mean():.2f}")

    # ── run-level averages (24 runs) ──────────────────────────────────────────
    unique_runs = sorted(set(runs))
    X_run = np.array([X[runs == r].mean(axis=0) for r in unique_runs])
    ra_run = np.array([ra[runs == r][0] for r in unique_runs])
    print(f"  Run-level matrix: {X_run.shape}")

    # ── standardise on window-level data ─────────────────────────────────────
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)
    X_run_sc = scaler.transform(X_run)

    # ── PCA (window-level fit) ────────────────────────────────────────────────
    pca = PCA(n_components=min(72, X_sc.shape[1]))
    pca.fit(X_sc)
    Z_win = pca.transform(X_sc)          # (72, n_components)
    Z_run = pca.transform(X_run_sc)      # (24, n_components)

    ev  = pca.explained_variance_ratio_
    cev = np.cumsum(ev)

    # ═════════════════════════════════════════════════════════════════════════
    # Plot 1 — explained variance
    # ═════════════════════════════════════════════════════════════════════════
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.bar(range(1, 21), ev[:20] * 100, color="steelblue", alpha=0.8, label="Individual")
    ax2 = ax.twinx()
    ax2.plot(range(1, 21), cev[:20] * 100, "o-", color="darkorange", label="Cumulative")
    ax2.axhline(90, color="gray", linestyle="--", linewidth=0.8)
    ax2.set_ylabel("Cumulative variance (%)", color="darkorange")
    ax.set_xlabel("Principal component")
    ax.set_ylabel("Individual variance (%)", color="steelblue")
    ax.set_title("PCA explained variance (first 20 PCs)")
    n90 = int(np.searchsorted(cev, 0.90)) + 1
    ax.set_title(f"PCA explained variance — {n90} PCs reach 90%")
    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc="center right")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "1_explained_variance.png", dpi=150)
    plt.close(fig)
    print(f"  PCs to reach 90% variance: {n90}")

    # ═════════════════════════════════════════════════════════════════════════
    # Plot 2 — PC1 vs PC2 coloured by Ra (window-level)
    # ═════════════════════════════════════════════════════════════════════════
    classes   = ra_to_class(ra)
    class_map = {
        "Low (≤0.30)":    ("steelblue",  "o"),
        "Med (0.31–0.50)":("darkorange", "s"),
        "High (>0.50)":   ("crimson",    "^"),
    }
    fig, ax = plt.subplots(figsize=(8, 6))
    for cls, (color, marker) in class_map.items():
        mask = classes == cls
        ax.scatter(Z_win[mask, 0], Z_win[mask, 1],
                   c=color, marker=marker, label=cls, alpha=0.7, edgecolors="k", linewidths=0.4)
    ax.set_xlabel(f"PC1 ({ev[0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({ev[1]*100:.1f}%)")
    ax.set_title("PC1 vs PC2 — all 72 windows coloured by Ra class")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "2_pc1_pc2_windows.png", dpi=150)
    plt.close(fig)

    # ═════════════════════════════════════════════════════════════════════════
    # Plot 3 — PC1 vs PC2, run-level averages coloured by continuous Ra
    # ═════════════════════════════════════════════════════════════════════════
    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(Z_run[:, 0], Z_run[:, 1], c=ra_run, cmap="plasma",
                    s=80, edgecolors="k", linewidths=0.5)
    plt.colorbar(sc, ax=ax, label="Ra (µm)")
    for i, r in enumerate(unique_runs):
        ax.annotate(str(r), (Z_run[i, 0], Z_run[i, 1]),
                    fontsize=7, textcoords="offset points", xytext=(4, 3))
    ax.set_xlabel(f"PC1 ({ev[0]*100:.1f}%)")
    ax.set_ylabel(f"PC2 ({ev[1]*100:.1f}%)")
    ax.set_title("PC1 vs PC2 — run-level means, coloured by Ra (µm)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "3_pc1_pc2_runs.png", dpi=150)
    plt.close(fig)

    # ═════════════════════════════════════════════════════════════════════════
    # Plot 4 — loadings heatmap for PC1–PC4
    # Each loading reshaped to (64, 12) so we can see which feature/row drives each PC
    # ═════════════════════════════════════════════════════════════════════════
    n_pcs = 4
    fig, axes = plt.subplots(1, n_pcs, figsize=(4 * n_pcs, 6))
    for pc_idx, ax in enumerate(axes):
        loading = pca.components_[pc_idx].reshape(N_ROWS, len(FEATURE_COLS))
        vmax = np.abs(loading).max()
        im = ax.imshow(loading, aspect="auto", cmap="RdBu_r",
                       vmin=-vmax, vmax=vmax, origin="upper")
        ax.set_title(f"PC{pc_idx+1} ({ev[pc_idx]*100:.1f}%)")
        ax.set_xlabel("Feature column")
        ax.set_ylabel("Row index")
        ax.set_xticks(range(len(FEATURE_COLS)))
        ax.set_xticklabels(FEATURE_COLS, rotation=90, fontsize=7)
        plt.colorbar(im, ax=ax, fraction=0.03)
    fig.suptitle("PC loadings reshaped to (64 rows × 12 feature columns)", y=1.01)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "4_loading_heatmaps.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ═════════════════════════════════════════════════════════════════════════
    # Plot 5 — PC score vs Ra (scatter per PC)
    # ═════════════════════════════════════════════════════════════════════════
    n_pcs_show = 6
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    for pc_idx, ax in enumerate(axes.flat):
        ax.scatter(Z_run[:, pc_idx], ra_run, c=ra_run, cmap="plasma",
                   edgecolors="k", linewidths=0.4, s=60)
        corr = np.corrcoef(Z_run[:, pc_idx], ra_run)[0, 1]
        ax.set_xlabel(f"PC{pc_idx+1} score")
        ax.set_ylabel("Ra (µm)")
        ax.set_title(f"PC{pc_idx+1}  r={corr:.3f}")
    fig.suptitle("PC score vs Ra — run-level (24 runs)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "5_pc_vs_ra.png", dpi=150)
    plt.close(fig)

    # ═════════════════════════════════════════════════════════════════════════
    # Plot 6 — per-column loading magnitude summed across rows (feature importance proxy)
    # ═════════════════════════════════════════════════════════════════════════
    n_top = 5
    col_importance = np.zeros(len(FEATURE_COLS))
    for pc_idx in range(n_top):
        loading = pca.components_[pc_idx].reshape(N_ROWS, len(FEATURE_COLS))
        # Weight by explained variance of that PC
        col_importance += ev[pc_idx] * np.abs(loading).sum(axis=0)

    fig, ax = plt.subplots(figsize=(10, 4))
    colors = ["steelblue" if i < 2 else ("forestgreen" if i < 4 else "darkorange")
              for i in range(len(FEATURE_COLS))]
    ax.bar(FEATURE_COLS, col_importance, color=colors)
    ax.set_xlabel("Feature column")
    ax.set_ylabel(f"Σ |loading| × variance (top {n_top} PCs)")
    ax.set_title(f"Feature column importance via PCA (top {n_top} PCs)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "6_column_importance.png", dpi=150)
    plt.close(fig)

    # ═════════════════════════════════════════════════════════════════════════
    # Plot 7 — per-row loading magnitude summed across columns (row importance proxy)
    # ═════════════════════════════════════════════════════════════════════════
    row_importance = np.zeros(N_ROWS)
    for pc_idx in range(n_top):
        loading = pca.components_[pc_idx].reshape(N_ROWS, len(FEATURE_COLS))
        row_importance += ev[pc_idx] * np.abs(loading).sum(axis=1)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(range(N_ROWS), row_importance, color="steelblue", alpha=0.8)
    ax.axvline(31.5, color="crimson", linestyle="--", linewidth=1, label="FFT ends (row 31)")
    ax.axvline(5.5, color="darkorange", linestyle="--", linewidth=1, label="5stats ends (row 5)")
    ax.axvline(9.5, color="forestgreen", linestyle="--", linewidth=1, label="DWT stats end (row 9)")
    ax.set_xlabel("Row index within feature vector")
    ax.set_ylabel(f"Σ |loading| × variance (top {n_top} PCs)")
    ax.set_title(f"Row-index importance via PCA (top {n_top} PCs)\nRows 0–9: DWT/FFT/stats valid | Rows 10–31: FFT only | Rows 32–63: 64mex/64coif only")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "7_row_importance.png", dpi=150)
    plt.close(fig)

    # ── print summary ─────────────────────────────────────────────────────────
    print("\n-- Column importance (variance-weighted, top-5 PCs) --")
    order = np.argsort(col_importance)[::-1]
    for i in order:
        print(f"  {FEATURE_COLS[i]:15s}: {col_importance[i]:.4f}")

    print("\n-- Top-10 most important rows --")
    row_order = np.argsort(row_importance)[::-1][:10]
    for r in row_order:
        print(f"  Row {r:2d}: {row_importance[r]:.4f}")

    print("\n-- PC-Ra correlation (run-level) --")
    for pc_idx in range(6):
        r = np.corrcoef(Z_run[:, pc_idx], ra_run)[0, 1]
        print(f"  PC{pc_idx+1}: r={r:.3f}  ({ev[pc_idx]*100:.1f}% variance)")

    print(f"\nPlots saved to {OUT_DIR}/")

if __name__ == "__main__":
    main()
