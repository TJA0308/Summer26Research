"""
Shared feature computation for build_rawwindow_features.py -- the raw-
waveform analog of em_feature_common.py. Where em_feature_common.py READS
precomputed 32FFT/64mexican/64coif/etc. columns from Excel (one real
measurement per run), this module COMPUTES the same 12 feature types fresh
from real, non-overlapping time windows of the raw signal (data/run{N}.csv),
so every window is a genuinely independent sample -- not a row-split
fragment of a single measurement.

Reuses RUNS/RA_VALUES/FEATURE_COLS/COL_IDX from em_feature_common.py so the
Excel-based and raw-window-based 32x12 layouts are directly comparable
(same column names/order, same 45 runs, same Ra values).

Column semantics (matching Shoulder Milling's schema, confirmed in
Shoulder Milling/scalogram_readme.md):
  32FFT        -- mean FFT magnitude in 32 EQUAL-width bands, 0 Hz to
                  Nyquist (see fft_band_means).
  5statistics  -- 6 time-domain descriptors of the raw window signal itself:
                  [mean, variance, skewness, kurtosis, rms, crest_factor].
                  ("5statistics" despite 6 values -- matches Shoulder
                  Milling's own column, which is also 6 real values despite
                  the name; see scalogram_readme.md Section 3's row table.)
  64mexican    -- RMS energy of a Mexican-hat (Ricker) CWT at 64 scales.
  64coif       -- RMS energy of a Coiflet-4-derived CWT at 64 scales (see
                  em_feature_common-style caveat: PyWavelets has no native
                  continuous coiflet wavelet, so this is built from the
                  coiflet-4 discrete wavelet's scaling function via
                  wavefun() -- an approximation, not a claim of exactness).
  KA/SA/KD/SD, rmsA/rmsD, crestfactA/crestfactD
               -- kurtosis/skewness/RMS/crest-factor of the approximation
                  (A) and detail (D) coefficients at each of 10 successive
                  single-level DWT decompositions (db4 wavelet) of the
                  window signal. "10 decomposition levels" per Shoulder
                  Milling's schema -- db4 is this module's own choice (not
                  verified against an unavailable original).
"""
import numpy as np
import pandas as pd
import pywt
from scipy.stats import kurtosis, skew, spearmanr

from em_feature_common import (   # noqa: F401  (re-exported for callers)
    RUNS, RA_VALUES, FEATURE_COLS, COL_IDX, load_cnn_train_module,
)

FS = 16393.0
N_FULL = 64        # candidate CWT scales before selection
N_SELECT = 32       # selected CWT scales / output rows
N_FFT_BANDS = 32
DWT_WAVELET = "db4"
DWT_LEVELS = 10


# ── per-window feature computation ──────────────────────────────────────────
def load_run_signal(data_dir, run: str, channel: str = "ai4") -> np.ndarray:
    df = pd.read_csv(data_dir / f"{run}.csv")
    return df[channel].to_numpy(dtype=np.float64)


def split_windows(signal: np.ndarray, n_windows: int) -> list:
    n = len(signal)
    chunk = n // n_windows
    return [signal[i * chunk:(i + 1) * chunk] for i in range(n_windows)]


def fft_band_means(signal: np.ndarray, fs: float = FS, n_bands: int = N_FFT_BANDS) -> np.ndarray:
    """Mean FFT magnitude in n_bands equal-width bands from 0 Hz to Nyquist."""
    freqs = np.fft.rfftfreq(len(signal), d=1.0 / fs)
    mags = np.abs(np.fft.rfft(signal - signal.mean()))
    edges = np.linspace(0.0, fs / 2.0, n_bands + 1)
    out = np.zeros(n_bands)
    for i in range(n_bands):
        hi_incl = (i == n_bands - 1)
        mask = (freqs >= edges[i]) & ((freqs <= edges[i + 1]) if hi_incl else (freqs < edges[i + 1]))
        out[i] = mags[mask].mean() if mask.any() else 0.0
    return out


def ricker(points: int, width: float) -> np.ndarray:
    """Mexican-hat (Ricker) mother wavelet -- vendored formula (rather than
    scipy.signal.ricker/cwt, which SciPy deprecated/removed)."""
    a = float(width)
    A = 2.0 / (np.sqrt(3.0 * a) * np.pi ** 0.25)
    vec = np.arange(0, points) - (points - 1.0) / 2.0
    xsq = vec ** 2
    wsq = a ** 2
    mod = 1.0 - xsq / wsq
    gauss = np.exp(-xsq / (2.0 * wsq))
    return A * mod * gauss


def _coif_mother(precision: int = 8, coif_name: str = "coif4"):
    wavelet = pywt.Wavelet(coif_name)
    _, psi, x = wavelet.wavefun(level=precision)
    psi = np.asarray(psi, dtype=np.float64)
    psi = psi - psi.mean()
    norm = np.sqrt(np.sum(psi ** 2))
    if norm > 0:
        psi = psi / norm
    x = np.asarray(x, dtype=np.float64)
    x_norm = (x - x[0]) / (x[-1] - x[0]) - 0.5
    return x_norm, psi


_COIF_X, _COIF_PSI = _coif_mother()


def coif_wavelet(points: int, width: float) -> np.ndarray:
    """Coiflet-4-derived mother wavelet, fixed [-0.5, 0.5] support resampled
    to `points` samples -- `width` is not applied here since the caller
    already grows `points` with width (see cwt_scale_energies), which is
    what performs the dilation; scaling here too would double-apply it."""
    t = np.linspace(-0.5, 0.5, points)
    return np.interp(t, _COIF_X, _COIF_PSI)


