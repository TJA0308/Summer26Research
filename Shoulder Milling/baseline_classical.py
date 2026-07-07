"""
Classical-ML baseline at NATIVE scalogram resolution (32x12 / 32x3) -- no
ImageNet backbone, no 224x224 upsampling. Sanity check for whether the 4
pretrained CNN backbones (resnet18/50, efficientnet_b0, convnext_tiny) are
actually worth their capacity/domain mismatch on this 48-train-sample
dataset, or whether a much simpler model gets comparable accuracy.

Reuses the same TARGETS splits and label_for as cnn_train_param.py so
results are directly comparable to eval_param_sweep_summary.csv.

Usage:
    python baseline_classical.py
    python baseline_classical.py --targets feed roughness --dirs scalograms_32x12 scalograms_32x12_feedopt
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from cnn_train_param import TARGETS, label_for

ROOT = Path(__file__).parent

MODELS = {
    "logreg":  lambda: LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced"),
    "rf":      lambda: RandomForestClassifier(n_estimators=300, max_depth=6,
                                               class_weight="balanced", random_state=42),
    "svm_rbf": lambda: SVC(kernel="rbf", C=1.0, class_weight="balanced", random_state=42),
    "hgb":     lambda: HistGradientBoostingClassifier(max_iter=150, random_state=42),
}


def load_native(img_dir: Path, target: str):
    df = pd.read_csv(img_dir / "labels.csv")
    df["label"] = df.apply(lambda r: label_for(target, r["side"], r["feed"], r.get("ra")), axis=1)

    spec     = TARGETS[target]
    train_df = df[df["run_id"].isin(spec["train_runs"])].reset_index(drop=True)
    test_df  = df[df["run_id"].isin(spec["test_runs"])].reset_index(drop=True)

    def to_arrays(sub):
        X = np.stack([
            np.asarray(Image.open(img_dir / fn).convert("L"), dtype=np.float32).ravel()
            for fn in sub["filename"]
        ])
        return X, sub["label"].to_numpy(), sub["run_id"].to_numpy()

    return to_arrays(train_df), to_arrays(test_df)


def majority_vote(preds, labels, runs):
    run_preds, run_true = {}, {}
    for p, t, r in zip(preds, labels, runs):
        run_preds.setdefault(r, []).append(p)
        run_true[r] = t
    correct = sum(
        int(max(set(run_preds[r]), key=run_preds[r].count) == run_true[r])
        for r in run_true
    )
    return correct / len(run_true)


def run_one(target, img_dir):
    (Xtr, ytr, rtr), (Xte, yte, rte) = load_native(img_dir, target)
    n_components = min(20, Xtr.shape[0] - 1)
    rows = []
    for name, make_model in MODELS.items():
        pipe = Pipeline([
            ("scale", StandardScaler()),
            ("pca", PCA(n_components=n_components, random_state=42)),
            ("clf", make_model()),
        ])
        pipe.fit(Xtr, ytr)
        preds = pipe.predict(Xte)
        rows.append({
            "target": target,
            "scalogram": img_dir.name.replace("scalograms_", ""),
            "model": name,
            "window_acc": round(float((preds == yte).mean()), 4),
            "run_acc": round(majority_vote(preds, yte, rte), 4),
        })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", nargs="+", default=["speed", "feed", "doc", "roughness"])
    parser.add_argument("--dirs", nargs="+", default=[
        "scalograms_32x12", "scalograms_32x3",
        "scalograms_32x12_feedopt", "scalograms_32x3_feedopt",
    ])
    args = parser.parse_args()

    all_rows = []
    for target in args.targets:
        for dir_name in args.dirs:
            img_dir = ROOT / dir_name
            if not img_dir.exists():
                continue
            if "feedopt" in dir_name and target != "feed":
                continue  # feedopt scalograms were only built/labelled for the feed pipeline
            print(f"\n=== {target} | {dir_name} ===")
            rows = run_one(target, img_dir)
            for r in rows:
                print(f"  {r['model']:10s}  window={r['window_acc']:.3f}  run={r['run_acc']:.3f}")
            all_rows.extend(rows)

    out = pd.DataFrame(all_rows)
    out.to_csv(ROOT / "baseline_classical_summary.csv", index=False)
    print(f"\nWrote {len(out)} rows -> baseline_classical_summary.csv")


if __name__ == "__main__":
    main()
