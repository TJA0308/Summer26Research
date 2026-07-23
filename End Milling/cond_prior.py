"""
Shared condition-prior helpers for End Milling's feed_coarse/roughness targets.

Background: unlike Shoulder Milling (where feed is experimentally independent
of the nuisance condition -- exactly one run per feed class per side), End
Milling's feed_coarse is almost a clean deterministic function of SPEED alone
(identical class pattern at every speed value, across all 3 DOC levels), and
roughness a smooth, monotonic function of (DOC, speed) jointly. Both targets
are causally downstream of the machining condition -- a KNOWN, CONTROLLED
parameter (you set DOC/speed on the machine; you don't need vibration to
infer them) -- not merely confounded by it. Condition-residual subtraction
(build_residual_scalograms.py) removes real target signal here rather than
just nuisance noise, which is why it gave inconsistent results under honest
leave-one-condition-out CV (see cv_evaluate_32x3.py's docstring/cv_summary.csv).

This module extracts that condition -> target pattern directly instead:
fit a small classifier on (DOC, speed) one-hot -> class alone (no image data),
and combine its predicted probabilities with an image model's via a weighted
PROBABILITY AVERAGE (not feature concatenation -- concatenating condition
one-hot with pixel PCA features was tried in cv_evaluate_32x3.py and made
things WORSE, diluting the clean condition signal with noisy pixel
components; probability-averaging keeps the two signal sources from
interfering with each other's decision boundaries).

Dependency-light by design (numpy + sklearn only, no torch, no repo-internal
imports) so this is importable both from the repo root (cv_evaluate_32x3.py,
stack_conditioning_32x3.py) and from cnn_model/cnn_train_32x3.py (which adds
this directory to sys.path, mirroring its existing import of cnn_train).
"""
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier

N_DOC = 3
N_SPEED = 5


def condition_onehot(conditions) -> np.ndarray:
    """[(doc, speed), ...] -> concatenated one-hot [n, N_DOC + N_SPEED]."""
    docs = np.array([c[0] for c in conditions])
    speeds = np.array([c[1] for c in conditions])
    return np.hstack([np.eye(N_DOC)[docs], np.eye(N_SPEED)[speeds]])


def conditions_for_runs(runs, doc_labels: dict, speed_labels: dict) -> dict:
    """runs (iterable of run names) -> {run: (doc_labels[run], speed_labels[run])}."""
    return {r: (doc_labels[r], speed_labels[r]) for r in runs}


def fit_condition_prior(train_conditions, train_labels, num_classes: int, seed: int = 42):
    """HGB on the (DOC, speed) one-hot alone -- no image data. Returns
    (clf, classes_) so predict_condition_prior can re-expand predict_proba's
    output to the FULL num_classes width regardless of which classes this
    particular training fold happened to contain."""
    X = condition_onehot(train_conditions)
    clf = HistGradientBoostingClassifier(max_iter=150, random_state=seed)
    clf.fit(X, train_labels)
    return clf, clf.classes_


def predict_condition_prior(clf, classes_, test_conditions, num_classes: int) -> np.ndarray:
    """Predicts condition-prior probabilities for test_conditions, re-expanded
    to full [n, num_classes] width -- zero-filling any class absent from the
    training fold. Fixes a latent bug: HistGradientBoostingClassifier.
    predict_proba only emits columns for classes it saw in training; under
    LOCO or an imbalanced split this silently misaligns column indices when
    averaged against a full-width CNN softmax (e.g. if training saw only
    classes {0, 2}, raw predict_proba returns a 2-column array where column
    1 actually means class 2, not class 1)."""
    X = condition_onehot(test_conditions)
    raw_proba = clf.predict_proba(X)
    full = np.zeros((len(test_conditions), num_classes), dtype=np.float64)
    for col, cls in enumerate(classes_):
        full[:, int(cls)] = raw_proba[:, col]
    return full


def stack_probs(cond_probs: np.ndarray, pixel_probs: np.ndarray, cond_weight: float) -> np.ndarray:
    """Weighted probability average -- NOT feature concatenation (see module
    docstring for why concatenation was rejected). cond_weight=1.0 is
    condition-only, 0.0 is pixel-model-only."""
    return cond_weight * cond_probs + (1 - cond_weight) * pixel_probs
