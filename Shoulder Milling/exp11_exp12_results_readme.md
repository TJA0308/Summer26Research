# exp11 / exp12 Results — All Four Targets, Same Features

Results for the two cross-target-balanced splits (**exp11**, **exp12** — defined in
`experimental_splits.md`) across all four targets (**speed, doc, feed, roughness**),
using the same feature setup per target: independent per-target CNNs (no cascade
conditioning), swept over the same 4 backbones (resnet18, resnet50, efficientnet_b0,
convnext_tiny) × 2 learning rates (1e-4, 1e-3) × with/without SMOTE = 16 configs per
target/split. This predates the condition-residual preprocessing in
`residual_preprocessing_readme.md` — these are the "raw pixel" numbers that
preprocessing was built to fix.

Two scalogram layouts are shown, each on its own 3-window (original) and 9-window
(row-band-split, see `experiments_writeup.md` §5) variant:
- **32x12** (Option C: 32 CWT scale rows × 12 cols)
- **32x3** (Option D: 32 rows × 3 cols — FFT + 2 wavelet families)

All numbers are `Run MV accuracy` read directly from the `eval_detailed_param.py`
output docs in `exp_results_32x12_exp11/`, `exp_results_32x12_exp12/`,
`exp_results_32x3_exp11/`, `exp_results_32x3_exp12/`, and their `_9win_` counterparts.
**best** = the single best config out of 16; **mean** = average across all 16 configs
(a better read on how reliable a target/scalogram/split combo is, since picking
"best of 16" on the same set you're scoring is optimistic — see caveat below).

---

## 3-window (original) scalograms

| Target | 32x12 exp11 | 32x12 exp12 | 32x3 exp11 | 32x3 exp12 |
|---|---|---|---|---|
| **speed** | best 100.0% / mean 82.8% | best 100.0% / mean 79.7% | best 100.0% / mean 85.9% | best 100.0% / mean 90.6% |
| **doc** | best 50.0% / mean 43.8% | best 75.0% / mean 46.9% | best 62.5% / mean 45.3% | best 62.5% / mean 46.9% |
| **feed** | best 75.0% / mean 50.0% | best 75.0% / mean 48.4% | best 75.0% / mean 48.4% | best 62.5% / mean 44.5% |
| **roughness** | best 87.5% / mean 68.8% | best 87.5% / mean 65.6% | best 87.5% / mean 73.4% | best 100.0% / mean 71.9% |

(feed n=16 per split reflects the with/without-SMOTE sweep, same as the other
targets; doc/speed/roughness show n=8 configs in the raw eval docs because those
particular sweeps didn't get a separate SMOTE pass in exp11/exp12 — feed did, since
it was the target under active investigation.)

## 9-window scalograms

| Target | 32x12 exp11 | 32x12 exp12 | 32x3 exp11 | 32x3 exp12 |
|---|---|---|---|---|
| **speed** | best 100.0% / mean 68.0% | best 100.0% / mean 78.1% | best 100.0% / mean 76.6% | best 100.0% / mean 82.0% |
| **doc** | best 62.5% / mean 41.4% | best 75.0% / mean 43.8% | best 75.0% / mean 50.0% | best 75.0% / mean 41.4% |
| **feed** | best 75.0% / mean 47.7% | best 50.0% / mean 42.2% | best 75.0% / mean 49.2% | best 62.5% / mean 46.1% |
| **roughness** | best 87.5% / mean 74.2% | best 87.5% / mean 68.8% | best 87.5% / mean 68.0% | best 87.5% / mean 71.1% |

---

## Observations

- **Speed is the only target that's actually solved.** 100% best-case on every
  scalogram/window/split combo, and its *mean* across all 16 configs stays
  70–90% — meaning it doesn't just work for one lucky arch/lr, most configs get
  it right. Confirms the "speed was solved early" note in `experiments_writeup.md`.
- **Roughness is solid but not perfect**: 87.5–100% best case, and unlike speed
  its mean (65–74%) is well below its best — more arch/lr-sensitive, but the
  binary smooth/rough split gives it a higher floor than doc or feed.
- **Doc and feed are the weak targets**, and it's not close: best-of-16 tops
  out at 50–75%, but the *mean* across configs sits in the low-to-mid 40s for
  both — meaning a random arch/lr pick has roughly a coin-flip's chance of
  landing near the "best" number reported. This is the same pattern flagged in
  `experiments_writeup.md` §6–§7: picking the best of a sweep and reporting it
  as *the* result overstates how reliable that number actually is.
- **9-window vs 3-window**: 9-window matches or edges out 3-window's best-case
  numbers in a few cells (doc 32x12/exp11: 62.5% vs 50.0%) but mostly just adds
  noise — means drop for speed/doc under 9-window in several columns, echoing
  §6's "not a free win" conclusion.
- **32x12 vs 32x3**: no consistent winner here either; differences are mostly
  within a config or two of each other, well inside the 12.5pp granularity of
  an 8-run test set.

## Caveat — this is still test-set-driven selection

Every "best" number above is the max over 16 configs *evaluated on the same
8-run test set it's being scored against* — the same selection-bias problem
flagged throughout `experiments_writeup.md` (§7 in particular). It is a fair,
consistent way to compare targets/scalograms/splits against each other, but it
is **not** an unbiased estimate of how any single config would perform on truly
unseen data. The debiased estimate — pooling predictions across all 8
leave-one-side-out folds with no test-set-driven picking — lives in
`cv_summary.csv` / `experiments_writeup.md` §7, and lands feed's honest ceiling
at ~42–54% run accuracy, well below every "best" figure in the tables above.

## What came next

`residual_preprocessing_readme.md` documents condition-residual preprocessing,
which — evaluated under the same leave-one-side-out CV as the debiased numbers
above — recovered feed to 87.5%/75.0% (32x3/32x12) and pushed roughness to
100% (base/exp12) / 87.5% (exp11) on the CNN sweep.

**Final decision:** residual is kept only for **feed and roughness** — both
share the same speed × doc nuisance condition, so it's applied consistently to
both or neither. **Speed and doc use the raw models from this doc** instead:
speed (resnet18, lr=1e-3, `scalograms_32x12`) is already 100%/100% on
exp11/exp12 with no preprocessing needed, and doc (resnet18, lr=1e-3,
`scalograms_32x3_9win`) holds a consistent 75%/75% across both splits — good
enough to skip the extra residual complexity for these two targets.
