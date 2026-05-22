"""
Hilbert envelope utilities for machining vibration signals.

Computes the instantaneous amplitude envelope of a signal by:
  1. Optional bandpass filter to isolate a frequency band of interest
  2. Hilbert transform to produce the analytic signal
  3. Take the modulus: envelope = |x + j*H{x}|

The envelope demodulates carrier oscillations (e.g. spindle harmonics)
and exposes the slower amplitude-modulation pattern driven by chip load,
DOC, and feed rate.
"""
import numpy as np
from scipy.signal import hilbert, butter, sosfiltfilt


def compute_envelope(signal: np.ndarray, fs: float,
                     f_low: float = None, f_high: float = None) -> np.ndarray:
    """
    Return the Hilbert amplitude envelope of `signal`.

    Parameters
    ----------
    signal : 1-D float array  (raw vibration samples, any DC offset allowed)
    fs     : effective sampling rate in Hz (after any downsampling)
    f_low  : optional bandpass lower cutoff in Hz (highpass if f_high is None)
    f_high : optional bandpass upper cutoff in Hz (lowpass  if f_low  is None)

    Returns
    -------
    envelope : 1-D float32 array, same length as signal, values >= 0
    """
    x = signal.astype(np.float64)
    x -= x.mean()

    if f_low is not None or f_high is not None:
        x = _bandpass(x, fs, f_low, f_high)

    return np.abs(hilbert(x)).astype(np.float32)


def _bandpass(signal: np.ndarray, fs: float,
              f_low: float = None, f_high: float = None,
              order: int = 4) -> np.ndarray:
    """Zero-phase Butterworth bandpass / highpass / lowpass filter."""
    nyq = fs / 2.0
    if f_low is not None and f_high is not None:
        sos = butter(order, [f_low / nyq, f_high / nyq], btype="band", output="sos")
    elif f_low is not None:
        sos = butter(order, f_low / nyq, btype="high", output="sos")
    else:
        sos = butter(order, f_high / nyq, btype="low",  output="sos")
    return sosfiltfilt(sos, signal)
