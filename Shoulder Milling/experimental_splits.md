# Experimental Splits — Unified Test Sets

## Motivation

The original three splits (README.md "Three Model Splits") each use a different
set of 8 test runs, purpose-designed to isolate one process parameter. This makes
individual models well-evaluated but prevents direct cross-model comparison: when
speed uses different test runs than doc, a model that scores 8/8 on speed can't
be meaningfully compared to one that scores 8/8 on doc, because the difficulty
of the held-out conditions differs.

**Experimental splits exp11 and exp12 use the same 8 test runs for all four
targets simultaneously.** This enables apples-to-apples comparison across targets
on a shared held-out set, and gives a variance estimate on accuracy numbers when
compared against the original per-target results.

## Derivation

Starting from the 16 speed-split alternatives that share zero test runs with the
original speed split, only 2 also satisfy:
- All 3 feed rates represented in the test set (feed balance)
- Exactly 4 smooth / 4 rough runs in the test set (roughness balance)
- 4 runs per speed class and 2 runs per doc class (speed + doc balance)

Those 2 are exp11 and exp12. They differ only in which feed the group (7,8)
pair contributes to the test set.

## Split Definitions

Both splits follow the isolation-pair structure: for each doc group, one feed
is held out as test and the other two stay in training.

| Doc group | Sides | exp11 feed in test | exp12 feed in test |
|-----------|-------|--------------------|--------------------|
| Y50/Z250  | 1, 2  | f7                 | f7                 |
| Y25/Z250  | 3, 4  | f3                 | f3                 |
| Y50/Z125  | 5, 6  | f5                 | f5                 |
| Y25/Z125  | 7, 8  | **f5**             | **f7**             |

### exp11 — test runs

| Run            | Speed  | Y-doc | Z-doc | Feed | Ra   | Roughness |
|----------------|--------|-------|-------|------|------|-----------|
| s25f7y5z25     | 2500   | 0.50  | 0.250 | f7   | 0.92 | rough     |
| s35f7y5z25     | 3500   | 0.50  | 0.250 | f7   | 0.32 | smooth    |
| s25f3y25z25    | 2500   | 0.25  | 0.250 | f3   | 0.50 | rough     |
| s35f3y25z25    | 3500   | 0.25  | 0.250 | f3   | 0.42 | rough     |
| s25f5y5z125    | 2500   | 0.50  | 0.125 | f5   | 0.18 | smooth    |
| s35f5y5z125    | 3500   | 0.50  | 0.125 | f5   | 0.28 | smooth    |
| s25f5y25z125   | 2500   | 0.25  | 0.125 | f5   | 0.28 | smooth    |
| s35f5y25z125   | 3500   | 0.25  | 0.125 | f5   | 0.44 | rough     |

**exp11 train runs (16):** s25f3y5z25, s25f5y5z25, s35f3y5z25, s35f5y5z25,
s25f5y25z25, s25f7y25z25, s35f5y25z25, s35f7y25z25,
s25f3y5z125, s25f7y5z125, s35f3y5z125, s35f7y5z125,
s25f3y25z125, s25f7y25z125, s35f3y25z125, s35f7y25z125

### exp12 — test runs

| Run            | Speed  | Y-doc | Z-doc | Feed | Ra   | Roughness |
|----------------|--------|-------|-------|------|------|-----------|
| s25f7y5z25     | 2500   | 0.50  | 0.250 | f7   | 0.92 | rough     |
| s35f7y5z25     | 3500   | 0.50  | 0.250 | f7   | 0.32 | smooth    |
| s25f3y25z25    | 2500   | 0.25  | 0.250 | f3   | 0.50 | rough     |
| s35f3y25z25    | 3500   | 0.25  | 0.250 | f3   | 0.42 | rough     |
| s25f5y5z125    | 2500   | 0.50  | 0.125 | f5   | 0.18 | smooth    |
| s35f5y5z125    | 3500   | 0.50  | 0.125 | f5   | 0.28 | smooth    |
| s25f7y25z125   | 2500   | 0.25  | 0.125 | f7   | 0.22 | smooth    |
| s35f7y25z125   | 3500   | 0.25  | 0.125 | f7   | 0.42 | rough     |

**exp12 train runs (16):** s25f3y5z25, s25f5y5z25, s35f3y5z25, s35f5y5z25,
s25f5y25z25, s25f7y25z25, s35f5y25z25, s35f7y25z25,
s25f3y5z125, s25f7y5z125, s35f3y5z125, s35f7y5z125,
s25f3y25z125, s25f5y25z125, s35f3y25z125, s35f5y25z125

## Balance Summary

All figures at the run level (8 test runs, 16 train runs).

| Dimension           | exp11 test    | exp12 test    | Original splits   |
|---------------------|---------------|---------------|-------------------|
| Speed 2500 / 3500   | 4 / 4         | 4 / 4         | 4 / 4 (all)       |
| Y-doc 0.25 / 0.50   | 4 / 4         | 4 / 4         | 4 / 4 (all)       |
| Z-doc 0.125 / 0.250 | 4 / 4         | 4 / 4         | 4 / 4 (all)       |
| Feed f3 / f5 / f7   | 2 / 4 / 2     | 2 / 2 / 4     | varies by target  |
| Roughness S / R     | 4 / 4         | 4 / 4         | 4 / 4 (doc split) |
| Doc classes (4)     | 2 / 2 / 2 / 2 | 2 / 2 / 2 / 2 | 2 ea. (doc split) |

Feed balance note: perfect 3-class balance with 8 test runs is impossible (8/3
is not an integer). Both splits have one feed appearing twice and the others once,
the best achievable. The two splits complement each other — exp11 tests f5 more
heavily, exp12 tests f7 more heavily.

## Overlap with Original Splits

| | vs original speed test | vs original doc/roughness test | vs original feed test |
|--|------------------------|--------------------------------|-----------------------|
| exp11 | **0 / 8** (disjoint) | 3 / 8 | 2 / 8 |
| exp12 | **0 / 8** (disjoint) | 2 / 8 | 2 / 8 |
| exp11 vs exp12 | — | — | 6 / 8 shared |

exp11 and exp12 differ by only 2 test runs (the group (7,8) pair: f5 in exp11,
f7 in exp12).

## Usage

Run everything with the provided script:

```powershell
.\run_exp_splits.ps1
```

Or individually:

```powershell
# 1. Generate SMOTE files for the experimental splits (run once per scalogram dir)
python smote_generate_param.py --split_id exp11
python smote_generate_param.py --split_id exp12

# 2. Train one model (no SMOTE)
python cnn_train_param.py --target speed --img_dir scalograms_32x12 `
    --arch resnet18 --lr 1e-3 --split_id exp11 --run_tag exp11

# 3. Train with SMOTE
python cnn_train_param.py --target speed --img_dir scalograms_32x12 `
    --arch resnet18 --lr 1e-3 --split_id exp11 --run_tag exp11_smote

# 4. Evaluate
python eval_detailed_param.py --target speed --img_dir scalograms_32x12 `
    --arch resnet18 --lr 1e-3 --split_id exp11 --run_tag exp11
```

Results land in `exp_results_32x12_exp11/` and `exp_results_32x12_exp12/`,
separate from the original `exp_results_32x12/`.
