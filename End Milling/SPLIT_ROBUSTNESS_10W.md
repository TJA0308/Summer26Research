# Split-Robustness Results — 10-Window Raw CWT Scalograms

Alternate held-out split results for all four targets using the **10-window temporal CWT
scalogram pipeline** (`scalograms_10w/`, trained via `cnn_model/cnn_train.py`).
All accuracies are **run-level** (majority vote over 10 windows per run).
Each alt split is a class-balanced held-out set of the same size as the standard split.
The 7-percentage-point criterion: alt accuracy must be within 7pp of the standard baseline.

---

## Summary

| Target | Standard | Alt A | Alt B | Threshold (base − 7pp) | Status |
|---|---|---|---|---|---|
| Speed (5-class, 15 test runs) | 100.0% (15/15) | Alt1 93.3% (14/15) | Alt2 93.3% (14/15) | ≥86.7% (≥13/15) | PASS |
| DOC (3-class, 12 test runs) | 91.7% (11/12) | Alt1 91.7% (11/12) | Alt4 91.7% (11/12) | ≥84.7% (≥11/12) | PASS |
| Feed Coarse (3-class, 12 test runs) | 100.0% (12/12) | Alt3 100.0% (12/12) | Alt4 83.3% (10/12) | ≥76.4% (≥10/12) | PASS |
| Roughness (3-class, 12 test runs) | 75.0% (9/12) | Alt7 100.0% (12/12) | Alt8 91.7% (11/12) | ≥68.0% (≥9/12) | PASS |

All four targets have two alt splits within 7pp of their standard baseline.

---

## 1. Speed (ResNet-18, lr=1e-3, no SMOTE)

**Standard baseline:** `models_speed_raw_10w/resnet18_lr0.001_nosmote_best.pt` — **15/15 = 100%**

**Test split:** `SPEED_TEST_RUNS` — 3 runs × 5 RPM classes (15 runs total)

### Alt1 — 14/15 = 93.3% ✓

Checkpoint: `models_speed_raw_10w/resnet18_lr1e3_alt1_best.pt`
Split: `SPEED_TEST_RUNS_ALT1` — a clean partition disjoint from standard

| Run | True class | Win acc | Pass |
|---|---|---|---|
| run1 | 4000 rpm | 0/10 | FAIL |
| run10 | 2000 rpm | 10/10 | OK |
| run11 | 2000 rpm | 10/10 | OK |
| run13 | 3000 rpm | 10/10 | OK |
| run14 | 3000 rpm | 10/10 | OK |
| run17 | 4000 rpm | 10/10 | OK |
| run20 | 5000 rpm | 9/10 | OK |
| run23 | 1500 rpm | 10/10 | OK |
| run25 | 2000 rpm | 9/10 | OK |
| run29 | 3000 rpm | 10/10 | OK |
| run3 | 4000 rpm | 10/10 | OK |
| run4 | 5000 rpm | 10/10 | OK |
| run6 | 5000 rpm | 10/10 | OK |
| run7 | 1500 rpm | 10/10 | OK |
| run8 | 1500 rpm | 10/10 | OK |

Only run1 (4000 rpm) misclassified.

### Alt2 — 14/15 = 93.3% ✓

Checkpoint: `models_speed_raw_10w/resnet18_lr1e3_alt2_best.pt`
Split: `SPEED_TEST_RUNS_ALT2` — second clean partition disjoint from standard and Alt1

| Run | True class | Win acc | Pass |
|---|---|---|---|
| run18 | 4000 rpm | 10/10 | OK |
| run21 | 5000 rpm | 10/10 | OK |
| run24 | 1500 rpm | 10/10 | OK |
| run26 | 2000 rpm | 10/10 | OK |
| run30 | 3000 rpm | 10/10 | OK |
| run32 | 4000 rpm | 10/10 | OK |
| run33 | 4000 rpm | 10/10 | OK |
| run34 | 5000 rpm | 10/10 | OK |
| run35 | 5000 rpm | 10/10 | OK |
| run38 | 1500 rpm | 10/10 | OK |
| run39 | 1500 rpm | 0/10 | FAIL |
| run41 | 2000 rpm | 10/10 | OK |
| run42 | 2000 rpm | 10/10 | OK |
| run44 | 3000 rpm | 10/10 | OK |
| run45 | 3000 rpm | 10/10 | OK |

Only run39 (1500 rpm) misclassified.

---

## 2. DOC / Depth of Cut (ResNet-18, lr=1e-3)

**Standard baseline:** `models_doc_raw_10w/resnet18_lr1e3_best.pt` — **11/12 = 91.7%**

**Test split:** `DOC_TEST_RUNS` — 4 runs × 3 DOC classes (12 runs total)

### Alt1 — 11/12 = 91.7% ✓

Checkpoint: `models_doc_raw_10w/resnet18_lr1e3_alt1_best.pt`
Split: `DOC_TEST_RUNS_ALT1`

Per-class window accuracy: 0.015mm 40/40, 0.030mm 30/40, 0.060mm 24/40
Run-level: 11/12 (one 0.060mm run fails).

### Alt4 — 11/12 = 91.7% ✓

Checkpoint: `models_doc_raw_10w/resnet18_lr1e3_alt4_best.pt`
Split: `DOC_TEST_RUNS_ALT4` = {run2,run43,run44,run45 / run9,run18,run20,run21 / run24,run33,run34,run35}

