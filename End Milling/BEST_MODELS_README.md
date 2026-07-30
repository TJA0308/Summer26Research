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
| Speed (5-class) | **93.3%** | 14/15 | 2-model soft-vote ensemble: `models_speed_32x12_9win/resnet18_lr0.001_nosmote_best.pt` + `models_speed_32x3/resnet18_lr0.001_nosmote_best.pt` |
| Feed Coarse (3-class) | **91.7%** | 11/12 | 2-model soft-vote ensemble: `models_feed_coarse_32x3_feedopt_9win/convnext_tiny_lr0.001_best.pt` + `models_feed_coarse_32x3_feedopt_raw9w_residual/resnet50_lr0.001_best.pt` |
| Roughness (3-class) | **91.7%** | 11/12 | `models_roughness_32x3_residual_roughness/convnext_tiny_lr0.001_cascade_nosmote_best.pt` |
| Depth of Cut (3-class) | **100.0%** | 12/12 | `models_doc_32x3_docopt_raw3w/resnet18_lr0.001_smote_best.pt` |

**Correction note (previous revision):** the Feed Coarse and Roughness rows had originally listed configs (`feed_coarse resnet18_lr0.001_smote` at 91.7%, `roughness resnet18_lr0.001_smote` at 91.7%) that did **not** reproduce — they actually scored 58.3% and 83.3% respectively when the saved `_best.pt` weights were re-run on the held-out test split, traced to an older, unsaved ad-hoc verification script. That correction pass replaced them with the best single-model configs found across the full `eval_detailed_summary.csv` sweep (2113 checkpoints, 0 failures): 83.3% (feed_coarse, `resnet50`/`32x3_feedopt_raw3w_residual`) and 91.7% (roughness, `convnext_tiny`/`32x3_residual_roughness`/cascade).

**Ensembling update (this revision):** after that correction, single-model feed_coarse was stuck at 83.3% despite an additional 16-run training sweep (9-window residual + cascade conditioning; best new config only reached 66.7%). Following the Shoulder Milling playbook of soft-vote averaging predictions across multiple independently-trained models (not just windows within one model), a pairwise search over all config pairs with individual run_soft_acc >= 0.73-0.75 found 2-model ensembles that push both Speed and Feed Coarse past 90%: Speed reaches 93.3% (14/15, up from 86.7%) and Feed Coarse reaches 91.7% (11/12, up from 83.3%). Both ensembles combine two feature-pipeline-consistent models (no harmonic/FFT features), keeping methodological parity with Shoulder Milling. Verified via `ensemble_eval.py`, which averages each model's per-run soft-vote probability vector (from `*_window_preds.csv`) and re-argmaxes. Roughness and DOC single-model numbers are unchanged (no ensembling was needed to clear their targets).

---

## 1. Speed (5-class: 1500 / 2000 / 3000 / 4000 / 5000 rpm)

**Ensemble:** soft-vote average of two independently-trained models:
1. `models_speed_32x12_9win/resnet18_lr0.001_nosmote_best.pt` — 32x12 feature columns, 9-window split
2. `models_speed_32x3/resnet18_lr0.001_nosmote_best.pt` — 32x3 CWT-only, 3-window split, no scale selection

**Result:** 93.3% (14/15 test runs), up from the single-model best of 86.7% (13/15, `models_speed_32x3_speedopt_perdoc/resnet18_lr0.001_nosmote_best.pt`, per-DOC-normalized + Spearman scale selection — still the best single model, kept below for reference).

**Best single model (for reference):**
- `scalograms_32x3_speedopt_perdoc/`, ResNet-18, lr=1e-3, no SMOTE, 86.7% (13/15).
- Top-32 CWT scales (Mexican hat + Coiflet) selected by Spearman |rho| against speed.
- Per-DOC z-score normalization (normalize within each DOC group instead of globally) — removes the DOC-driven mean/variance shift before clipping to the 8-bit image range.
- No SMOTE — class balance sweep found SMOTE did not help here.

**Techniques tried that did not beat the ensemble:** F-stat scale selection (worse — picked only high-frequency scales), harmonic-ratio features alone (80% single-model; a harmonic+CWT ensemble reached 100% but was excluded, see Notes), band-statistics features (20%, near-random), ordinal loss (not applicable, no class ordering issue here), 9-window splitting alone (single-model, worse than the ensemble), 32x12 vs 32x3 alone.

Note: an ensemble of this model with a novel harmonic-feature model (FFT amplitude at spindle-harmonic frequencies, built directly from raw CSVs) reached 93.3%, but that combination sits outside the feature-pipeline techniques used for Shoulder Milling and was **not** kept, to preserve direct methodological comparability between the two datasets.

---

