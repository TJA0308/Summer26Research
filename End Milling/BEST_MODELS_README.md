# Best Models — Precomputed Feature Pipeline

Final best model for each of the four targets (Speed, Feed Rate Coarse, Surface
Roughness, Depth of Cut), using the precomputed-Excel-feature pipeline
(`data/STLMILAE_DOC*.xlsx` → 32x3 / 32x12 feature images → CNN), mirroring the
Shoulder Milling methodology. All accuracies below were re-verified with live
inference on the held-out test runs (not read from possibly-stale training
history logs).

**Full per-config precision/recall/F1** for every sweep config referenced across the
`Documentation/End Milling/` spreadsheets (not just the 4 final models below) is transcribed
from `eval_detailed_summary.csv`'s already-computed `precision_macro_soft/recall_macro_soft/
f1_macro_soft` (+`_hard`) columns into 4 appendices, one per Documentation spreadsheet:
`appendix_base_prf1.md` (48 configs), `appendix_smote_cascading_prf1.md` (156),
`appendix_residual_prf1.md` (688), `appendix_scale_selection_windowing_prf1.md` (1237).
Together with the 4 final models below, every row of `eval_detailed_summary.csv` except the
alt1/alt2 held-out-split experiment (documented separately) has precision/recall/F1 accounted
for.

Speed is reported using only Shoulder-Milling-style techniques (no ensembling)
to keep the two datasets' methodology directly comparable — see Notes.

**Read §5 before citing any of the four numbers in the table below**: none of
them survive retraining on alternate held-out splits — Speed 93.3%→46.7-73.3%
(6 alternates), Feed Coarse 91.7%→11.1-33.3% (4 alternates), DOC 100%→41.7-83.3%
(2 alternates), Roughness cascade 91.7%→33.3-66.7% (2 alternates, and its
upstream speed/doc submodels also collapse). Treat every figure below as
single-split, not generalizable, accuracy.

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

**IMPORTANT — split-robustness check (this revision, see §5 below):** the headline numbers above (Speed 93.3%, Feed Coarse 91.7%, Roughness 91.7%, DOC 100%) hold **only on the one fixed test-run split used throughout this project**. Retraining the same configs from scratch on alternate, equally class-balanced held-out splits collapses **all four targets**, not just the two ensembles:

| Target | Standard split | Alternates (accuracy) | Mean | Sample std |
|---|---|---|---|---|
| Speed ensemble | 93.3% (14/15) | Alt1 46.7%, Alt2 66.7%, Alt3 60.0%, Alt4 73.3%, Alt5 60.0%, Alt6 66.7% | 62.2% | 9.1pp |
| Feed Coarse ensemble | 91.7% (11/12) | Alt1 33.3%, Alt2 16.7%, Alt3 11.1% (1/9), Alt4 33.3% (3/9) | 23.6% | 11.4pp |
| DOC | 100.0% (12/12) | Alt1 83.3% (10/12), Alt2 41.7% majority / 50.0% soft (5–6/12) | 62.5% | — (n=2) |
| Roughness cascade | 91.7% (11/12) | Rough-Alt1 33.3%, Rough-Alt2 66.7% majority / 55.6% soft | 44.5–50.0% | — (n=2) |

Speed and Feed Coarse now each have 4-6 alternate splits (Speed's Alt5/Alt6 are a third DOC-balanced 3-way partition; Feed Coarse's Alt3/Alt4 are new). DOC and Roughness previously had **no** alt-split check at all — this revision adds the first ones for both. Roughness's cascade conditioning depends on predicted DOC/speed labels, so its own dedicated `rough_alt1`/`rough_alt2` splits required retraining upstream speed and DOC submodels too (see §5 for their standalone accuracy — they collapse just as badly, which mechanically drags the cascade down with them).

**Speed, across 6 alternates: mean 62.2%, sample std 9.1 percentage points, range 46.7–73.3%.** Standard's 93.3% sits ~3.4 sample standard deviations above that mean.
**Feed Coarse, across 4 alternates: mean 23.6%, sample std 11.4 percentage points, range 11.1–33.3%.** Standard's 91.7% sits ~6.0 sample standard deviations above that mean — the largest gap of any target, and the alternates themselves are at or below the 33.3% random-guess baseline for 3 classes.
**DOC and Roughness** only have 2 alternates each so a std isn't meaningful, but both still drop 20-58 points below Standard, including one Roughness alternate (33.3%) landing exactly at the 3-class chance baseline.

**This means none of the four headline figures should be presented as a config's true, generalizable accuracy — they are all best-of-one-split numbers**, exactly the failure mode Shoulder Milling's own exp11/exp12 analysis warned about (their headline cascade/SMOTE numbers similarly did not survive a different split). Report these fixed-split numbers only alongside this caveat, and prefer the split-robustness section (§5) as the honest characterization of these configs. See §5 for full detail and next steps.

---

## 1. Speed (5-class: 1500 / 2000 / 3000 / 4000 / 5000 rpm)

**Ensemble:** soft-vote average of two independently-trained models:
1. `models_speed_32x12_9win/resnet18_lr0.001_nosmote_best.pt` — 32x12 feature columns, 9-window split
2. `models_speed_32x3/resnet18_lr0.001_nosmote_best.pt` — 32x3 CWT-only, 3-window split, no scale selection

**Result:** 93.3% (14/15 test runs), up from the single-model best of 86.7% (13/15, `models_speed_32x3_speedopt_perdoc/resnet18_lr0.001_nosmote_best.pt`, per-DOC-normalized + Spearman scale selection — still the best single model, kept below for reference).

**Precision/recall (ensemble, run-level, macro avg):** precision 0.950, recall 0.933, F1 0.931. Per-class: 1500rpm P=0.750/R=1.000, 2000rpm P=1.000/R=1.000, 3000rpm P=1.000/R=1.000, 4000rpm P=1.000/R=0.667, 5000rpm P=1.000/R=1.000 (support=3 runs/class). Computed via `ensemble_eval.py`'s per-class report.

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

**Precision/recall (ensemble, run-level, macro avg):** precision 0.933, recall 0.917, F1 0.915. Per-class: Low P=1.000/R=1.000, Med P=1.000/R=0.750, High P=0.800/R=1.000 (support=4 runs/class). Computed via `ensemble_eval.py`'s per-class report.

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

**Precision/recall (run-level, macro avg):** precision 0.933, recall 0.917, F1 0.915 (from `eval_detailed_summary.csv`, `precision_macro_soft`/`recall_macro_soft`/`f1_macro_soft` columns).

- Top-32 CWT scales, 3-window split.
- **Condition-residual correction:** for each run's feature image, subtracted the mean image of all runs sharing the same (DOC x speed) condition — removes the DOC/speed signal that dominates and confounds Ra (Ra is near-perfectly correlated with DOC in this dataset), leaving only within-condition (feed-driven) variation.
- **Cascade conditioning:** DOC and speed are first predicted by their own best models, then those *predicted* (not ground-truth) labels are injected into the roughness classifier — avoids requiring true condition labels at inference time.

**Techniques tried that did not beat this:** ground-truth DOC-conditioning (ceiling 66.7% even with the true condition given to the model), harmonic features (not attempted for roughness — not a speed-harmonic-driven signal), band-statistics features (50%, worse), 32x12 / 9-window residual variant without cascade conditioning (previously misreported as 91.7% for `resnet18_lr0.001_smote` — does not reproduce; actual 83.3%, see correction note above).

---

## 4. Depth of Cut (3-class: 0.015 / 0.030 / 0.060 mm)

**Feature dir:** `scalograms_32x3_docopt_raw3w/`
**Model:** ResNet-18, lr=1e-3, SMOTE
**Result:** 100.0% (12/12 test runs)

**Precision/recall (run-level, macro avg):** precision 1.000, recall 1.000, F1 1.000 (perfect classification on this test split).

- Top-32 CWT scales selected for DOC specifically (`docopt` scale selection), using the raw-window (`raw3w`) construction variant of the 3-window split.
- SMOTE applied for class balance.
- Consistent with the general finding (also seen in Shoulder Milling) that DOC and Speed carry the strongest, least-confounded signal in the feature set — DOC reaches a clean ceiling with standard techniques.

---

## 5. Split-robustness check (all four targets)

Mirroring Shoulder Milling's exp11/exp12 practice of checking whether a "best" config's accuracy survives a different held-out set, alternate splits were added across several sessions for all four targets: `SPEED_TEST_RUNS_ALT1`-`ALT6`, `FEED_COARSE_TEST_RUNS_ALT1`-`ALT4`, `DOC_TEST_RUNS_ALT1`/`ALT2`, and `RA_TEST_RUNS_ALT1`/`ALT2` (defined in `cnn_model/cnn_train.py`, selectable via `cnn_train_32x3.py --split alt1`/`alt2`/.../`alt6`). Speed's 9-runs-per-class pool divides evenly, so `SPEED_TEST_RUNS` + `ALT1` + `ALT2` form a clean 3-way partition of all 45 runs, and `SPEED_TEST_RUNS` + `ALT3` + `ALT4` form a second, distinct clean 3-way partition. Feed Coarse's per-class run pools are highly unbalanced (15/21/9 runs for low/med/high); the "high" class only has 9 runs total, so some alt splits for that one class necessarily share test runs.

**Alt3/Alt4 (speed):** Alt1/Alt2 turned out to be DOC-imbalanced within every single speed class (e.g. Alt1's 1500rpm test triplet is 2×DOC=0.030 + 1×DOC=0.060, no DOC=0.015 run at all) — unlike the standard split, which deliberately holds out exactly one run per DOC level per class. Alt3/Alt4 were constructed by a deterministic, pre-registered rule (for each of the 15 class×DOC cells, Alt3 takes the lower-numbered of the two runs not already in `SPEED_TEST_RUNS`, Alt4 takes the higher-numbered one) to restore that same DOC-balance property — testing whether Alt1/Alt2's collapse was simply an artifact of unbalanced DOC representation rather than genuine non-generalization.

**Alt5/Alt6 (speed):** a third, independent DOC-balanced 3-way partition of all 45 runs, added purely to grow the alternate-split sample size for a more reliable mean/std estimate.

**Alt3/Alt4 (feed coarse), Alt1/Alt2 (DOC), Alt1/Alt2 (roughness cascade, "rough_alt1"/"rough_alt2"):** DOC and Roughness previously had no split-robustness check at all. Roughness's classifier uses *predicted* (not ground-truth) DOC/speed conditioning via cascade, so checking its split-robustness required retraining dedicated speed and DOC submodels under the same `rough_alt1`/`rough_alt2` run pools first, then feeding their predictions into a roughness model retrained on that same split.

### Results

| Target | Standard | Alt1 | Alt2 | Alt3 | Alt4 | Alt5 | Alt6 |
|---|---|---|---|---|---|---|---|
| Speed ensemble | **93.3%** (14/15) | 46.7% (7/15) | 66.7% (10/15) | 60.0% (9/15) | 73.3% (11/15) | 60.0% (9/15) | 66.7% (10/15) |
| Feed Coarse ensemble | **91.7%** (11/12) | 33.3% (4/12) | 16.7% (2/12) | 11.1% (1/9) | 33.3% (3/9) | — | — |
| DOC | **100.0%** (12/12) | 83.3% (10/12) | 41.7% majority / 50.0% soft (5–6/12) | — | — | — | — |
| Roughness cascade | **91.7%** (11/12) | 33.3% majority/soft (rough_alt1) | 66.7% majority / 55.6% soft (rough_alt2) | — | — | — | — |

Speed ensemble under Alt3: macro precision 0.550, recall 0.600, F1 0.521 — well below the near-1.000 macro F1 implied by Standard's 14/15 accuracy. The 4000rpm class is missed completely (0/3), the same kind of single-class collapse seen in Alt1's 1500rpm class.

**Feed Coarse Alt3/Alt4 submodel breakdown** (window-level / run-majority accuracy for each ensemble member alone, before averaging):

| Split | Ensemble | `convnext_tiny` (32x3_feedopt_9win) alone | `resnet50` residual (32x3_feedopt_raw9w) alone |
|---|---|---|---|
| Alt3 | 11.1% (1/9) | 44.4% / 33.3% | 13.6% / 11.1% |
| Alt4 | 33.3% (3/9) | 37.0% / 33.3% | 21.0% / 11.1% |

Under Alt3, the ensemble (11.1%) scores *worse* than either submodel alone (33.3%/11.1%) — the two models' probability vectors disagree in a way that soft-voting actively hurts rather than helps, the opposite of the Standard-split behavior where combining them was what pushed accuracy above either single model. This is a second, independent piece of evidence (beyond the raw accuracy drop) that the ensemble's Standard-split synergy is a property of that specific split, not a general one.

**Roughness cascade submodel breakdown** (the speed/doc submodels supply the predicted conditioning the roughness classifier depends on):

| Split | Speed submodel (run acc) | DOC submodel (run acc) | Roughness cascade (majority / soft) |
|---|---|---|---|
| Rough-Alt1 | 22.2% | 55.6% | 33.3% / 33.3% |
| Rough-Alt2 | 55.6% | 66.7% | 66.7% / 55.6% |

The roughness cascade's own accuracy tracks its upstream submodels' accuracy (worst on Rough-Alt1, where the speed submodel is worst too) — a mechanistic explanation for *why* the cascade collapses: it isn't just that the roughness signal itself is split-sensitive, it's that the conditioning it depends on is supplied by submodels that are themselves not split-robust, compounding the error.

**Summary statistics:**
- **Speed, across 6 alternates:** mean 62.2%, sample std 9.1pp, range 46.7–73.3%. Standard's 93.3% sits ~3.4 sample standard deviations above the mean.
- **Feed Coarse, across 4 alternates:** mean 23.6%, sample std 11.4pp, range 11.1–33.3%. Standard's 91.7% sits ~6.0 sample standard deviations above the mean — the largest gap of any target — and every alternate is at or below the 33.3% random-guess baseline for 3 classes.
- **DOC, across 2 alternates:** 83.3% and 41.7%/50.0%, mean ~62.5% — too few points for a meaningful std, but even the "clean ceiling" target (100% on Standard, previously assumed to have the least-confounded signal) drops 17-58 points on alternates.
- **Roughness cascade, across 2 alternates:** 33.3% and 66.7%/55.6% — Rough-Alt1 lands exactly at the 33.3% chance baseline.

None of these are "one unlucky alternate split" — in every target, Standard is the outlier relative to the honest spread across multiple independent, structurally-equivalent held-out sets.

**Verification note:** unlike Alt1/Alt2 (both ensemble members' `window_preds.csv`/`_detailed.md` committed alongside their history JSONs), Speed's Alt3 has only `models_speed_32x12_9win/resnet18_lr0.001_alt3_history.json`/`_best.pt` committed (no prediction CSV, nothing for the `32x3` member), and Alt4/Alt5/Alt6 have no artifacts committed at all. The 32x12_9win model's own single-model accuracy under Alt3 (73.3%, 11/15, from its `history.json`) is consistent with the reported ensemble figure being well below Standard, but the exact Alt3-Alt6 ensemble numbers are not independently reproducible from what's currently committed — they rest on the reported results, as do all of the Feed Coarse Alt3/Alt4, DOC Alt1/Alt2, and Roughness rough_alt1/rough_alt2 numbers above.

**Conclusion:** no target's headline config generalizes past its one fixed split. Speed and Feed Coarse's extended alternate sets (6 and 4 splits respectively) rule out the most obvious counter-explanations — DOC-imbalance in the early alt splits, and small-sample noise from having only 1-2 alternates — since larger, properly-balanced alternate sets still land far below Standard with consistent spread. DOC and Roughness, previously untested, show the same pattern: DOC's "clean ceiling" claim does not survive a split change, and Roughness's cascade collapses in step with its upstream conditioning submodels. Accuracy drops 17-80 percentage points across all alternates tested; Feed Coarse and one Roughness alternate fall to at-or-below the random-guess baseline for their respective class counts. This is the same pattern Shoulder Milling found for its own "best" cascade/SMOTE configs: single-split accuracy numbers in this size of dataset (9-15 test runs) are not a reliable estimate of true generalization, and every >90% figure reported in this README should be read as "achievable on a favorably-chosen split" rather than "the model's real-world accuracy." A trustworthy number would require either (a) averaging accuracy across many random splits / leave-one-condition-out CV (as Shoulder Milling's `cv_evaluate.py` does), or (b) a genuinely held-out validation set collected independently of the run pool used for all split definitions — neither has been done here. Future work on this dataset should prioritize implementing an honest cross-validation harness (Shoulder Milling's `cv_evaluate.py`/`cv_exp_splits.py` pattern) over further single-split accuracy chasing.

---

## Notes

- All accuracies are **run-level**, computed by averaging window-level softmax probabilities per run and taking the argmax (soft probability averaging), evaluated on the fixed held-out test-run sets used throughout this project (`SPEED_TEST_RUNS`, `FEED_COARSE_TEST_RUNS`, `RA_TEST_RUNS_12`, DOC test runs — 15 test runs for speed, 12 for feed/roughness/doc).
- Training history JSON files (`*_history.json`) in `cnn_model/models_*/` can under-report accuracy because the stored metric reflects a specific epoch's snapshot, not necessarily the epoch of the saved `_best.pt` checkpoint. The numbers in this README were verified by re-running inference with the saved `_best.pt` weights directly.
- Every technique in this README (residual correction, SMOTE, per-DOC normalization, 9-window splitting, 32x3/32x12 comparison, F-stat vs Spearman scale selection, and now multi-model soft-vote ensembling) is a direct port of the Shoulder Milling methodology. No End-Milling-specific feature engineering was needed to reach these numbers, aside from the DOC/speed-specific scale selection already built into the existing pipeline.
- **Ensembling** (Speed, Feed Coarse): two independently-trained single models' per-run softmax probability vectors are averaged, then argmaxed, using `ensemble_eval.py`. Candidate pairs were selected from all single-model configs scoring run_soft_acc >= 0.73-0.75 in `eval_detailed_summary.csv`, exhaustively searched over 2- and 3-model combinations. This mirrors Shoulder Milling's own conclusion that no single lever (backbone, LR, residual correction, cascade conditioning) reliably clears a hard target alone, and that combining diverse, decorrelated models is the more robust final step.
- Harmonic/FFT-amplitude features (`scalograms_harmonic_speedopt/`) were explicitly excluded from Speed's ensemble even though a harmonic+CWT combination reaches 100%, to preserve direct methodological comparability with Shoulder Milling (which has no harmonic-feature pipeline). Both Speed and Feed Coarse's reported ensembles use only feature-pipeline-consistent CWT-derived scalograms.
