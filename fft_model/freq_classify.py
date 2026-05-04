"""
FFT + SVM classifier for spindle speed or depth of cut (DOC).

Speed: samples power at spindle fundamental frequencies + harmonics.
DOC:   uses log-power in broadband frequency bands (DOC changes overall amplitude).

Leave-one-run-out CV gives a fair out-of-sample result for every run.

Usage:
    python freq_classify.py --target speed --data_dir ./data
    python freq_classify.py --target doc   --data_dir ./data
    python freq_classify.py --target speed --data_dir ./data --predict data/run1.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

FS       = 16393
CHANNELS = ["ai4", "ai5", "ai6"]

# ── Speed labels & features ───────────────────────────────────────────────
SPEED_LABELS = {
    "run1": 3,  "run2": 3,  "run3": 3,
    "run4": 4,  "run5": 4,  "run6": 4,
    "run7": 0,  "run8": 0,  "run9": 0,
    "run10": 1, "run11": 1, "run12": 1,
    "run13": 2, "run14": 2, "run15": 2,
    "run16": 3, "run17": 3, "run18": 3,
    "run19": 4, "run20": 4, "run21": 4,
    "run22": 0, "run23": 0, "run24": 0,
    "run25": 1, "run26": 1, "run27": 1,
    "run28": 2, "run29": 2, "run30": 2,
    "run31": 3, "run32": 3, "run33": 3,
    "run34": 4, "run35": 4, "run36": 4,
    "run37": 0, "run38": 0, "run39": 0,
    "run40": 1, "run41": 1, "run42": 1,
    "run43": 2, "run44": 2, "run45": 2,
}
SPEED_NAMES = {0: "1500 rpm", 1: "2000 rpm", 2: "3000 rpm", 3: "4000 rpm", 4: "5000 rpm"}
SPEED_HZ    = {0: 25.0, 1: 33.33, 2: 50.0, 3: 66.67, 4: 83.33}
N_HARMONICS = 4
BIN_HALF_W  = 2

# ── DOC labels ────────────────────────────────────────────────────────────
DOC_LABELS = {
    "run1": 0,  "run2": 0,  "run3": 0,
    "run4": 0,  "run5": 0,  "run6": 0,
    "run7": 1,  "run8": 1,  "run9": 1,
    "run10": 1, "run11": 1, "run12": 1,
    "run13": 1, "run14": 1, "run15": 1,
    "run16": 1, "run17": 1, "run18": 1,
    "run19": 1, "run20": 1, "run21": 1,
    "run22": 2, "run23": 2, "run24": 2,
    "run25": 2, "run26": 2, "run27": 2,
    "run28": 2, "run29": 2, "run30": 2,
    "run31": 2, "run32": 2, "run33": 2,
    "run34": 2, "run35": 2, "run36": 2,
    "run37": 0, "run38": 0, "run39": 0,
    "run40": 0, "run41": 0, "run42": 0,
    "run43": 0, "run44": 0, "run45": 0,
}
DOC_NAMES   = {0: "0.015 mm", 1: "0.03 mm", 2: "0.06 mm"}
N_DOC_BANDS = 30  # log-spaced frequency bands from 20-4000 Hz

# ── Feed rate labels ──────────────────────────────────────────────────────
# Actual feed values in mm/rev: 0=3, 1=4, 2=5, 3=6, 4=7, 5=8
FEED_LABELS = {
    "run1":  2,  "run2":  3,  "run3":  4,   # DOC=0.015, 4000rpm, feed=5,6,7
    "run4":  3,  "run5":  4,  "run6":  5,   # DOC=0.015, 5000rpm, feed=6,7,8
    "run7":  0,  "run8":  1,  "run9":  2,   # DOC=0.030, 1500rpm, feed=3,4,5
    "run10": 0,  "run11": 1,  "run12": 2,   # DOC=0.030, 2000rpm, feed=3,4,5
    "run13": 1,  "run14": 2,  "run15": 3,   # DOC=0.030, 3000rpm, feed=4,5,6
    "run16": 2,  "run17": 3,  "run18": 4,   # DOC=0.030, 4000rpm, feed=5,6,7
    "run19": 3,  "run20": 4,  "run21": 5,   # DOC=0.030, 5000rpm, feed=6,7,8
    "run22": 0,  "run23": 1,  "run24": 2,   # DOC=0.060, 1500rpm, feed=3,4,5
    "run25": 0,  "run26": 1,  "run27": 2,   # DOC=0.060, 2000rpm, feed=3,4,5
    "run28": 1,  "run29": 2,  "run30": 3,   # DOC=0.060, 3000rpm, feed=4,5,6
    "run31": 2,  "run32": 3,  "run33": 4,   # DOC=0.060, 4000rpm, feed=5,6,7
    "run34": 3,  "run35": 4,  "run36": 5,   # DOC=0.060, 5000rpm, feed=6,7,8
    "run37": 0,  "run38": 1,  "run39": 2,   # DOC=0.015, 1500rpm, feed=3,4,5
    "run40": 0,  "run41": 1,  "run42": 2,   # DOC=0.015, 2000rpm, feed=3,4,5
    "run43": 1,  "run44": 2,  "run45": 3,   # DOC=0.015, 3000rpm, feed=4,5,6
}
FEED_NAMES  = {0: "3 mm/rev", 1: "4 mm/rev", 2: "5 mm/rev", 3: "6 mm/rev", 4: "7 mm/rev", 5: "8 mm/rev"}
N_FEED_BANDS = 50  # more bands than DOC to resolve fine amplitude differences


def extract_speed_features(csv_path):
    """Power at spindle harmonic frequencies — ideal for speed classification."""
    df        = pd.read_csv(csv_path)
    N         = len(df)
    freq_axis = np.fft.rfftfreq(N, d=1.0 / FS)
    features  = []
    for ch in CHANNELS:
        sig  = df[ch].values.astype(np.float64)
        sig -= sig.mean()
        psd  = np.abs(np.fft.rfft(sig)) ** 2
        for cls_hz in SPEED_HZ.values():
            for h in range(1, N_HARMONICS + 1):
                target = cls_hz * h
                idx    = np.argmin(np.abs(freq_axis - target))
                lo     = max(0, idx - BIN_HALF_W)
                hi     = min(len(psd), idx + BIN_HALF_W + 1)
                features.append(np.log1p(psd[lo:hi].sum()))
    return np.array(features, dtype=np.float32)


def extract_doc_features(csv_path):
    """Log-power in broadband frequency bands — captures DOC-driven amplitude changes."""
    df        = pd.read_csv(csv_path)
    N         = len(df)
    freq_axis = np.fft.rfftfreq(N, d=1.0 / FS)
    band_edges = np.geomspace(20.0, 4000.0, N_DOC_BANDS + 1)
    features  = []
    for ch in CHANNELS:
        sig  = df[ch].values.astype(np.float64)
        sig -= sig.mean()
        psd  = np.abs(np.fft.rfft(sig)) ** 2
        for lo_f, hi_f in zip(band_edges[:-1], band_edges[1:]):
            mask = (freq_axis >= lo_f) & (freq_axis < hi_f)
            features.append(np.log1p(psd[mask].sum()))
    return np.array(features, dtype=np.float32)


def extract_feed_features(csv_path):
    """Log-power in fine-grained broadband bands — feed rate shifts force amplitude across spectrum."""
    df        = pd.read_csv(csv_path)
    N         = len(df)
    freq_axis = np.fft.rfftfreq(N, d=1.0 / FS)
    band_edges = np.geomspace(20.0, 4000.0, N_FEED_BANDS + 1)
    features  = []
    for ch in CHANNELS:
        sig  = df[ch].values.astype(np.float64)
        sig -= sig.mean()
        psd  = np.abs(np.fft.rfft(sig)) ** 2
        for lo_f, hi_f in zip(band_edges[:-1], band_edges[1:]):
            mask = (freq_axis >= lo_f) & (freq_axis < hi_f)
            features.append(np.log1p(psd[mask].sum()))
    return np.array(features, dtype=np.float32)


def load_dataset(data_dir, label_map, feature_fn):
    runs, X, y = [], [], []
    for csv_path in sorted(Path(data_dir).glob("run*.csv")):
        run = csv_path.stem
        if run not in label_map:
            continue
        runs.append(run)
        X.append(feature_fn(csv_path))
        y.append(label_map[run])
    return runs, np.array(X), np.array(y)


def leave_one_run_out_cv(runs, X, y, class_names):
    correct, total = 0, 0
    per_class = {c: {"tp": 0, "n": 0} for c in class_names}
    for i, run in enumerate(runs):
        mask = np.ones(len(runs), dtype=bool)
        mask[i] = False
        clf  = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=10, gamma="scale"))
        clf.fit(X[mask], y[mask])
        pred = clf.predict(X[[i]])[0]
        true = y[i]
        per_class[true]["n"]  += 1
        per_class[true]["tp"] += int(pred == true)
        correct += int(pred == true)
        total   += 1
        status = "OK" if pred == true else f"WRONG -> {class_names[pred]}"
        print(f"  {run:<8}  true={class_names[true]:<12}  pred={class_names[pred]:<12}  {status}")

    print(f"\nOverall accuracy: {correct}/{total} = {correct/total:.1%}")
    print("Per-class accuracy:")
    for c, name in class_names.items():
        d = per_class[c]
        print(f"  {name}: {d['tp']}/{d['n']}")

    clf = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=10, gamma="scale"))
    clf.fit(X, y)
    return clf


def predict_one(csv_path, clf, class_names, feature_fn):
    feat   = feature_fn(csv_path).reshape(1, -1)
    pred   = clf.predict(feat)[0]
    scores = clf.decision_function(feat)[0]
    label  = list(class_names.values())[0].split()[0]  # "speed" or "0.015"
    print(f"\nPredicted: {class_names[pred]}")
    print("Decision scores (higher = more confident):")
    for i, (cls, name) in enumerate(class_names.items()):
        bar = "#" * max(0, int((scores[i] + 3) * 6))
        print(f"  {name:>12}  {scores[i]:+.2f}  {bar}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target",   default="speed", choices=["speed", "doc", "feed"],
                        help="Prediction target: spindle speed, depth of cut, or feed rate")
    parser.add_argument("--data_dir", default="./data", help="Folder of run CSVs")
    parser.add_argument("--predict",  default=None,    help="CSV to predict after training")
    args = parser.parse_args()

    if args.target == "doc":
        label_map   = DOC_LABELS
        class_names = DOC_NAMES
        feature_fn  = extract_doc_features
    elif args.target == "feed":
        label_map   = FEED_LABELS
        class_names = FEED_NAMES
        feature_fn  = extract_feed_features
    else:
        label_map   = SPEED_LABELS
        class_names = SPEED_NAMES
        feature_fn  = extract_speed_features

    print(f"Target: {args.target}  |  Extracting features ...")
    runs, X, y = load_dataset(args.data_dir, label_map, feature_fn)
    print(f"Loaded {len(runs)} runs, {X.shape[1]} features each\n")

    print("Leave-one-run-out cross-validation:")
    clf = leave_one_run_out_cv(runs, X, y, class_names)

    if args.predict:
        predict_one(args.predict, clf, class_names, feature_fn)


if __name__ == "__main__":
    main()