def _manual_cwt(signal: np.ndarray, wavelet_fn, widths: np.ndarray) -> np.ndarray:
    """Same algorithm as (the now-deprecated) scipy.signal.cwt: per width,
    an N=min(10*width, len(signal))-sample kernel convolved 'same'."""
    out = np.empty((len(widths), len(signal)), dtype=np.float64)
    for i, w in enumerate(widths):
        n = max(int(min(10 * w, len(signal))), 1)
        out[i] = np.convolve(signal, wavelet_fn(n, w), mode="same")
    return out


def cwt_scale_energies(signal: np.ndarray, wavelet_fn, n_scales: int = N_FULL) -> np.ndarray:
    """RMS energy of the CWT coefficients at each of scales 1..n_scales."""
    widths = np.arange(1, n_scales + 1)
    coeffs = _manual_cwt(signal, wavelet_fn, widths)
    return np.sqrt(np.mean(coeffs ** 2, axis=1))


def time_domain_stats(signal: np.ndarray) -> np.ndarray:
    """6 values: mean, variance, skewness, kurtosis, RMS, crest factor --
    the "5statistics" column (6 real values despite the name; see module
    docstring)."""
    mean = signal.mean()
    var = signal.var()
    sk = skew(signal)
    ku = kurtosis(signal)
    rms = np.sqrt(np.mean(signal ** 2))
    crest = np.max(np.abs(signal)) / (rms + 1e-12)
    return np.array([mean, var, sk, ku, rms, crest])


def dwt_level_stats(signal: np.ndarray, wavelet: str = DWT_WAVELET, n_levels: int = DWT_LEVELS) -> dict:
    """Iteratively single-level-decomposes the signal `n_levels` times
    (cA_0 = signal, (cA_i, cD_i) = pywt.dwt(cA_{i-1}, wavelet)), returning
    8 length-n_levels arrays: KA, SA, KD, SD, rmsA, rmsD, crestfactA,
    crestfactD."""
    KA = np.zeros(n_levels); SA = np.zeros(n_levels)
    KD = np.zeros(n_levels); SD = np.zeros(n_levels)
    rmsA = np.zeros(n_levels); rmsD = np.zeros(n_levels)
    crestA = np.zeros(n_levels); crestD = np.zeros(n_levels)

    cA = signal
    for i in range(n_levels):
        cA, cD = pywt.dwt(cA, wavelet)
        KA[i] = kurtosis(cA); SA[i] = skew(cA)
        KD[i] = kurtosis(cD); SD[i] = skew(cD)
        rmsA[i] = np.sqrt(np.mean(cA ** 2))
        rmsD[i] = np.sqrt(np.mean(cD ** 2))
        crestA[i] = np.max(np.abs(cA)) / (rmsA[i] + 1e-12)
        crestD[i] = np.max(np.abs(cD)) / (rmsD[i] + 1e-12)

    return {"KA": KA, "SA": SA, "KD": KD, "SD": SD,
            "rmsA": rmsA, "rmsD": rmsD, "crestfactA": crestA, "crestfactD": crestD}


def compute_window_features(signal: np.ndarray) -> dict:
    """All raw feature vectors for one real time window: fft (32,),
    mex (64,), coi (64,), stats5 (6,), dwt (dict of 8x(10,))."""
    return {
        "fft": fft_band_means(signal),
        "mex": cwt_scale_energies(signal, ricker),
        "coi": cwt_scale_energies(signal, coif_wavelet),
        "stats5": time_domain_stats(signal),
        "dwt": dwt_level_stats(signal),
    }


# ── scale selection (identical method to em_feature_common.select_cwt_rows,
#    but averaging each RUN's own real windows instead of reading one
#    precomputed measurement) ────────────────────────────────────────────
def target_value(mod, run: str, target: str):
    if target == "roughness":
        return RA_VALUES[run]
    if target == "feed_coarse":
        return mod.FEED_LABELS[run] + 3
    if target == "speed":
        return int(mod.SPEED_NAMES[mod.SPEED_LABELS[run]].split()[0])
    if target == "doc":
        return float(mod.DOC_NAMES[mod.DOC_LABELS[run]].split()[0])
    raise ValueError(target)


def select_cwt_rows(run_mex_mean: dict, run_coi_mean: dict, mod, target: str, runs_sorted: list):
    """run_mex_mean/run_coi_mean: {run: (64,) array}, already averaged
    across that run's windows. Returns (top_idx sorted ascending, scores)."""
    mex = np.stack([run_mex_mean[r] for r in runs_sorted])
    coi = np.stack([run_coi_mean[r] for r in runs_sorted])
    target_arr = np.array([target_value(mod, r, target) for r in runs_sorted])

    scores = np.zeros(N_FULL)
    for row_i in range(N_FULL):
        s_mex, _ = spearmanr(mex[:, row_i], target_arr)
        s_coi, _ = spearmanr(coi[:, row_i], target_arr)
        s_mex = 0.0 if np.isnan(s_mex) else abs(s_mex)
        s_coi = 0.0 if np.isnan(s_coi) else abs(s_coi)
        scores[row_i] = (s_mex + s_coi) / 2.0

    top_idx = np.sort(np.argsort(scores)[::-1][:N_SELECT])
    return top_idx, scores