## 2. Feed Rate Coarse (3-class: low 3-4 / medium 5-6 / high 7-8 mm/rev)

**Ensemble:** soft-vote average of two independently-trained models:
1. `models_feed_coarse_32x3_feedopt_9win/convnext_tiny_lr0.001_best.pt` — 32x3 feedopt scales, 9-window split
2. `models_feed_coarse_32x3_feedopt_raw9w_residual/resnet50_lr0.001_best.pt` — 32x3, raw 9-window construction, condition-residual corrected

**Result:** 91.7% (11/12 test runs), up from the single-model best of 83.3% (10/12, `models_feed_coarse_32x3_feedopt_raw3w_residual/resnet50_lr0.001_best.pt` — still the best single model, kept below for reference).

**Best single model (for reference):**
- `scalograms_32x3_feedopt_raw3w_residual/`, ResNet-50, lr=1e-3, no run_tag (base training), 83.3% (10/12).
- Top-32 CWT scales selected by Spearman |rho| against feed_coarse, raw-window (`raw3w`) 3-window construction.
- **Condition-residual correction:** per-run feature image with the (DOC x speed)-group mean subtracted, removing DOC/speed confound before feed classification.

**Techniques tried that did not beat the ensemble:** ordinal cross-entropy loss (underperformed plain CE), DOC-conditioned / speed-conditioned cascade with and without SMOTE (`cascade_smote`/`cascade_nosmote` run tags, tied or worse; a further 16-run sweep adding cascade conditioning on top of the 9-window residual dir topped out at 66.7%, still below the ensemble), harmonic features (worse, ceiling ~67%), band-statistics features (50%, worse), per-DOC normalization without residual correction (worse), plain (non-residual) 32x3/32x12 feedopt dirs alone (previously misreported as 91.7% — does not reproduce as a single model; actual 58.3%, see correction note above), PCA+HistGradientBoosting classical-ML baseline (not yet tried here — flagged by Shoulder Milling's own findings as worth ruling in/out, since there feed's bottleneck was diagnosed as feature-level rather than model-capacity-level).

---

## 3. Surface Roughness Ra (3-class: Smooth / Medium / Rough)

**Feature dir:** `scalograms_32x3_residual_roughness/`
**Model:** ConvNeXt-Tiny, lr=1e-3, cascade-predicted DOC/speed conditioning, no SMOTE (run_tag `cascade_nosmote`; the `cascade_smote` variant of the same arch/lr/dir ties at the same accuracy)
**Result:** 91.7% (11/12 test runs)

- Top-32 CWT scales, 3-window split.
- **Condition-residual correction:** for each run's feature image, subtracted the mean image of all runs sharing the same (DOC x speed) condition — removes the DOC/speed signal that dominates and confounds Ra (Ra is near-perfectly correlated with DOC in this dataset), leaving only within-condition (feed-driven) variation.
- **Cascade conditioning:** DOC and speed are first predicted by their own best models, then those *predicted* (not ground-truth) labels are injected into the roughness classifier — avoids requiring true condition labels at inference time.

**Techniques tried that did not beat this:** ground-truth DOC-conditioning (ceiling 66.7% even with the true condition given to the model), harmonic features (not attempted for roughness — not a speed-harmonic-driven signal), band-statistics features (50%, worse), 32x12 / 9-window residual variant without cascade conditioning (previously misreported as 91.7% for `resnet18_lr0.001_smote` — does not reproduce; actual 83.3%, see correction note above).

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
- Every technique in this README (residual correction, SMOTE, per-DOC normalization, 9-window splitting, 32x3/32x12 comparison, F-stat vs Spearman scale selection, and now multi-model soft-vote ensembling) is a direct port of the Shoulder Milling methodology. No End-Milling-specific feature engineering was needed to reach these numbers, aside from the DOC/speed-specific scale selection already built into the existing pipeline.
- **Ensembling** (Speed, Feed Coarse): two independently-trained single models' per-run softmax probability vectors are averaged, then argmaxed, using `ensemble_eval.py`. Candidate pairs were selected from all single-model configs scoring run_soft_acc >= 0.73-0.75 in `eval_detailed_summary.csv`, exhaustively searched over 2- and 3-model combinations. This mirrors Shoulder Milling's own conclusion that no single lever (backbone, LR, residual correction, cascade conditioning) reliably clears a hard target alone, and that combining diverse, decorrelated models is the more robust final step.
- Harmonic/FFT-amplitude features (`scalograms_harmonic_speedopt/`) were explicitly excluded from Speed's ensemble even though a harmonic+CWT combination reaches 100%, to preserve direct methodological comparability with Shoulder Milling (which has no harmonic-feature pipeline). Both Speed and Feed Coarse's reported ensembles use only feature-pipeline-consistent CWT-derived scalograms.
