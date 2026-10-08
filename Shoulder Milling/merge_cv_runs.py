"""
Merge cv_summary.csv plus every CSV under cv_runs/** into cv_summary_merged.csv.

De-duplicates on (target, scalogram, model, arch, split, group, seed, lr,
preproc), keeping the row with the latest `timestamp` (rows lacking a
timestamp sort oldest; ties keep the later-read row). Never overwrites
cv_summary.csv.

Legacy rows (pre-dating the lr column) have a blank lr. By default they stay
blank. With --infer_legacy_lr, for each key (everything except lr), blank-lr
seed-42 rows are assigned lr=1e-3 for the first one and lr=1e-4 for the second
(file/row order). Only seed 42 is inferred; other blank-lr rows stay blank.

Usage:
    python merge_cv_runs.py [--infer_legacy_lr] [--out cv_summary_merged.csv]
"""
import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
KEY = ["target", "scalogram", "model", "arch", "split", "group", "seed", "lr", "preproc"]


def _read(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["_source"] = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
    return df


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--infer_legacy_lr", action="store_true",
                    help="blank-lr seed-42 legacy rows: first per key = 1e-3, second = 1e-4")
    ap.add_argument("--out", default="cv_summary_merged.csv")
    args = ap.parse_args()

    files = []
    base = ROOT / "cv_summary.csv"
    if base.exists():
        files.append(base)
    files += sorted(p for p in (ROOT / "cv_runs").glob("**/*.csv"))
    if not files:
        raise SystemExit("no input CSVs found")

    frames = [_read(p) for p in files]
    for p, f in zip(files, frames):
        print(f"  read {len(f):5d} rows  {f['_source'].iloc[0] if len(f) else p}")
    df = pd.concat(frames, ignore_index=True)
    n_in = len(df)

    for c in KEY + ["timestamp", "git_sha"]:
        if c not in df.columns:
            df[c] = ""
    df["target"] = df["target"].replace("", "feed")   # pre---target legacy rows were feed-only
    df["preproc"] = df["preproc"].replace("", "none")  # pre---preproc rows used raw PNGs

    n_inferred = 0
    if args.infer_legacy_lr:
        legacy = (df["lr"] == "") & (df["seed"] == "42")
        okey = [k for k in KEY if k != "lr"]
        for _, idx in df[legacy].groupby(okey, sort=False).groups.items():
            for rank, i in enumerate(list(idx)[:2]):
                df.at[i, "lr"] = "0.001" if rank == 0 else "0.0001"
                n_inferred += 1

    # normalise numeric spellings so 1e-3 / 0.001 and 42 / 42.0 collide
    def _num(x):
        try:
            return repr(float(x))
        except (TypeError, ValueError):
            return x
    df["lr"] = df["lr"].map(_num)
    df["seed"] = df["seed"].map(lambda x: str(int(float(x))) if x != "" else x)

    df["_order"] = range(len(df))
    out = (df.sort_values(["timestamp", "_order"], kind="stable")
             .drop_duplicates(KEY, keep="last")
             .sort_values("_order"))
    n_dup = n_in - len(out)
    out = out.drop(columns=["_order", "_source"])
    out_path = ROOT / args.out
    if out_path.name == "cv_summary.csv":
        raise SystemExit("refusing to overwrite cv_summary.csv")
    out.to_csv(out_path, index=False)

    print(f"\ninput rows: {n_in} from {len(files)} file(s)")
    print(f"duplicates dropped: {n_dup}")
    print(f"legacy lr inferred: {n_inferred}")
    print(f"blank lr remaining: {(out['lr'] == '').sum()}")
    print(f"wrote {len(out)} rows -> {out_path.name}")


if __name__ == "__main__":
    main()
