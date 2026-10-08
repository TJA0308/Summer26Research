"""
Leak-free (fold-nested) preprocessing for LOCO cross-validation.

The legacy scalogram directories were built ONCE on all 24 runs:
  * feedopt: top-32 CWT scale rows chosen by Spearman |rho| vs feed on all
    24 runs (build_option_c/d_scalograms.py select_cwt_rows), and the
    column z-score (mu, sigma) fit on all 72 windows.
  * residual: per-group mean subtracted, where the group lies entirely inside
    the target's LOCO test fold (build_residual_scalograms.py), i.e. test
    images are centred on their own fold's mean (transductive).

This module refits those steps on the TRAINING fold only.

    pp = make_preproc(kind, img_dir, labels_df, target=...)
    pp.fit(train_idx)            # train_idx: row positions into labels_df
    imgs = pp.transform(idx)     # list aligned with labels_df rows idx

kinds
-----
'feedopt_nested'
    Same method as feedopt (Spearman scale selection against ordinal feed on
    run-level means), but selection and the z-score stats use training windows
    only. Needs the full 64-row CWT cache from cache_fullscale_cwt.py.
    Returns uint8-quantised PIL 'L' images, same layout as the legacy dirs.

'residual_inductive'   ** NEW VARIANT -- NOT the legacy residual method fixed **
    Legacy residual = subtract a per-group mean computed from the fold's own
    (test) images. This variant instead fits, on the training fold only,
    X ~ mu + additive effects of the NON-target designed factors
    (effect-coded least squares per pixel), and subtracts the fitted baseline
    from train AND test images. Levels of a nuisance factor never seen in
    training (e.g. speed target, whole doc level held out) get effect 0, so
    that factor is NOT removed for those test images. Residuals are mapped to
    uint8 with a (lo, hi) range fit on the TRAINING fold only (0.05/99.95
    percentiles, so <=0.1% of training pixels clip). Numbers from it must be
    reported as a different method, not as the legacy residual numbers.

TRANSFORM CONTRACT (shared with cv_evaluate.py)
-----------------------------------------------
transform(idx) returns a list of PIL.Image mode 'L' (uint8), one per index, for
EVERY kind. Signed/float quantities must be mapped to uint8 inside fit() using
train-fold statistics only. cv_evaluate rejects float arrays from --preproc
(its float path assumes [0,1], which silently destroyed signed residuals).
ResidualInductive.transform_float(idx) exposes the unquantised signed residual
for tests/diagnostics. After fit(), `fit_idx_` records the exact indices used.

Known remaining upstream leak (cannot be fixed here): the PNGs in img_dir were
already column-z-scored with stats from all 72 windows. 'residual_inductive'
inherits that (mild, label-free, per-column affine); 'feedopt_nested' avoids
it by rebuilding from the raw full-scale cache.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from scipy.stats import spearmanr

# Copied from cnn_train_param.py:92-93 (not imported: that module pulls torch).
SIDE_TO_SPEED = {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1}
SIDE_TO_DOC = {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2, 7: 3, 8: 3}
FEED_NUM = {"f3": 3, "f5": 5, "f7": 7}

FEATURE_COLS = ["32FFT", "5statistics", "64mexican", "64coif", "KA", "SA", "KD",
                "SD", "rmsA", "rmsD", "crestfactA", "crestfactD"]
CWT_COLS = (2, 3)
N_SELECT = 32

# designed factors that stay NUISANCE for each target (roughness mirrors the
# legacy per-side grouping: feed is excluded because it carries roughness).
NUISANCE = {
    "feed": ("speed", "doc"),
    "speed": ("doc", "feed"),
    "doc": ("speed", "feed"),
    "roughness": ("speed", "doc"),
}


def factors_from_labels(labels_df: pd.DataFrame) -> pd.DataFrame:
    side = labels_df["side"].astype(int)
    return pd.DataFrame({
        "speed": side.map(SIDE_TO_SPEED).values,
        "doc": side.map(SIDE_TO_DOC).values,
        "feed": labels_df["feed"].values,
    })


def select_scale_rows(cwt_run_means: np.ndarray, target_per_run: np.ndarray,
                      n_select: int = N_SELECT) -> np.ndarray:
    """cwt_run_means (n_runs, 64, 2); target_per_run (n_runs,). Mirrors
    build_option_c_scalograms.select_cwt_rows scoring exactly."""
    n_rows = cwt_run_means.shape[1]
    scores = np.zeros(n_rows)
    for r in range(n_rows):
        s = []
        for c in range(cwt_run_means.shape[2]):
            rho, _ = spearmanr(cwt_run_means[:, r, c], target_per_run)
            s.append(0.0 if np.isnan(rho) else abs(rho))
        scores[r] = np.mean(s)
    return np.sort(np.argsort(scores)[::-1][:n_select])


class _Base:
    fit_idx_ = None

    def fit(self, train_idx: np.ndarray) -> None:
        raise NotImplementedError

    def transform(self, idx: np.ndarray) -> list:
        raise NotImplementedError


class FeedoptNested(_Base):
    def __init__(self, img_dir, labels_df, full=None, layout=None):
        """full = (sample_ids, array (N,64,12)) or None to load
        <img_dir>/../fullscale_cwt/{full_images.npy,sample_ids.npy}."""
        self.labels = labels_df.reset_index(drop=True)
        name = Path(img_dir).name
        self.layout = layout or ("32x3" if "32x3" in name else "32x12")
        if full is None:
            d = Path(img_dir).resolve().parent / "fullscale_cwt"
            if not (d / "full_images.npy").exists():
                raise FileNotFoundError(
                    f"{d}/full_images.npy missing. Run cache_fullscale_cwt.py first "
                    "(needs data/Side*.xlsx).")
            full = (np.load(d / "sample_ids.npy", allow_pickle=True),
                    np.load(d / "full_images.npy"))
        ids, arr = full
        pos = {s: i for i, s in enumerate(np.asarray(ids).tolist())}
        self.full = np.asarray(arr, dtype=np.float32)[
            [pos[s] for s in self.labels["sample_id"]]]          # aligned to rows
        self.feed_num = self.labels["feed"].map(FEED_NUM).values.astype(float)
        self.runs = self.labels["run"].values
        self.rows_ = self.mu_ = self.sig_ = None

    def _build_raw(self, idx):
        f = self.full[idx]                                        # (n,64,12)
        n = len(idx)
        if self.layout == "32x3":
            out = np.zeros((n, N_SELECT, 3), np.float32)
            out[:, :, 0] = f[:, :N_SELECT, 0]
            out[:, :, 1] = f[:, self.rows_, 2]
            out[:, :, 2] = f[:, self.rows_, 3]
        else:
            out = np.zeros((n, N_SELECT, 12), np.float32)
            for c in range(12):
                out[:, :, c] = f[:, self.rows_, c] if c in CWT_COLS else f[:, :N_SELECT, c]
        return out

    def fit(self, train_idx):
        train_idx = np.asarray(train_idx)
        self.fit_idx_ = train_idx.copy()
        runs = np.unique(self.runs[train_idx])
        means = np.zeros((len(runs), self.full.shape[1], 2))
        tgt = np.zeros(len(runs))
        for i, r in enumerate(runs):
            m = train_idx[self.runs[train_idx] == r]
            means[i, :, 0] = self.full[m, :, 2].mean(0)
            means[i, :, 1] = self.full[m, :, 3].mean(0)
            tgt[i] = self.feed_num[m[0]]
        if len(np.unique(tgt)) < 2:
            raise ValueError("training fold has <2 distinct feed values")
        self.rows_ = select_scale_rows(means, tgt)
        raw = self._build_raw(train_idx)
        flat = raw.reshape(-1, raw.shape[-1])
        self.mu_ = flat.mean(0)
        sig = flat.std(0)
        sig[sig < 1e-10] = 1.0
        self.sig_ = sig

    def transform(self, idx):
        if self.rows_ is None:
            raise RuntimeError("call fit() first")
        z = (self._build_raw(np.asarray(idx)) - self.mu_) / self.sig_
        u8 = np.clip((z + 3) / 6 * 255, 0, 255).astype(np.uint8)
        return [Image.fromarray(a) for a in u8]


class ResidualInductive(_Base):
    """NEW variant: train-fold additive nuisance baseline (see module doc)."""

    def __init__(self, img_dir, labels_df, target, images=None, nuisance=None):
        self.labels = labels_df.reset_index(drop=True)
        self.target = target
        self.nuis = tuple(nuisance or NUISANCE[target])
        if images is None:
            images = np.stack([
                np.asarray(Image.open(Path(img_dir) / fn).convert("L"), np.float32)
                for fn in self.labels["filename"]])
        self.X = np.asarray(images, np.float32)
        self.shape = self.X.shape[1:]
        fac = factors_from_labels(self.labels)
        self.fac = {k: fac[k].values for k in self.nuis}
        self.levels_ = None

    def _design(self, idx):
        cols = [np.ones((len(idx), 1))]
        for k in self.nuis:
            lv = self.levels_[k]
            v = self.fac[k][idx]
            if len(lv) < 2:
                continue
            m = np.zeros((len(idx), len(lv) - 1))
            for j, l in enumerate(lv[:-1]):
                m[:, j] = (v == l)
            last = (v == lv[-1])
            m[last, :] = -1.0                      # effect coding, last = -sum
            cols.append(m)                         # unseen level -> all zeros
        return np.hstack(cols)

    def fit(self, train_idx):
        train_idx = np.asarray(train_idx)
        self.fit_idx_ = train_idx.copy()
        self.levels_ = {k: sorted(pd.unique(self.fac[k][train_idx]).tolist())
                        for k in self.nuis}
        D = self._design(train_idx)
        Y = self.X[train_idx].reshape(len(train_idx), -1).astype(np.float64)
        self.beta_, *_ = np.linalg.lstsq(D, Y, rcond=None)
        res = Y - D @ self.beta_
        self.scale_ = float(res.std()) * 2 + 1e-6
        z = res / self.scale_
        self.lo_, self.hi_ = (float(v) for v in np.quantile(z, [0.0005, 0.9995]))
        if self.hi_ - self.lo_ < 1e-9:
            self.hi_ = self.lo_ + 1e-9

    def transform_float(self, idx):
        """Signed residual / scale_ (float32 arrays), unquantised."""
        if self.levels_ is None:
            raise RuntimeError("call fit() first")
        idx = np.asarray(idx)
        base = self._design(idx) @ self.beta_
        res = (self.X[idx].reshape(len(idx), -1) - base) / self.scale_
        return [r.reshape(self.shape).astype(np.float32) for r in res]

    def transform(self, idx):
        """uint8 'L' images; (lo_, hi_) from the training fold maps to 0..255."""
        out = []
        for r in self.transform_float(idx):
            u8 = np.clip((r - self.lo_) / (self.hi_ - self.lo_) * 255.0, 0, 255)
            out.append(Image.fromarray(u8.round().astype(np.uint8)))
        return out


def make_preproc(kind: str, img_dir, labels_df: pd.DataFrame, target: str = "feed", **kw):
    """kind in {'feedopt_nested', 'residual_inductive'}. target only matters for
    residual_inductive (selects which factors are nuisance)."""
    if kind == "feedopt_nested":
        return FeedoptNested(img_dir, labels_df, **kw)
    if kind == "residual_inductive":
        return ResidualInductive(img_dir, labels_df, target, **kw)
    raise ValueError(f"unknown kind {kind!r}")


def legacy_group_residual(images: np.ndarray, labels_df: pd.DataFrame, target: str):
    """LEGACY transductive residual (mirrors build_residual_scalograms.py:
    group_key + group mean over ALL supplied rows). Only for positive-control
    tests / comparison; never use inside a CV loop."""
    side = labels_df["side"].astype(int).values
    feed = labels_df["feed"].values
    if target in ("feed", "roughness"):
        keys = [(s,) for s in side]
    elif target == "speed":
        keys = [(SIDE_TO_DOC[s], f) for s, f in zip(side, feed)]
    else:
        keys = [(SIDE_TO_SPEED[s], f) for s, f in zip(side, feed)]
    out = np.empty_like(images, dtype=np.float32)
    for k in set(keys):
        m = np.array([kk == k for kk in keys])
        out[m] = images[m] - images[m].mean(0)
    return out
