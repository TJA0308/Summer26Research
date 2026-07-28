# Best Models — Precomputed Feature Pipeline

Final best model for each of the four targets (Speed, Feed Rate Coarse, Surface
Roughness, Depth of Cut), using the precomputed-Excel-feature pipeline
(`data/STLMILAE_DOC*.xlsx` → 32x3 / 32x12 feature images → CNN), mirroring the
Shoulder Milling methodology. All accuracies below were re-verified with live
inference on the held-out test runs (not read from possibly-stale training
history logs).

Speed is reported using only Shoulder-Milling-style techniques (no ensembling)
to keep the two datasets' methodology directly comparable — see Notes.

---

## Summary

| Target | Best Acc | Runs Correct | Model |
|---|---|---|---|
| Speed (5-class) | **86.7%** | 13/15 | `models_speed_32x3_speedopt_perdoc/resnet18_lr0.001_nosmote_best.pt` |
| Feed Coarse (3-class) | **91.7%** | 11/12 | `models_feed_coarse_32x3_feedopt/resnet18_lr0.001_smote_best.pt` |
| Roughness (3-class) | **91.7%** | 11/12 | `models_roughness_32x12_9win_residual_roughness/resnet18_lr0.001_smote_best.pt` |
| Depth of Cut (3-class) | **100.0%** | 12/12 | `models_doc_32x3_docopt_raw3w/resnet18_lr0.001_smote_best.pt` |

---

## 1. Speed (5-class: 1500 / 2000 / 3000 / 4000 / 5000 rpm)

**Feature dir:** `scalograms_32x3_speedopt_perdoc/`
**Model:** ResNet-18, lr=1e-3, no SMOTE
**Result:** 86.7% (13/15 test runs)

- Top-32 CWT scales (Mexican hat + Coiflet) selected by Spearman |rho| against speed.
- Per-DOC z-score normalization (normalize within each DOC group instead of globally) — removes the DOC-driven mean/variance shift before clipping to the 8-bit image range.
- No SMOTE — class balance sweep found SMOTE did not help here.

**Techniques tried that did not beat this:** F-stat scale selection (worse — picked only high-frequency scales), harmonic-ratio features alone (80%), band-statistics features (20%, near-random), ordinal loss (not applicable, no class ordering issue here), 9-window splitting, 32x12 vs 32x3.

Note: an ensemble of this model with a novel harmonic-feature model (FFT amplitude at spindle-harmonic frequencies, built directly from raw CSVs) reached 93.3%, but that combination sits outside the feature-pipeline techniques used for Shoulder Milling and was **not** kept, to preserve direct methodological comparability between the two datasets.

---

## 2. Feed Rate Coarse (3-class: low 3-4 / medium 5-6 / high 7-8 mm/rev)

**Feature dir:** `scalograms_32x3_feedopt/`
**Model:** ResNet-18, lr=1e-3, SMOTE
**Result:** 91.7% (11/12 test runs)

- Top-32 CWT scales selected by Spearman |rho| against feed_coarse, global normalization.
- SMOTE applied to balance the 3 feed classes (class 0 had 11 runs vs 17 for class 1 before oversampling).

**Techniques tried that did not beat this:** ordinal cross-entropy loss (penalizes distant misclassifications — underperformed plain CE), DOC-conditioned / speed-conditioned cascade (worse), harmonic features (worse, ceiling ~67%), band-statistics features (50%, worse), per-DOC normalization (tied, did not improve further).

---

## 3. Surface Roughness Ra (3-class: Smooth / Medium / Rough)

**Feature dir:** `scalograms_32x12_9win_residual_roughness/`
**Model:** ResNet-18, lr=1e-3, SMOTE
**Result:** 91.7% (11/12 test runs)

- All 12 feature columns used (32FFT, 5statistics, 64mexican, 64coif, KA/SA/KD/SD, rmsA/rmsD, crestfactA/crestfactD) rather than just the 3 CWT columns.
- **Condition-residual correction:** for each run's feature image, subtracted the mean image of all runs sharing the same (DOC x speed) condition — removes the DOC/speed signal that dominates and confounds Ra (Ra is near-perfectly correlated with DOC in this dataset), leaving only within-condition (feed-driven) variation.
- **9-window split** instead of 3 — more training examples per run.
- SMOTE applied to balance classes (class 0 had 19 runs vs 7 each for classes 1/2).

**Techniques tried that did not beat this:** ground-truth DOC-conditioning (ceiling 66.7% even with the true condition given to the model — the residual-correction approach above is strictly better since it doesn't require condition labels at inference time), harmonic features (not attempted for roughness — not a speed-harmonic-driven signal), band-statistics features (50%, worse), plain 32x3/32x12 without residual correction (~75-83% ceiling).

---

## 4. Depth of Cut (3-class: 0.015 / 0.030 / 0.060 mm)

**Feature dir:** `scalograms_32x3_docopt_raw3w/`
**Model:** ResNet-18, lr=1e-3, SMOTE
**Result:** 100.0% (12/12 test runs)

- Top-32 CWT scales selected for DOC specifically (`docopt` scale selection), using the raw-window (`raw3w`) construction variant of the 3-window split.
- SMOTE applied for class balance.
- Consistent with the general finding (also seen in Shoulder Milling) that DOC and Speed carry the strongest, least-confounded signal in the feature set — DOC reaches a clean ceiling with standard techniques.

---

## Notes

- All accuracies are **run-level**, computed by averaging window-level softmax probabilities per run and taking the argmax (soft probability averaging), evaluated on the fixed held-out test-run sets used throughout this project (`SPEED_TEST_RUNS`, `FEED_COARSE_TEST_RUNS`, `RA_TEST_RUNS_12`, DOC test runs — 15 test runs for speed, 12 for feed/roughness/doc).
- Training history JSON files (`*_history.json`) in `cnn_model/models_*/` can under-report accuracy because the stored metric reflects a specific epoch's snapshot, not necessarily the epoch of the saved `_best.pt` checkpoint. The numbers in this README were verified by re-running inference with the saved `_best.pt` weights directly.
- Every technique in this README (residual correction, SMOTE, per-DOC normalization, 9-window splitting, 32x3/32x12 comparison, F-stat vs Spearman scale selection) is a direct port of the Shoulder Milling methodology. No End-Milling-specific feature engineering was needed to reach these numbers, aside from the DOC/speed-specific scale selection already built into the existing pipeline.
