




"""
Extended correlation analysis for shoulder milling feature matrices.

Complements pca_analysis.py by adding supervised and non-linear methods:

  1. Spearman correlation  — per feature-position rank correlation with Ra;
                             robust to the Ra=0.92 outlier that Pearson is not.
  2. Mutual Information    — non-linear feature-Ra dependence per position.
  3. PLS Regression        — supervised DR; unlike PCA, components explicitly
                             maximise covariance with Ra rather than total variance.
  4. t-SNE                 — non-linear 2-D embedding to check whether Ra classes
                             cluster in structure that PCA's linear projection missed.

Why these on top of PCA?
  PCA showed that PC1 (46.6% variance) has only r=0.26 with Ra while PC2 and PC5
  (lower variance) have r~0.44.  This gap arises because the dominant source of
  variance in the data is the machining parameter combination (RPM x feed x depth),
  not surface roughness.  PCA is unsupervised — it cannot preferentially surface the
  Ra signal.  The methods here either directly quantify feature-Ra relationships
  (Spearman, MI) or explicitly optimise for them (PLS).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import spearmanr
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from sklearn.feature_selection import mutual_info_regression
from sklearn.manifold import TSNE

# ── shared helpers (duplicated from pca_analysis.py for standalone execution) ──
DATA_DIR = Path(__file__).parent / "data"
OUT_DIR  = Path(__file__).parent / "pca_plots"
OUT_DIR.mkdir(exist_ok=True)

FEATURE_COLS = [
    "32FFT", "5statistics", "64mexican", "64coif",
    "KA", "SA", "KD", "SD", "rmsA", "rmsD", "crestfactA", "crestfactD",
]
N_ROWS = 64

SIDE_TO_RUNS = {
    1: (1, 2, 3), 2: (13, 14, 15), 3: (4, 5, 6), 4: (16, 17, 18),
    5: (7, 8, 9), 6: (19, 20, 21), 7: (10, 11, 12), 8: (22, 23, 24),
}

def load_ra():
    raw = pd.read_excel(DATA_DIR / "Surface Roughness_Data.xlsx", header=None)
    run_ra = {}
    for _, row in raw.iterrows():
        try:
            run_ra[int(float(row[1]))] = float(row[11])
        except Exception:
            pass
    return run_ra

def sheet_to_image(df_raw):
    df = df_raw.copy()
    df.columns = df.iloc[0]
    df = df.iloc[1:].reset_index(drop=True).apply(pd.to_numeric, errors="coerce")
    img = np.zeros((N_ROWS, len(FEATURE_COLS)), dtype=np.float32)
    for col_idx, col in enumerate(FEATURE_COLS):
        if col not in df.columns:
            continue
        vals = df[col].dropna().values.astype(np.float32)
        n = min(len(vals), N_ROWS)
        img[:n, col_idx] = vals[:n]
    return img

def load_dataset():
    run_ra = load_ra()
    images, ra_vals, run_ids = [], [], []
    for side_num in range(1, 9):
        xl = pd.ExcelFile(DATA_DIR / f"Side{side_num}.xlsx")
        run_nums = SIDE_TO_RUNS[side_num]
        for sheet in xl.sheet_names:
            feed_key = "f3" if "f3" in sheet else ("f5" if "f5" in sheet else "f7")
            run_num  = run_nums[{"f3": 0, "f5": 1, "f7": 2}[feed_key]]
            img = sheet_to_image(xl.parse(sheet, header=None))
            images.append(img)
            ra_vals.append(run_ra[run_num])
            run_ids.append(run_num)
    X    = np.stack(images).reshape(len(images), -1)
    ra   = np.array(ra_vals)
    runs = np.array(run_ids)
    return X, ra, runs

def ra_to_class(ra):
    cls = np.empty(len(ra), dtype=object)
    cls[ra <= 0.30] = "Low (<=0.30)"
    cls[(ra > 0.30) & (ra <= 0.50)] = "Med (0.31-0.50)"
    cls[ra > 0.50] = "High (>0.50)"
    return cls

# ── run-level averages ─────────────────────────────────────────────────────────
def run_level(X, ra, runs):
    unique_runs = sorted(set(runs))
    X_run  = np.array([X[runs == r].mean(axis=0) for r in unique_runs])
    ra_run = np.array([ra[runs == r][0] for r in unique_runs])
    return X_run, ra_run

# ══════════════════════════════════════════════════════════════════════════════
# 1. SPEARMAN CORRELATION
# ══════════════════════════════════════════════════════════════════════════════
def plot_spearman(X_run, ra_run):
    """
    Compute Spearman rho between each of the 768 feature positions and Ra.
    Reshape to (64, 12) heatmap so we can see which feature types and which
    row indices carry the strongest monotonic relationship with Ra.

    Using run-level averages (24 data points) to avoid inflating significance
    with the 3 windows per run that share the same label.
    """
    rho_map = np.zeros((N_ROWS, len(FEATURE_COLS)))
    for j in range(X_run.shape[1]):
        col_vals = X_run[:, j]
        if col_vals.std() < 1e-10:   # constant (zero-padded) — skip
            continue
        rho, _ = spearmanr(col_vals, ra_run)
        row, col = divmod(j, len(FEATURE_COLS))
        rho_map[row, col] = rho if not np.isnan(rho) else 0.0

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # heatmap
    ax = axes[0]
    vmax = np.abs(rho_map).max()
    im = ax.imshow(rho_map, aspect="auto", cmap="RdBu_r",
                   vmin=-vmax, vmax=vmax, origin="upper")
    ax.set_xticks(range(len(FEATURE_COLS)))
    ax.set_xticklabels(FEATURE_COLS, rotation=90, fontsize=8)
    ax.set_ylabel("Row index within feature vector")
    ax.set_title("Spearman rho with Ra (run-level)")
    plt.colorbar(im, ax=ax, label="rho")

    # per-column max |rho|
    ax = axes[1]
    col_max_rho = np.abs(rho_map).max(axis=0)
    ax.bar(FEATURE_COLS, col_max_rho, color="steelblue")
    ax.set_ylabel("Max |Spearman rho| across rows")
    ax.set_title("Strongest Ra correlation per feature type")
    ax.tick_params(axis="x", rotation=45)
    ax.axhline(0.4, color="crimson", linestyle="--", linewidth=0.8, label="|rho|=0.4 threshold")
    ax.legend(fontsize=8)

    fig.suptitle("Spearman Correlation Analysis", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "8_spearman.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # summary
    print("\n-- Spearman: max |rho| per feature column --")
    order = np.argsort(col_max_rho)[::-1]
    for i in order:
        print(f"  {FEATURE_COLS[i]:15s}: max|rho|={col_max_rho[i]:.3f}")

    # find top-10 individual positions
    flat_rho = np.abs(rho_map).flatten()
    top_idx = np.argsort(flat_rho)[::-1][:10]
    print("\n-- Top-10 individual (row, col) positions by |Spearman rho| --")
    for idx in top_idx:
        row, col = divmod(idx, len(FEATURE_COLS))
        print(f"  row={row:2d}  col={FEATURE_COLS[col]:15s}  rho={rho_map[row, col]:.3f}")

    return rho_map

# ══════════════════════════════════════════════════════════════════════════════
# 2. MUTUAL INFORMATION
# ══════════════════════════════════════════════════════════════════════════════
def plot_mutual_info(X_run, ra_run):
    """
    Estimate MI between each feature position and Ra using sklearn's k-nearest
    neighbour estimator (handles non-linear, non-Gaussian relationships).

    MI is non-negative: 0 means independent, higher means more shared information.
    Unlike correlation, MI captures U-shaped or threshold relationships that
    Spearman rho would miss.
    """
    mi = mutual_info_regression(X_run, ra_run, random_state=42)
    mi_map = mi.reshape(N_ROWS, len(FEATURE_COLS))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    ax = axes[0]
    im = ax.imshow(mi_map, aspect="auto", cmap="viridis", origin="upper")
    ax.set_xticks(range(len(FEATURE_COLS)))
    ax.set_xticklabels(FEATURE_COLS, rotation=90, fontsize=8)
    ax.set_ylabel("Row index within feature vector")
    ax.set_title("Mutual Information with Ra (run-level)")
    plt.colorbar(im, ax=ax, label="MI (nats)")

    ax = axes[1]
    col_max_mi = mi_map.max(axis=0)
    ax.bar(FEATURE_COLS, col_max_mi, color="forestgreen")
    ax.set_ylabel("Max MI across rows")
    ax.set_title("Strongest MI with Ra per feature type")
    ax.tick_params(axis="x", rotation=45)

    fig.suptitle("Mutual Information Analysis", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "9_mutual_info.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    print("\n-- Mutual Info: max MI per feature column --")
    order = np.argsort(col_max_mi)[::-1]
    for i in order:
        print(f"  {FEATURE_COLS[i]:15s}: max_MI={col_max_mi[i]:.4f}")

    return mi_map

# ══════════════════════════════════════════════════════════════════════════════
# 3. PARTIAL LEAST SQUARES
# ══════════════════════════════════════════════════════════════════════════════
def plot_pls(X_run, ra_run, X_win, ra_win):
    """
    PLS finds latent components that simultaneously maximise variance in X and
    covariance with Ra — unlike PCA which maximises only variance in X.

    We compare:
      - PLS component scores vs Ra (scatter per component)
      - PLS loadings heatmap (which features drive Ra-predictive components)
      - Cross-validated R^2 as a function of number of PLS components
        (using leave-one-out on the 24 run-level points)
    """
    scaler = StandardScaler()
    X_sc   = scaler.fit_transform(X_run)

    n_comp_max = min(10, X_run.shape[0] - 1)
    pls = PLSRegression(n_components=n_comp_max, scale=False)
    pls.fit(X_sc, ra_run)
    T = pls.transform(X_sc)   # (24, n_comp_max)

    # ---- scatter: PLS component vs Ra ----
    n_show = 6
    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    for i, ax in enumerate(axes.flat):
        corr = np.corrcoef(T[:, i], ra_run)[0, 1]
        ax.scatter(T[:, i], ra_run, c=ra_run, cmap="plasma",
                   edgecolors="k", linewidths=0.4, s=60)
        ax.set_xlabel(f"PLS component {i+1}")
        ax.set_ylabel("Ra (um)")
        ax.set_title(f"PLS{i+1}  r={corr:.3f}")
    fig.suptitle("PLS Component Scores vs Ra (run-level, 24 points)")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "10_pls_scores.png", dpi=150)
    plt.close(fig)

    # ---- loadings heatmap for first 4 components ----
    n_comp_plot = 4
    fig, axes = plt.subplots(1, n_comp_plot, figsize=(4 * n_comp_plot, 6))
    for i, ax in enumerate(axes):
        loading = pls.x_loadings_[:, i].reshape(N_ROWS, len(FEATURE_COLS))
        vmax = np.abs(loading).max()
        im = ax.imshow(loading, aspect="auto", cmap="RdBu_r",
                       vmin=-vmax, vmax=vmax, origin="upper")
        ax.set_title(f"PLS{i+1} loadings")
        ax.set_xticks(range(len(FEATURE_COLS)))
        ax.set_xticklabels(FEATURE_COLS, rotation=90, fontsize=7)
        ax.set_ylabel("Row index")
        plt.colorbar(im, ax=ax, fraction=0.03)
    fig.suptitle("PLS Loadings (feature positions driving Ra-predictive components)",
                 fontsize=11, y=1.01)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "11_pls_loadings.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # ---- Leave-one-side-out R^2 vs n_components ----
    # (8 physical sides, each with 3 runs = 3 data points per test fold)
    # R^2 is undefined for n_test=1, so LOO doesn't work here; use 8-fold.
    from sklearn.model_selection import cross_val_score, KFold
    kf = KFold(n_splits=8, shuffle=False)   # 24 runs ordered by side
    r2_scores = []
    for n in range(1, n_comp_max + 1):
        m = PLSRegression(n_components=n, scale=False)
        scores = cross_val_score(m, X_sc, ra_run, cv=kf, scoring="r2")
        r2_scores.append(scores.mean())

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(range(1, n_comp_max + 1), r2_scores, "o-", color="steelblue")
    ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
    best_n = int(np.argmax(r2_scores)) + 1
    ax.axvline(best_n, color="crimson", linestyle="--",
               label=f"Best: {best_n} components (R^2={r2_scores[best_n-1]:.3f})")
    ax.set_xlabel("Number of PLS components")
    ax.set_ylabel("LOO CV R^2")
    ax.set_title("PLS: 8-fold CV R^2 vs number of components (24 runs)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "12_pls_loo_r2.png", dpi=150)
    plt.close(fig)

    print(f"\n-- PLS 8-fold CV R^2 by n_components --")
    for n, r2 in enumerate(r2_scores, 1):
        print(f"  {n} components: R^2={r2:.3f}")
    print(f"  Best: {best_n} components, R^2={r2_scores[best_n-1]:.3f}")

    # ---- PLS component importance ----
    pls_col_importance = np.abs(pls.x_loadings_[:, :4]).sum(axis=1)
    col_imp = pls_col_importance.reshape(N_ROWS, len(FEATURE_COLS)).sum(axis=0)
    print("\n-- PLS loadings: column importance (sum |loading| across rows, PLS1-4) --")
    for i in np.argsort(col_imp)[::-1]:
        print(f"  {FEATURE_COLS[i]:15s}: {col_imp[i]:.4f}")

    return pls, T

# ══════════════════════════════════════════════════════════════════════════════
# 4. t-SNE
# ══════════════════════════════════════════════════════════════════════════════
def plot_tsne(X_win, ra_win, X_run, ra_run):
    """
    t-SNE is a non-linear embedding that preserves local neighbourhood structure.
    If Ra classes form tight clusters in t-SNE space but not in PCA space, it
    indicates the class-discriminating structure is non-linear.

    We run t-SNE on the window-level data (72 points) with two perplexity values
    to check stability of the embedding.
    """
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X_win)

    # reduce to 50 PCA dims first (standard t-SNE pre-processing)
    pca_pre = PCA(n_components=min(50, X_sc.shape[0] - 1))
    X_pca = pca_pre.fit_transform(X_sc)

    class_map = {
        "Low (<=0.30)":    ("steelblue",  "o"),
        "Med (0.31-0.50)": ("darkorange", "s"),
        "High (>0.50)":    ("crimson",    "^"),
    }
    classes = ra_to_class(ra_win)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    for ax, perp in zip(axes, [5, 15]):
        tsne = TSNE(n_components=2, perplexity=perp, random_state=42,
                    max_iter=1000, init="pca")
        Z = tsne.fit_transform(X_pca)
        for cls, (color, marker) in class_map.items():
            mask = classes == cls
            ax.scatter(Z[mask, 0], Z[mask, 1], c=color, marker=marker,
                       label=cls, alpha=0.75, edgecolors="k", linewidths=0.3, s=55)
        ax.set_title(f"t-SNE (perplexity={perp})")
        ax.legend(fontsize=8)
        ax.set_xlabel("t-SNE 1")
        ax.set_ylabel("t-SNE 2")

    fig.suptitle("t-SNE — 72 windows coloured by Ra class", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT_DIR / "13_tsne.png", dpi=150)
    plt.close(fig)

# ══════════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════════
def main():
    print("Loading dataset ...")
    X, ra, runs = load_dataset()
    X_run, ra_run = run_level(X, ra, runs)

    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)
    X_run_sc = scaler.transform(X_run)

    print(f"  Window-level: {X.shape}   Run-level: {X_run.shape}")

    print("\n=== 1. Spearman Correlation ===")
    rho_map = plot_spearman(X_run_sc, ra_run)

    print("\n=== 2. Mutual Information ===")
    mi_map = plot_mutual_info(X_run_sc, ra_run)

    print("\n=== 3. Partial Least Squares ===")
    pls, T_pls = plot_pls(X_run_sc, ra_run, X_sc, ra)

    print("\n=== 4. t-SNE ===")
    plot_tsne(X_sc, ra, X_run_sc, ra_run)

    print(f"\nAll plots saved to {OUT_DIR}/")


if __name__ == "__main__":
    main()
