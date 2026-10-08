"""Check which lr=1e-4 seed-42 LOCO resnet18 rows are already in cv_summary.csv.

Hypothesis: older lr=1e-4 rows have a blank `lr`; for each (target, group,
scalogram) the 2nd blank-lr seed-42 loco cnn/resnet18 row in file order is the
lr=1e-4 run. Rows with an explicit lr=1e-4 are used directly.
Compares to section 4 of LOCO_CV_RESULTS.md. Read-only. Exit 0 always;
prints MISSING_CELLS list (also usable by gpu_jobs).
"""
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DOC = ROOT / "LOCO_CV_RESULTS.md"
CSV = ROOT / "cv_summary.csv"
TOL = 0.0006  # doc rounds to 0.1 pp
SECTION_TO_CELL = {"Speed": ("speed", "primary"), "DOC": ("doc", "primary"),
                   "Feed": ("feed", "primary"), "Roughness (primary)": ("roughness", "primary")}


def parse_doc():
    txt = DOC.read_text(encoding="utf-8")
    sec4 = re.search(r"^## 4\..*?(?=^## 5\.)", txt, re.S | re.M).group(0)
    out = {}
    for m in re.finditer(r"^### (.+?)\n(.*?)(?=^### |\Z)", sec4, re.S | re.M):
        name = m.group(1).strip()
        if name not in SECTION_TO_CELL:
            continue
        tgt, grp = SECTION_TO_CELL[name]
        for row in re.finditer(r"^\|\s*(32x\S+)\s*\|\s*([\d.]+)%\s*\|\s*([\d.]+)%", m.group(2), re.M):
            out[(tgt, grp, row.group(1))] = (float(row.group(2)) / 100, float(row.group(3)) / 100)
    return out


def main():
    doc = parse_doc()
    d = pd.read_csv(CSV)
    d = d[(d.model == "cnn") & (d.seed == 42) & (d.split == "loco") & (d.arch == "resnet18")]
    d = d[d.target.notna()]
    rows = []
    # secondary roughness: same scalograms as primary roughness, no doc table
    cells = [(t, g, s, doc[(t, g, s)]) for (t, g, s) in doc]
    cells += [("roughness", "secondary", s, None) for (t, g, s) in doc if t == "roughness"]
    for t, g, s, dv in cells:
        sub = d[(d.target == t) & (d.group == g) & (d.scalogram == s)]
        blank = sub[sub.lr.isna()].run_acc_soft.tolist()
        expl = sub[sub.lr == 1e-4].run_acc_soft.tolist()
        first = blank[0] if blank else None
        second = expl[0] if expl else (blank[1] if len(blank) > 1 else None)
        src = "explicit" if expl else ("blank#2" if len(blank) > 1 else "none")
        if dv is None:
            flag = "NO-1E-3-ROW" if first is None else ("NO-DOC" if second is not None else "MISSING")
        else:
            ok3 = first is not None and abs(first - dv[0]) < TOL
            ok4 = second is not None and abs(second - dv[1]) < TOL
            flag = "MATCH" if ok3 and ok4 else ("MISSING" if second is None else "MISMATCH")
        rows.append((f"{t}/{g}/{s}", dv[0] if dv else None, dv[1] if dv else None, first, second, src, flag))
    f = lambda x: "  -   " if x is None else f"{x:.4f}"
    print(f"{'cell':46s} {'doc1e-3':>7s} {'doc1e-4':>7s} {'csv1st':>7s} {'csv2nd':>7s} {'2nd-src':>8s} flag")
    for c, a, b, x, y, src, fl in rows:
        print(f"{c:46s} {f(a):>7s} {f(b):>7s} {f(x):>7s} {f(y):>7s} {src:>8s} {fl}")
    prim = [r for r in rows if r[6] not in ("NO-DOC", "NO-1E-3-ROW")]
    n_match = sum(r[6] == "MATCH" for r in prim)
    print(f"\nDoc-compared cells: {len(prim)}; MATCH: {n_match}")
    print("Roughness secondary (no doc table): " +
          ", ".join(f"{r[0].split('/')[-1]}={r[6]}" for r in rows if "/secondary/" in r[0]))
    bad = [r[0] for r in rows if r[6] in ("MISMATCH", "MISSING", "NO-1E-3-ROW")]
    print("MISSING_CELLS:", bad if bad else "none")


if __name__ == "__main__":
    main()
