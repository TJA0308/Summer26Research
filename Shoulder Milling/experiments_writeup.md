# Shoulder Milling: cascade conditioning → feedopt → windowing

Chronological writeup of everything tried from cascade conditioning onward, with
the actual numbers behind each step. Covers commits `fb14ab7` through `088cee4`.

Background: all targets are predicted from "scalogram" images built from
pre-computed per-window CWT/FFT/DWT feature vectors (no raw waveform exists in
`data/Side*.xlsx`). Two scalogram layouts are compared throughout: Option C
(`scalograms_32x12`, 32 CWT scale rows × 12 cols) and Option D (`scalograms_32x3`,
32 rows × 3 cols: FFT + 2 wavelet families). Speed and doc were solved early
(near-100% run accuracy with plain independent CNNs); **feed rate is the
target that drove nearly all of the work below** — it plateaued around 50–75%
run accuracy no matter what was tried.

## 1. Cascade conditioning 

Idea: feed rate might be easier to predict if the model also knows the
(predicted) speed and depth-of-cut, since the three process parameters aren't
independent in how they imprint on the vibration spectrum.

Implementation: `ConditionedModel` wraps any of the 4 backbones (resnet18,
resnet50, efficientnet_b0, convnext_tiny), concatenating one-hot vectors of
*predicted* parent labels with the pooled CNN features before the classifier
head. `cnn_train_param.py` auto-detects cascade conditioning — doc conditions
on predicted speed, feed conditions on predicted speed+doc — if the matching
`<parent>_pred_<scalo>.csv` already exists; otherwise it trains unconditioned
with a warning. `predict_conditioning.py` generates those CSVs from the single
best already-trained parent model. SMOTE is auto-skipped in conditioned mode
(synthetic windows have no real upstream parent to condition on).

Also introduced in this commit: per-target dropout (speed=0.0, doc/feed=0.15
— speed showed no overfitting and was hurt by a uniform 0.3 dropout in an
earlier sweep; doc/feed did overfit, but 0.3 was too strong).

**Known caveat, flagged at the time and never fully resolved:** the parent
predictions used for conditioning come from one fully-trained model evaluated
on its own training set, not from out-of-fold cross-validation. A
conditioning model's "known" parent labels during training are therefore
inflated relative to what it would see on genuinely held-out data. Accepted
as a simplification given dataset size (48 train / 8 test runs).

## 2. SMOTE sweeps + eval-robustness fixes (`6ed1d83`, `1eabc0d`)

Two full sweeps (3 targets × 2 scalogram sizes × 4 archs × 2 LRs = 48 models
each, `--run_tag smote`), the second after adding label smoothing, Gaussian
noise augmentation, and wiring cascade conditioning into the feed run.

Results were consistent across both passes:
- doc improved with SMOTE — best became 100% run accuracy (resnet18/32x3/lr=1e-3, up from 87.5%).
- speed stayed at 100% on its best configs, unaffected by SMOTE.
- **feed stayed the hardest target, capping out at 75% run accuracy** (efficientnet_b0/32x12/lr=1e-4) — SMOTE alone did not move feed's ceiling.

This is the first concrete signal that feed's difficulty wasn't a class-imbalance
problem (SMOTE targets exactly that) — something else was capping it.

`eval_detailed_param.py` was also hardened in `1eabc0d` to auto-detect a
checkpoint's actual dropout/conditioning structure from its state-dict keys
rather than trusting the history JSON alone, since `.pt` files from a prior
run could have a different structure than the current code would produce.

## 3. Feed-correlated scale selection + roughness 2-class target (`c66237f`)

Root-cause hypothesis: the 32 CWT scale rows kept in Option C/D scalograms are
selected by Spearman correlation with **Ra (surface roughness)**, never with
feed — because the original design target was Ra. A direct check found 8 of
those 32 Ra-tuned rows are actually below-average for feed separability, while
~8 of the rows it discards (mostly coarse scales 36–50) carry real feed
signal that the Ra-tuned selection throws away.

Fix: added `--target {ra,feed}` to both scalogram-build scripts and generated
feed-correlated variants — `scalograms_32x12_feedopt` and
`scalograms_32x3_feedopt` — using the same `select_cwt_rows()` logic but
scored against feed instead of Ra.

Also added in this commit: a 2-class **roughness** target (smooth Ra≤0.4 vs.
rough Ra>0.4), reusing doc's train/test split (which happens to land exactly
8/8 train and 4/4 test for that binary split).

