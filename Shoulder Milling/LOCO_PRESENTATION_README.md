# Shoulder Milling — LOCO Cross-Validation: Results Summary

Status as of 2026-10-05. Full tables and every variant live in `LOCO_CV_RESULTS.md`;
raw rows in `cv_summary.csv`. Everything below is **Leave-One-Condition-Out (LOCO)**,
ResNet-18 fine-tuned from ImageNet, 50 epochs, **final-epoch weights only**,
run-level soft vote, exact Clopper-Pearson 95% CIs over **24 runs**.

## TL;DR

- We built a leak-audited LOCO protocol for a 24-run factorial milling dataset and used it to
  test whether CWT+CNN models generalize to **unseen cutting conditions**.
- **Best model per target** (LOCO, seed 42, one config chosen out of 16 scalogram variants):
  Speed **100%**, DOC **95.8%**, Feed **87.5%**, Roughness **75.0%**.
- These are **peak** numbers. They are optimistic: the winner was picked among 16 variants on the
  same 24 runs, from a single seed, and three of the four winners use preprocessing that saw all
  24 runs (details in "How to read these numbers"). Always show them with the baseline column.
- The robust, defensible takeaway: **speed generalizes under LOCO; DOC partly; feed weakly;
  roughness is not yet shown.**

## 1. What LOCO tests

24 runs = 2 speeds x 3 feeds x 2 depths of cut x 2 sides, 3 time windows each. A random split
lets a model memorize run-specific noise. LOCO holds out every run that shares a combination of
the *other* designed factors, so the held-out runs are the only place the target factor varies.

| Target | Held out per fold | Folds | Runs/fold | Chance |
|---|---|---|---|---|
| Speed | depth-of-cut (y x z) | 4 | 6 | 50.0% |
| Feed | speed x doc | 8 | 3 | 33.3% |
| DOC | speed x feed | 6 | 4 | 25.0% |
| Roughness (primary) | doc (y x z) | 4 | 6 | 50.0% |

Anti-leakage rules: final-epoch model only (no test-accuracy checkpoint choice), no SMOTE, no
cascade conditioning, headline metric = run-level soft vote, CI = Clopper-Pearson over 24 runs.

## 2. Evaluation bugs this protocol caught

| Finding | Evidence |
|---|---|
| **Checkpoint selection on test accuracy** inflated every old headline | Mean **14.65 pp** over 383 logged runs (70.1% -> 55.4%, window-level, fixed split); `corrected_standard_split_window_acc.csv` |
| **Roughness grouped by speed x feed leaks doc** | A zero-image doc lookup scores **62.5%** with no vibration input; roughness is now grouped by doc (primary) |
| **Roughness chance mislabelled as 25%** | It is a balanced 2-class target: true chance is **50%** (commit `517fb8b5`) |
| **Residualized variants are transductive** | Each residual group lies inside one LOCO test fold, so test images are centred on their own fold mean |

## 3. Best model per target (LOCO, seed 42, lr = 1e-3)

| Target | Chance | Best configuration | Accuracy | 95% CI | Best **without** residual preprocessing |
|---|---|---|---|---|---|
| Speed | 50% | `32x12_9win` (tied with `32x12_residual_speed`) | **100.0%** | [85.8, 100] | same, 100.0% |
| DOC | 25% | `32x12_residual_doc` | **95.8%** | [78.9, 99.9] | `32x3_feedopt_9win` 91.7% [73.0, 99.0] |
| Feed | 33.3% | `32x3_residual_roughness` | **87.5%** | [67.6, 97.3] | `32x3_9win` 66.7% [44.7, 84.4] |
| Roughness | 50% | `32x12_feedopt_9win` | **75.0%** | [53.3, 90.2] | same, 75.0% |

Best scalogram per target (image directories): `scalograms_32x12_9win`,
`scalograms_32x12_residual_doc`, `scalograms_32x3_residual_roughness`,
`scalograms_32x12_feedopt_9win`.

## 4. How to read these numbers (put these caveats on the same slide)

1. **Best-of-16, single seed.** Each winner is the maximum over 16 variants, chosen on
   the same 24 runs it is scored on. The expected gap between a peak and its true performance is
   positive. With 24 runs the CI is roughly +/-20 pp.
2. **Residual winners (DOC 95.8%, Feed 87.5%) are transductive**, not clean generalization
   numbers: the model effectively sees a class-balanced test batch centred on its own mean.
   The "without residual" column is the fairer peak for those two targets.
3. **Row selection saw all 24 runs.** CWT rows for the `32x12`/`32x3` families (and feedopt) were
   chosen by Spearman correlation with Ra (base) or feed (feedopt) on all 24 runs before LOCO.
   For roughness this is direct label leakage, so 75.0% is the number most at risk.
   LOCO here cross-validates the classifier stage only, not the whole pipeline.
4. **Speed's 100% is not evidence that 9win helps**: plain `32x12` also scores 100% at seed 42.
5. **`9win` is a scale-band split** (3 contiguous scale-row bands per window), not extra time windows.

## 5. The generalization counterpart (always show next to the peaks)

Plain `32x12`, no variant selection. CNN = 5-seed mean +/- std (seeds 42-46); HGB = PCA(20) +
gradient boosting on pixels, seed 42, untuned.

