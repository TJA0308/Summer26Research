"""Leak tests for nested_preproc (synthetic data, CPU, fast).

Invariant: perturbing ONLY test-fold windows must not change anything fit()
learns nor the transformed TRAINING images. Positive controls show the legacy
all-data procedures DO change (so the test is able to detect leakage).
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import nested_preproc as npp  # noqa: E402

SIDE_TO_RUNS = {1: (1, 2, 3), 2: (13, 14, 15), 3: (4, 5, 6), 4: (16, 17, 18),
                5: (7, 8, 9), 6: (19, 20, 21), 7: (10, 11, 12), 8: (22, 23, 24)}


def make_labels():
    rows = []
    for side, runs in SIDE_TO_RUNS.items():
        for fk, run in zip(("f3", "f5", "f7"), runs):
            for w in "abc":
                rows.append(dict(filename=f"r{run}_{w}.png", sample_id=f"r{run}_{w}",
                                 run_id=f"r{run}", window=w, run=run, side=side, feed=fk))
    return pd.DataFrame(rows)


def make_full(labels, seed=0):
    rng = np.random.default_rng(seed)
    full = rng.normal(size=(len(labels), 64, 12)).astype(np.float32)
    # weak feed signal on a few rows so selection is data dependent
    f = labels["feed"].map(npp.FEED_NUM).values[:, None]
    full[:, :20, 2] += 0.15 * f
    full[:, :20, 3] += 0.15 * f
    return full


LAB = make_labels()
TEST = np.where(LAB["side"].values == 1)[0]          # LOCO feed fold = one side
TRAIN = np.where(LAB["side"].values != 1)[0]


def _feedopt(full):
    return npp.make_preproc("feedopt_nested", "scalograms_32x12_feedopt", LAB,
                            full=(LAB["sample_id"].values, full))


def _arr(imgs):
    return np.stack([np.asarray(i) for i in imgs])


def _perturbed(full):
    full2 = full.copy()
    full2[TEST] = np.random.default_rng(1).normal(size=full2[TEST].shape) * 1000
    return full2


def test_feedopt_nested_ignores_test_windows():
    full = make_full(LAB)
    a, b = _feedopt(full), _feedopt(_perturbed(full))
    a.fit(TRAIN)
    b.fit(TRAIN)
    np.testing.assert_array_equal(a.rows_, b.rows_)
    np.testing.assert_array_equal(a.mu_, b.mu_)
    np.testing.assert_array_equal(a.sig_, b.sig_)
    np.testing.assert_array_equal(_arr(a.transform(TRAIN)), _arr(b.transform(TRAIN)))
    assert len(a.transform(TEST)) == len(TEST)


def test_feedopt_positive_control_all_data_fit_changes():
    """Old behaviour = fit on every window incl. test. Must react to test data."""
    full = make_full(LAB)
    allidx = np.arange(len(LAB))
    a, b = _feedopt(full), _feedopt(_perturbed(full))
    a.fit(allidx)
    b.fit(allidx)
    assert not np.array_equal(a.rows_, b.rows_) or not np.allclose(a.mu_, b.mu_)
    assert not np.array_equal(_arr(a.transform(TRAIN)), _arr(b.transform(TRAIN)))


def _resid(images, target="feed"):
    return npp.make_preproc("residual_inductive", None, LAB, target=target, images=images)


def test_residual_inductive_ignores_test_windows():
    rng = np.random.default_rng(2)
    X = rng.normal(size=(len(LAB), 32, 3)).astype(np.float32)
    X2 = X.copy()
    X2[TEST] += 500.0
    a, b = _resid(X), _resid(X2)
    a.fit(TRAIN)
    b.fit(TRAIN)
    np.testing.assert_array_equal(a.beta_, b.beta_)
    assert a.scale_ == b.scale_ and (a.lo_, a.hi_) == (b.lo_, b.hi_)
    np.testing.assert_array_equal(np.stack(a.transform(TRAIN)), np.stack(b.transform(TRAIN)))


def test_residual_inductive_removes_known_nuisance():
    """Additive speed/doc effect must be removed from an UNSEEN side's windows."""
    rng = np.random.default_rng(3)
    fac = npp.factors_from_labels(LAB)
    X = (rng.normal(size=(len(LAB), 8, 3)) * 0.01
         + 5.0 * fac["speed"].values[:, None, None]
         + 2.0 * fac["doc"].values[:, None, None]).astype(np.float32)
    pp = _resid(X)
    pp.fit(TRAIN)
    out = np.stack(pp.transform_float(TEST)) * pp.scale_
    assert np.abs(out).max() < 0.2  # nuisance gone (was up to ~11)


def test_legacy_group_residual_positive_control():
    """Legacy residual centres the held-out side on ITS OWN mean (transductive);
    the inductive variant does not (a shift of the test fold survives)."""
    rng = np.random.default_rng(4)
    X = rng.normal(size=(len(LAB), 8, 3)).astype(np.float32)
    leg = npp.legacy_group_residual(X, LAB, "feed")
    np.testing.assert_allclose(leg[TEST].mean(0), 0.0, atol=1e-5)
    X2 = X.copy()
    X2[TEST] += 7.0
    leg2 = npp.legacy_group_residual(X2, LAB, "feed")
    np.testing.assert_allclose(leg[TEST], leg2[TEST], atol=1e-4)  # shift erased by own-mean
    a, b = _resid(X), _resid(X2)
    a.fit(TRAIN)
    b.fit(TRAIN)
    assert not np.allclose(np.stack(a.transform_float(TEST)), np.stack(b.transform_float(TEST)))


def test_residual_uint8_roundtrip_keeps_signed_signal():
    """Bug repro: old transform returned signed float residuals (std ~0.5) that
    cv_evaluate._open_img clipped to [0,1] -> all negatives became 0."""
    rng = np.random.default_rng(5)
    X = rng.normal(size=(len(LAB), 8, 3)).astype(np.float32) * 10 + 100
    pp = _resid(X)
    pp.fit(TRAIN)
    flt = np.stack(pp.transform_float(TRAIN))
    assert (flt < 0).mean() > 0.3                      # signed, std ~0.5
    old = (np.clip(flt, 0, 1) * 255).round() / 255     # old _open_img path
    neg = flt < 0
    assert np.unique(old[neg]).size == 1               # old path: every negative pixel -> 0
    print("old-path corr", np.corrcoef(old.ravel(), flt.ravel())[0, 1])
    imgs = pp.transform(TRAIN)
    assert all(i.mode == "L" for i in imgs)
    u8 = np.stack([np.asarray(i) for i in imgs]).astype(float)
    assert np.corrcoef(u8.ravel(), flt.ravel())[0, 1] > 0.97
    assert np.unique(u8[neg]).size > 20                # new path keeps negative structure
    assert np.corrcoef(u8[neg], flt[neg])[0, 1] > 0.95
    assert (u8 == 0).mean() + (u8 == 255).mean() < 0.0015   # <=0.1% clipped (+rounding)
    assert pp.lo_ < 0 < pp.hi_


def test_cache_script_fails_clearly_without_data(tmp_path, monkeypatch):
    import cache_fullscale_cwt as c
    monkeypatch.setattr(c, "DATA_DIR", tmp_path)
    monkeypatch.setattr(sys, "argv", ["x"])
    try:
        c.main()
    except SystemExit as e:
        assert "raw data not found" in str(e)
    else:
        raise AssertionError("expected SystemExit")