Smoke test (efficientnet_b0/lr=1e-4, single config): feed run accuracy
**75.0% on `scalograms_32x12_feedopt` vs. 62.5%** on the Ra-tuned
`scalograms_32x12` — feedopt scale selection helped immediately. Roughness
hit 87.5% run accuracy in the same smoke test.

## 4. Full roughness + feedopt sweeps (`de281e3`)

- Roughness: 16 models (2 scalogram sizes × 4 archs × 2 LRs, no SMOTE). Best: **100% run accuracy** (efficientnet_b0/32x12/lr=1e-4).
- Feed on feedopt scalograms, unconditioned: 16 models (smote tag). Best **71.4% run accuracy excluding run s25f7y5z25** (5/7) vs. 57.1% (4/7) on the standard Ra-tuned scalograms over the same 7 runs — confirms the feedopt scale selection helps, independent of conditioning.
- Speed+doc retrained on the feedopt dirs as well, purely to produce the parent-prediction CSVs needed to condition feed in the next step.


## 5. Scalogram windowing: split into 9 sub-windows (`44ceb88`, `088cee4`)

Different lever: instead of changing scale-row selection or adding
conditioning, increase the number of independent samples per run. Each run
currently has only 3 time windows; majority-voting over 3 noisy votes is
fragile (one flipped window changes the run's outcome).

There is no raw waveform anywhere in the repo to re-window in time — `data/Side*.xlsx`
only stores pre-computed per-window CWT/FFT/DWT feature vectors. So this is a
**post-generation split of the already-built scalogram PNGs along the scale-row
axis**: each existing `(32, C)` window image is cut into 3 contiguous row-bands
(`np.array_split`, sizes 11/11/10) via the new `split_scalogram_windows.py`,
tripling 3 windows/run to 9 sub-windows/run, applied to all four scalogram
variants (`scalograms_32x12[_feedopt]`, `scalograms_32x3[_feedopt]`) into
sibling `*_9win` directories with the same `labels.csv` schema. Windows are
relabelled `w1..w9` per run in parent-window order, so existing run-level
majority-vote grouping (by the numeric `run` column) works unmodified.

`cnn_train_param.py` needed no changes (already groups by numeric `run`,
window-count-agnostic). `eval_detailed_param.py` was generalized from a
hardcoded `w1/w2/w3` dict to parsing the window number directly out of the
label string, and `eval_one()` now derives `n_windows` from the loaded data
instead of assuming 3 — verified against the new 9-window data (8 test runs
× 9 correctly-ordered windows each for feed).

`run_9win_sweep.ps1` mirrors the existing sweep runners: trains
speed/doc/feed/roughness on the standard 9win dirs, trains speed+doc on the
feedopt 9win dirs to regenerate feed's conditioning CSVs, retrains feed
conditioned, then runs detailed eval over everything into `exp_results_*_9win/`.

**Status: run.** Command used (from `Shoulder Milling/`):

```powershell
.\run_9win_sweep.ps1
```

Results are in §6 below.

## 6. 9-window sweep results

New project-best for feed: **efficientnet_b0 / lr=1e-4 /
`scalograms_32x3_feedopt_9win`, conditioned on speed+doc: 87.5% (7/8) run
accuracy** — beats the 75% ceiling that had held since §2. Confirmed
genuinely conditioned via its `history.json`
(`conditioned: True, cond_parents: ['speed', 'doc']`). It gets both `s25f7y5z25` and
`s35f5y25z125` right — the two runs most consistently missed in every prior
conditioned-feed sweep — and only misses `s35f3y5z125`. Window-level accuracy for this
model is just 45.8%, lower than several configs that scored worse at the run
level: the win comes from majority-vote-over-9 smoothing out per-window
noise, not from the model being more accurate window-by-window.

**Best-of-sweep (ceiling) comparison, old 3-window vs. new 9-window**
(8 arch/lr configs per row):

| target | scalogram | old best | new best | Δ |
|---|---|---|---|---|
| feed (conditioned) | 32x3_feedopt | 75.0% | **87.5%** | **+12.5pp — new project best** |
| feed (conditioned) | 32x12_feedopt | 75.0% | 62.5% | −12.5pp |
| feed (unconditioned) | 32x3 | 75.0% | 75.0% | tied |
| feed (unconditioned) | 32x12 | 75.0% | 62.5% | −12.5pp |
| doc | 32x12 | 87.5% | **100%** | +12.5pp (resnet18/lr=1e-3) |
| doc | 32x3 | 87.5% | 87.5% | tied |
| speed | 32x12 / 32x3 | 100% | 100% | tied |
| roughness | 32x12 | 100% | 100% | tied |
| roughness | 32x3 | 87.5% | 87.5% | tied |

**But average stability across configs dropped almost everywhere** —
comparing the mean accuracy across all 8 arch/lr configs per target/scalogram,
not just the best one:

| target/scalogram | old mean (3-win) | new mean (9-win) | Δ |
|---|---|---|---|
| speed/32x12 | 96.9% | 67.2% | −29.7pp |
| speed/32x3 | 93.8% | 79.7% | −14.1pp |
| doc/32x12 | 81.3% | 57.8% | −23.5pp |
| doc/32x3 | 79.7% | 50.0% | −29.7pp |
| feed/32x12 | 57.8% | 45.3% | −12.5pp |
| feed/32x3 | 62.5% | 48.4% | −14.1pp |
| roughness/32x12 | 76.6% | 76.6% | flat |
| roughness/32x3 | 92.2% | 75.1% | −17.1pp |

Even speed — which used to hit 100% on almost every config — now swings as
low as 50% depending on arch/lr. The peak (best-of-8) result held or
improved in most rows, but the typical config got worse in most rows too.
Consistent with the mechanism anticipated in §5: narrowing each sub-window's
scale bandwidth makes individual votes noisier; majority-vote-over-9 only
pays that off when a config's errors happen to spread out rather than recur
systematically, and otherwise just adds noise.

**Conclusion: the 9-window split is not a free win.** It produced the single
best feed result in the project, but it is arch/lr-sensitive, and made
several other targets (especially doc and speed) less reliable across the
sweep. If pursuing this further, the efficientnet_b0/lr=1e-4/32x3_feedopt
conditioned configuration specifically is the one worth re-validating (e.g.
across multiple training seeds), not the windowing approach in general.

## Summary table: feed run accuracy across every approach tried

| approach | best run accuracy | source |
|---|---|---|
| unconditioned, Ra-tuned scale rows (32x12/32x3) | 75% | §2 |
| unconditioned, feedopt scale rows, excl. run s25f7y5z25 | 71.4% | §4 |
| cascade-conditioned, feedopt scale rows, 3-window | 75% | commit `953654d` |
| cascade-conditioned, feedopt scale rows, 9-window | **87.5%** | §6 |

The headline result across sections 1–4: **feed-correlated scale selection
(§3) is the one change with a clear, reproducible effect (+12.5pp in the
original smoke test, replicated in the full sweep), while cascade
conditioning (§1) and SMOTE (§2) each individually failed to move feed's
ceiling beyond what feed-correlated scale selection alone already
achieved.** The windowing approach (§5–§6) changed that: cascade-conditioned
feed on `scalograms_32x3_feedopt_9win` (efficientnet_b0, lr=1e-4) reached
**87.5% (7/8)** — the first result to beat the 75% ceiling that had held
since the first SMOTE sweep — though §6 shows this gain was not uniform:
most other arch/lr configs got noisier (lower average accuracy) under the
9-window split, so the improvement is real but config-sensitive, not a
guaranteed win from windowing alone.

**Update (§7): the 87.5% figure above does not reproduce and should not be
treated as the project record — see §7 for the bug that likely produced it
and the honest, leakage-controlled numbers that replace it.**

## 7. Conditioning bug fix, multi-task alternative, and honest leave-one-side-out CV

**Bug found:** `predict_conditioning.py` was calling conditioned models with
`model(t)` — no conditioning tensors passed at all — when generating the
parent-prediction CSVs that downstream cascade stages (doc conditions on
speed, feed conditions on speed+doc) consume at training time. Fixed in
commit `e15d9ed`. Post-fix, the identical config that produced the 87.5%
figure above (efficientnet_b0/lr=1e-4/`scalograms_32x3_feedopt_9win`,
cascade-conditioned) reruns at **37.5%** — a 50pp swing on the exact same
arch/lr/split. The real cascade-conditioned feed ceiling, checked across the
original split and the cross-target-balanced exp11/exp12 splits (both
`32x12_feedopt_9win` and `32x3_feedopt_9win`), is consistently **~62.5% run
accuracy / ~41–46% window accuracy** — no better than unconditioned. **The
87.5% figure should be treated as a bug artifact, not a reproducible result.**

**Multi-task alternative** (`cnn_train_multitask.py`): one shared backbone +
three ground-truth-supervised heads (speed/doc/feed) trained jointly,
replacing the cascade's predicted-label conditioning entirely. Swept
efficientnet_b0/lr=1e-4 across `{32x3_feedopt, 32x12_feedopt}` × `{base,
exp11, exp12}` × 3 seeds (`run_multitask_feed.ps1`). Feed run accuracy
(hard-vote, mean ± std over seeds):

| scalogram | split | run acc |
|---|---|---|
| 32x12_feedopt | base | 66.7% ± 5.9% |
| 32x12_feedopt | exp11 | 50.0% ± 0.0% |
| 32x12_feedopt | exp12 | 58.3% ± 11.8% |
| 32x3_feedopt | base | 54.2% ± 15.6% |
| 32x3_feedopt | exp11 | 70.8% ± 5.9% |
| 32x3_feedopt | exp12 | 54.2% ± 5.9% |

Pre-registered verdict (`summarize_multitask.py`, fail if run acc ≤62.5% on
2+ of 3 splits): **FAIL on both scalogram dirs.** Multi-task relocates where
the lucky spikes land (66.7–70.8% vs. the cascade's 62.5% peaks) but doesn't
reliably clear the bar. `32x12_feedopt`/exp11's exact 50.0% ± 0.0% across all
3 seeds (zero variance) is worth a follow-up look — usually indicates the
model collapsed to the same prediction pattern regardless of initialization.

**Leave-one-side-out CV** (`cv_evaluate.py`): pools predictions across all 8
leave-one-side-out folds (24 runs total, 4.2pp granularity, no test-set-driven
model or checkpoint selection) — the cleanest read available, since every
number above still rests on picking configs and epochs using the same 8-run
test set they're scored on. HGB (StandardScaler + PCA-20 +
HistGradientBoosting on native pixels, same recipe as `baseline_classical.py`)
vs. `tiny_cnn` (~40K-param from-scratch CNN, no ImageNet pretraining, no
224×224 upsample):

| scalogram | model | run acc |
|---|---|---|
| 32x3_feedopt | hgb | 41.7% |
| 32x3_feedopt | tiny_cnn | ~39–42% |
| 32x12_feedopt | hgb | 54.2% |
| 32x12_feedopt | tiny_cnn | ~46–50% |
| 64x2_full (see below) | hgb | 45.8% hard / **54.2% soft** |
| 64x2_full | tiny_cnn | 40.3% ± 4.8% |

Two findings that revise earlier sections of this writeup:
1. **32x12 beats 32x3 under clean CV** (54.2% vs. 41.7% hgb) — the opposite
   of what the original 8-run splits suggested throughout §1–§6. The earlier
   "32x3 ties/beats 32x12" conclusion was itself resting on 8-run-split noise.
2. **HGB beats tiny_cnn everywhere tried.** None of the deep-learning
   machinery — cascade, multi-task, or even a from-scratch CNN — clears
   simple PCA + classical ML once evaluated honestly. The bottleneck looks
   like the *features*, not model capacity.

**Option E** (`build_option_e_scalograms.py`, `scalograms_64x2_full/`): tests
whether the Ra/feed-Spearman top-32 row selection used by every scalogram
variant above is discarding useful coarse-scale information, per the §3
finding that ~8 discarded rows (36–50) "carry real feed signal." Keeps ALL
64 CWT scale rows from both wavelet families (64mexican, 64coif), no row
selection, no FFT/DWT/time-stat columns (avoids reintroducing the dead-zone
problem §3/Option D was built to avoid). Result: HGB soft-vote run accuracy
54.2%, tying `32x12_feedopt`'s clean-CV result without needing the Spearman
selection step at all — selection isn't hurting, but skipping it doesn't
clearly help either.

**Bottom line as of §7:** the honest, leakage-controlled ceiling for feed
rate prediction on this pipeline is **~40–55% run accuracy** (pooled 24-run
CV), not the 87.5%/75% figures reported in §1–§6. Feed rate looks like a
genuinely hard target given this sensor/feature setup — a features-and-data
problem more than a modeling problem, since simple classical ML matches
every CNN variant tried so far.</new_string>