| Target | Chance | Best-of-16 peak (seed 42) | CNN `32x12`, 5-seed mean | HGB `32x12` |
|---|---|---|---|---|
| Speed | 50% | 100.0% | 87.5 +/- 9.3% (range 75-100) | 91.7% |
| DOC | 25% | 95.8% | 60.0 +/- 3.7% | 83.3% |
| Feed | 33.3% | 87.5% | 55.0 +/- 1.9% | 62.5% |
| Roughness | 50% | 75.0% | 57.5 +/- 1.9% | 58.3% |

Honest reading: with 24 runs a low-capacity model matches or beats fine-tuned ResNet-18. Only the
DOC gap (HGB +23 pp) looks real, and there is no paired test yet. Speed is the one target that
clearly generalizes.

lr = 1e-3 beat lr = 1e-4 in 44 of 48 comparisons (2 ties, 2 for 1e-4). lr=1e-4 labels for 40 of
the 48 are inferred from row order in `cv_summary.csv`, not from an explicit column.

## 6. Precision / recall / F1

All values are **run-level** (soft vote over a run's windows), pooled over every LOCO held-out
fold, so each of the 24 runs is predicted exactly once. Macro = unweighted mean over classes.
Computed by `compute_prf1.py` from per-window predictions saved with `--save_preds`.

**Computed now (CPU): HGB baseline, plain `32x12`, LOCO, seed 42** (accuracy reproduces the
`cv_summary.csv` HGB rows exactly; full per-class tables + confusion matrices in `cv_preds/hgb_prf1.md`):

| Target | Accuracy | Macro-P | Macro-R | Macro-F1 | Per-class F1 |
|---|---|---|---|---|---|
| Speed (2 cls) | 0.917 | 0.929 | 0.917 | 0.916 | 0.923, 0.909 |
| DOC (4 cls) | 0.833 | 0.839 | 0.833 | 0.833 | 0.923, 0.667, 0.909, 0.833 |
| Feed (3 cls) | 0.625 | 0.617 | 0.625 | 0.615 | 0.750, 0.429, 0.667 |
| Roughness (2 cls) | 0.583 | 0.583 | 0.583 | 0.583 | 0.583, 0.583 |

Reading it: DOC class 1 (F1 0.667) and Feed class 1, the middle feed (F1 0.429), are the weak classes.
Roughness F1 equals accuracy because the two classes are balanced (12/12) and the errors are symmetric
(5 vs 5), i.e. no better than slightly above chance.

**Best CNN models: PENDING (needs the GPU).** `cv_evaluate.py` previously saved only accuracy,
not predictions, and there is no CUDA on this machine, so P/R/F1 for the CNN configs in section 3
cannot be derived from existing data. They require a re-run with predictions saved:

| Target | Configuration | Acc | Macro-P | Macro-R | Macro-F1 |
|---|---|---|---|---|---|
| Speed | `32x12_9win` | pending | pending | pending | pending |
| DOC | `32x12_residual_doc` (and `32x3_feedopt_9win`, non-residual) | pending | pending | pending | pending |
| Feed | `32x3_residual_roughness` (and `32x3_9win`, non-residual) | pending | pending | pending | pending |
| Roughness | `32x12_feedopt_9win` | pending | pending | pending | pending |

Run `gpu_jobs/D_prf1_best.ps1` (or `.sh`) on the GPU machine: it re-runs these configs at seed 42
plus the plain `32x12` baseline at seeds 42-46 (the generalization counterpart), then writes
`cv_preds/cnn_prf1.md`. A GPU re-run may not reproduce the seed-42 accuracies above bit-for-bit,
so quote the accuracy from the re-run next to its P/R/F1 and state any difference.

## 7. What is not done yet

- No multi-seed run of the winning configs (batch B), and no fold-nested preprocessing runs
  (batch C). Scripts are ready in `gpu_jobs/`; neither has been run.
- CNN precision/recall/F1 (batch D, section 6) is pending the same GPU machine.
- No leak-free version of the 9win variants (their image widths are ragged for `--preproc`).
- No paired test between HGB and the CNN, no permutation tests, no second dataset (End Milling)
  under the same protocol.
- Raw vibration signals and CWT code are not in the repo, only precomputed feature sheets.

## 8. Reproduce

```bash
python cv_evaluate.py --img_dir scalograms_32x12_9win --target speed \
    --models cnn --arch resnet18 --epochs 50 --seeds 42
python cv_evaluate.py --img_dir scalograms_32x12_residual_doc --target doc \
    --models cnn --arch resnet18 --epochs 50 --seeds 42
python cv_evaluate.py --img_dir scalograms_32x3_residual_roughness --target feed \
    --models cnn --arch resnet18 --epochs 50 --seeds 42
python cv_evaluate.py --img_dir scalograms_32x12_feedopt_9win --target roughness \
    --models cnn --arch resnet18 --epochs 50 --seeds 42

# Precision / recall / F1 from saved predictions
python cv_evaluate.py --img_dir scalograms_32x12 --target speed --models hgb --seeds 42 \
    --save_preds cv_preds/hgb --out_csv /tmp/hgb_speed.csv   # --out_csv keeps cv_summary.csv untouched
python compute_prf1.py "cv_preds/hgb/*.csv" --out_md cv_preds/hgb_prf1.md
```

GPU batches for the remaining work (incl. batch D for CNN P/R/F1): see `gpu_jobs/README.md`.
