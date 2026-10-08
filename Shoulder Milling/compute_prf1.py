"""Run-level precision / recall / F1 for LOCO predictions saved by
`cv_evaluate.py --save_preds <dir>`.

Each input CSV holds the per-window held-out softmax probabilities for ONE
(target, scalogram, model, group, seed) LOCO run (columns: filename, run_id,
fold, label, p0..pK-1). Because every run is held out exactly once in LOCO,
pooling all folds gives exactly one prediction per run (24 runs).

Headline = run-level soft vote (mean probability over a run's windows), the
same rule as cv_evaluate.vote(). Reported per class and macro-averaged;
window-level macro-F1 is shown for reference. Metrics come from LOCO held-out
folds only -- never from training data.

Usage:
    python compute_prf1.py cv_preds/*.csv
    python compute_prf1.py cv_preds/speed__32x12_9win__cnn-resnet18__primary__s42.csv --out_md prf1.md
"""
import argparse
import glob
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

FNAME = re.compile(r"^(?P<target>[^_]+)__(?P<scalogram>.+)__(?P<model>[^_]+(?:-[^_]+)?)__"
                   r"(?P<group>[^_]+)__s(?P<seed>\d+)$")


def run_level(df: pd.DataFrame):
    pcols = [c for c in df.columns if re.fullmatch(r"p\d+", c)]
    g = df.groupby("run_id")
    probs = g[pcols].mean()
    y_true = g["label"].first().reindex(probs.index).to_numpy()
    y_pred = probs.to_numpy().argmax(axis=1)
    return y_true, y_pred, len(pcols)


def prf(y_true, y_pred, k):
    labels = list(range(k))
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
    mp, mr, mf, _ = precision_recall_fscore_support(y_true, y_pred, labels=labels,
                                                    average="macro", zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return dict(p=p, r=r, f=f, s=s, macro=(mp, mr, mf), acc=float((y_true == y_pred).mean()), cm=cm)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("preds", nargs="+", help="prediction CSVs (globs ok)")
    ap.add_argument("--out_md", default=None, help="also write the markdown report here")
    args = ap.parse_args()

    files = sorted({f for pat in args.preds for f in glob.glob(pat)})
    if not files:
        raise SystemExit("no prediction files matched")

    lines, summary = [], []
    for f in files:
        m = FNAME.match(Path(f).stem)
        tag = Path(f).stem if m is None else (
            f"{m['target']} | {m['scalogram']} | {m['model']} | group={m['group']} | seed {m['seed']}")
        df = pd.read_csv(f)
        y_true, y_pred, k = run_level(df)
        res = prf(y_true, y_pred, k)
        win_pred = df[[c for c in df.columns if re.fullmatch(r"p\d+", c)]].to_numpy().argmax(axis=1)
        _, _, win_f1, _ = precision_recall_fscore_support(df["label"], win_pred, labels=list(range(k)),
                                                          average="macro", zero_division=0)
        lines += [f"### {tag}", "",
                  f"Run-level soft vote over {len(y_true)} held-out runs (LOCO): "
                  f"accuracy **{res['acc']:.3f}**, macro-P **{res['macro'][0]:.3f}**, "
                  f"macro-R **{res['macro'][1]:.3f}**, macro-F1 **{res['macro'][2]:.3f}** "
                  f"(window-level macro-F1 {win_f1:.3f})", "",
                  "| Class | Precision | Recall | F1 | Support (runs) |", "|---|---|---|---|---|"]
        for c in range(k):
            lines.append(f"| {c} | {res['p'][c]:.3f} | {res['r'][c]:.3f} | {res['f'][c]:.3f} | {int(res['s'][c])} |")
        lines += ["", "Confusion matrix (rows = true, cols = predicted):", "", "```",
                  np.array2string(res["cm"]), "```", ""]
        if m:
            summary.append(dict(key=(m["target"], m["scalogram"], m["model"], m["group"]),
                                seed=int(m["seed"]), acc=res["acc"], mp=res["macro"][0],
                                mr=res["macro"][1], mf=res["macro"][2]))

    # multi-seed roll-up (only where >1 seed for the same config)
    by = {}
    for s in summary:
        by.setdefault(s["key"], []).append(s)
    multi = {k: v for k, v in by.items() if len(v) > 1}
    if multi:
        lines += ["### Across seeds (mean +/- std, ddof=1)", "",
                  "| Config | Seeds | Accuracy | Macro-P | Macro-R | Macro-F1 |", "|---|---|---|---|---|---|"]
        for k, v in multi.items():
            def ms(name):
                a = np.array([x[name] for x in v])
                return f"{a.mean():.3f} +/- {a.std(ddof=1):.3f}"
            lines.append(f"| {' / '.join(k)} | {len(v)} | {ms('acc')} | {ms('mp')} | {ms('mr')} | {ms('mf')} |")
        lines.append("")

    out = "\n".join(lines)
    print(out)
    if args.out_md:
        Path(args.out_md).write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