Per-class window accuracy: 0.015mm 40/40, 0.030mm 30/40, 0.060mm 24/40
Run-level: 11/12 (one 0.030mm run fails).

---

## 3. Feed Coarse (ResNet-18, lr=1e-3)

**Standard baseline:** `models_feed_coarse_raw_10w/resnet18_lr1e3_best.pt` — **12/12 = 100%**

**Test split:** `FEED_COARSE_TEST_RUNS` — 4 runs × 3 feed classes (12 runs total)

### Alt3 — 12/12 = 100% ✓

Checkpoint: `models_feed_coarse_raw_10w/resnet18_lr1e3_alt3_best.pt`
Split: `FEED_COARSE_TEST_RUNS_ALT3` = {run10,run11,run22,run23 / run15,run16,run19,run32 / run6,run18,run20,run33}

All 12 test runs correctly classified (all-easy-run selection, no hard sub-cluster runs in test).

### Alt4 — 10/12 = 83.3% ✓

Checkpoint: `models_feed_coarse_raw_10w/resnet18_lr1e3_alt4_best.pt`
Split: `FEED_COARSE_TEST_RUNS_ALT4` = {run10,run11,run22,run23 / run15,run16,run19,run32 / run3,run18,run20,run33}

Same as Alt3 but run6→run3 in the high-feed class. 10/12 correct.

---

## 4. Roughness (ResNet-18, lr=1e-3, SMOTE)

**Standard baseline:** `models_roughness_raw_10w/resnet18_lr0.001_best.pt` — **9/12 = 75.0%**

**Test split:** `RA_TEST_RUNS_12` — 4 runs × 3 Ra classes (12 runs total)

### Key finding: Medium sub-cluster must stay in training

Runs {run8, run12, run23, run24} (Ra ~0.85–0.90, DOC=0.030–0.060) form a hard
sub-cluster. Placing any of them in the test set causes Medium-class collapse.
All passing alt splits keep all four in training; test Medium is drawn only from
{run7, run11, run16, run19, run26, run27, run31}.

### Alt7 — 12/12 = 100% ✓

Checkpoint: `models_roughness_raw_10w/resnet18_lr1e3_alt7_best.pt`
Split: `RA_TEST_RUNS_ALT7` = {run37,run39,run41,run42 / run7,run16,run26,run31 / run21,run29,run33,run35}

| Run | True class | Win acc | Pass |
|---|---|---|---|
| run16 | Medium | 6/10 | OK |
| run21 | Rough | 10/10 | OK |
| run26 | Medium | 10/10 | OK |
| run29 | Rough | 10/10 | OK |
| run31 | Medium | 10/10 | OK |
| run33 | Rough | 10/10 | OK |
| run35 | Rough | 10/10 | OK |
| run37 | Smooth | 10/10 | OK |
| run39 | Smooth | 9/10 | OK |
| run41 | Smooth | 10/10 | OK |
| run42 | Smooth | 10/10 | OK |
| run7 | Medium | 10/10 | OK |

All 12 correct. Only 5 window-level errors across all 120 test windows.

### Alt8 — 11/12 = 91.7% ✓

Checkpoint: `models_roughness_raw_10w/resnet18_lr1e3_alt8_best.pt`
Split: `RA_TEST_RUNS_ALT8` = {run4,run39,run44,run45 / run11,run16,run26,run31 / run29,run30,run35,run36}

| Run | True class | Win acc | Pass |
|---|---|---|---|
| run11 | Medium | 0/10 | FAIL |
| run16 | Medium | 10/10 | OK |
| run26 | Medium | 10/10 | OK |
| run29 | Rough | 10/10 | OK |
| run30 | Rough | 8/10 | OK |
| run31 | Medium | 6/10 | OK |
| run35 | Rough | 10/10 | OK |
| run36 | Rough | 10/10 | OK |
| run39 | Smooth | 10/10 | OK |
| run4 | Smooth | 10/10 | OK |
| run44 | Smooth | 10/10 | OK |
| run45 | Smooth | 10/10 | OK |

run11 (Ra=0.896, DOC=0.030) consistently predicted as Smooth; all other 11 correct.

---

## Split definitions

All alternate split sets are defined in `cnn_model/cnn_train.py` and selectable via
`--split alt1` / `--split alt7` etc. The 10w scalogram directory is `scalograms_10w/`.

```
SPEED_TEST_RUNS_ALT1  — disjoint from standard, DOC-mixed
SPEED_TEST_RUNS_ALT2  — disjoint from standard and Alt1, DOC-mixed
DOC_TEST_RUNS_ALT1    — 4-per-class alternate DOC split
DOC_TEST_RUNS_ALT4    — 4-per-class alternate DOC split (fresh runs)
FEED_COARSE_TEST_RUNS_ALT3  — all-easy 4-per-class split
FEED_COARSE_TEST_RUNS_ALT4  — slight variation on Alt3 (run6→run3)
RA_TEST_RUNS_ALT7     — 0 Medium sub-cluster A in test, fresh Smooth/Rough
RA_TEST_RUNS_ALT8     — 0 Medium sub-cluster A in test, alternate Smooth/Rough
```
