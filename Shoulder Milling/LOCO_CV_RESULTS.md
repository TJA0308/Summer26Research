# Shoulder Milling — LOCO Cross-Validation Results

**Model:** ResNet-18, fine-tuned from ImageNet weights  
**Epochs:** 50, final-epoch evaluation only (no test-accuracy checkpoint selection)  
**Batch size:** 8 | **Optimizer:** Adam + cosine annealing LR schedule  
**Learning rates:** 1e-3 (primary) and 1e-4 (comparison)  
**Seeds:** seed 42 for all variant comparisons; seeds 42–46 for baseline 32x12/32x3

---

## 1. What is LOCO Cross-Validation?

**Leave-One-Condition-Out (LOCO)** cross-validation is a structured hold-out scheme
designed for small factorial experiments where standard random k-fold would allow
the model to memorize run-specific noise rather than learning the designed-factor
signal.

The dataset has 24 runs crossing 2 spindle speeds × 3 feed rates × 2 depths of cut
× 2 depths of engagement. LOCO holds out every run that shares a particular
combination of the *other* designed factors — so the held-out runs are the only
place where the target factor varies in isolation, making leakage impossible by
construction.

### Fold structure per target

| Target | Grouping (what is held out) | Folds | Runs/fold | Chance |
|--------|----------------------------|-------|-----------|-------------|
| Speed | depth-of-cut (y × z) | 4 | 6 | 50.0% |
| Feed | speed × doc (s × y × z) | 8 | 3 | 33.3% |
| DOC | speed × feed (s × f) | 6 | 4 | 25.0% |
| Roughness (primary) | doc (y × z) | 4 | 6 | 50.0%‡ |
| Roughness (secondary)† | speed × feed (s × f) | 6 | 4 | 50.0%†‡ |

‡Roughness is a balanced 2-class target (12 smooth / 12 rough of 24 runs), so true
chance is **50%** for both groupings. For feed/speed/doc, "chance" above is identical
to this script's zero-image nuisance-lookup floor (verified via `--selftest`) because
those are designed factors, independent of their LOCO grouping by construction. For
roughness the two diverge: the primary (doc-out) grouping's nuisance-lookup floor
measures **25%** — well BELOW the 50% true chance, confirming doc is genuinely held
out (a clean sanity check, not a lower chance level) — while the secondary grouping's
is **62.5%**, ABOVE true chance, meaning doc leaks into training there. All `+Margin`
figures below are computed against the 50% TRUE chance, never against either floor.

†Roughness/secondary is shown for reference only — not a valid LOCO number on its own.
Because Ra is strongly doc-driven, grouping by speed×feed leaves doc fully visible in
training, and a zero-image doc-lookup alone scores 62.5% run accuracy with NO
vibration signal at all. Never report a secondary-grouping roughness score without
this 62.5% floor alongside it.

### Anti-leakage discipline
- Final-epoch model only — no test-accuracy checkpoint selection
- No SMOTE — real windows only
- No cascade conditioning — plain unconditioned classifier throughout
- Headline metric: **run_acc_soft** (mean-probability soft vote over windows per run)
- 95% CI: exact Clopper-Pearson over 24 pooled runs

---

## 2. Scalogram Techniques

All scalograms are CWT (continuous wavelet transform) images of vibration signals.

| Technique | Description |
|-----------|-------------|
| **32x12** | 32 CWT scale rows × 12 time columns, 3 windows/run; rows selected by Spearman \|rho\| with Ra (same routine, `target="ra"`) |
| **32x3** | 32 scale rows × 3 time columns, 3 windows/run (narrower window); rows selected by Spearman \|rho\| with Ra |
| **9win** | Each of the 3 windows/run is cut into 3 contiguous scale-row bands (rows split along the 32-scale axis), giving 9 sub-images/run that share the parent window's label. This is a post-generation split, not re-windowing in time (`split_scalogram_windows.py`, docstring lines 1-14; `np.array_split(img, 3, axis=0)` at line 50) |
| **feedopt** | 32 CWT scale rows selected by Spearman \|rho\| between run-level mean CWT row (mexican, coif; averaged) and ordinal feed (3/5/7), fit once on all 24 runs* (`select_cwt_rows(target="feed")`, `build_option_c_scalograms.py:114-150`; not an F-statistic) |
| **feedopt_9win** | feedopt scale selection + 3-way scale-band split (9 sub-images/run) |
| **feedopt_residual** | feedopt scalograms with feed-predictive component residualized out* |
| **residual_doc** | CWT with doc-predictive component residualized out* |
| **residual_roughness** | CWT with Ra-predictive component residualized out* |
| **residual_speed** | CWT with speed-predictive component residualized out* |

*CWT scale selection and residualization are fit on all 24 runs before the LOCO loop —
LOCO cross-validates the classifier stage only, not the full end-to-end pipeline.

---

## 3. Full Results — lr = 1e-3, seed 42

*(32x12 and 32x3 baselines show mean ± std across seeds 42–46 in parentheses)*  
Margins = percentage points above the chance floor for that target.

### Speed (2 classes, chance = 50%)

| Scalogram | Score | +Margin |
|-----------|-------|---------|
| **32x12_9win** | **100.0%** | +50.0 pp |
| **32x12_residual_speed** | **100.0%** | +50.0 pp |
| **32x3_residual_speed** | **100.0%** | +50.0 pp |
| 32x12_residual_roughness | 95.8% | +45.8 pp |
| **32x12** | **87.5%** *(±9.3)* | +37.5 pp |
| 32x3 | 87.5% | +37.5 pp |
| 32x3_feedopt | 87.5% | +37.5 pp |
| 32x3_residual_roughness | 87.5% | +37.5 pp |
| 32x12_feedopt_9win | 83.3% | +33.3 pp |
| 32x12_feedopt_residual | 83.3% | +33.3 pp |
| 32x3_9win | 83.3% | +33.3 pp |
| 32x3_feedopt_9win | 83.3% | +33.3 pp |
| 32x12_feedopt | 79.2% | +29.2 pp |
| 32x12_residual_doc | 79.2% | +29.2 pp |
| 32x3_feedopt_residual | 79.2% | +29.2 pp |
| 32x3_residual_doc | 75.0% | +25.0 pp |

### DOC / Depth of Cut (4 classes, chance = 25%)

| Scalogram | Score | +Margin |
|-----------|-------|---------|
| **32x12_residual_doc** | **95.8%** | +70.8 pp |
| 32x3_feedopt_9win | 91.7% | +66.7 pp |
| 32x3_feedopt | 83.3% | +58.3 pp |
| 32x12_feedopt_9win | 83.3% | +58.3 pp |
| 32x3_residual_doc | 79.2% | +54.2 pp |
| 32x12_feedopt | 75.0% | +50.0 pp |
| 32x12_residual_speed | 75.0% | +50.0 pp |
| 32x3 | 75.0% | +50.0 pp |
| 32x12_9win | 70.8% | +45.8 pp |
| 32x3_9win | 70.8% | +45.8 pp |
| **32x12** | **60.0%** *(±3.7)* | +35.0 pp |
| 32x3_feedopt_residual | 58.3% | +33.3 pp |
| 32x3_residual_speed | 54.2% | +29.2 pp |
| 32x12_residual_roughness | 41.7% | +16.7 pp |
| 32x12_feedopt_residual | 37.5% | +12.5 pp |
| 32x3_residual_roughness | 37.5% | +12.5 pp |

### Feed Rate (3 classes, chance = 33.3%)

| Scalogram | Score | +Margin |
|-----------|-------|---------|
| **32x3_residual_roughness** | **87.5%** | +54.2 pp |
| 32x3_feedopt_residual | 79.2% | +45.9 pp |
| 32x12_feedopt_residual | 66.7% | +33.4 pp |
| 32x12_residual_roughness | 66.7% | +33.4 pp |
| 32x3_9win | 66.7% | +33.4 pp |
| 32x3_residual_speed | 66.7% | +33.4 pp |
| 32x12_residual_speed | 62.5% | +29.2 pp |
| **32x12** | **55.0%** *(±1.9)* | +21.7 pp |
| 32x3 | 54.2% | +20.9 pp |
| 32x3_feedopt | 50.0% | +16.7 pp |
| 32x3_feedopt_9win | 50.0% | +16.7 pp |
| 32x12_feedopt_9win | 45.8% | +12.5 pp |
| 32x12_9win | 41.7% | +8.4 pp |
| 32x3_residual_doc | 41.7% | +8.4 pp |
| 32x12_feedopt | 41.7% | +8.4 pp |
| 32x12_residual_doc | 33.3% | ≈ chance |

### Surface Roughness / Ra (2 classes, chance = 50% — see §1 footnote; DO NOT use 25%)

| Scalogram | Score | +Margin (vs true 50% chance) |
|-----------|-------|---------|
| **32x12_feedopt_9win** | **75.0%** | +25.0 pp |
| 32x12_9win | 70.8% | +20.8 pp |
| 32x3_feedopt_9win | 70.8% | +20.8 pp |
| 32x12_feedopt | 62.5% | +12.5 pp |
| 32x3_9win | 62.5% | +12.5 pp |
| **32x12** | **57.5%** *(±1.9)* | +7.5 pp |
| 32x3 | 58.3% | +8.3 pp |
| 32x3_feedopt | 58.3% | +8.3 pp |
| 32x3_residual_roughness | 58.3% | +8.3 pp |
| 32x12_residual_speed | 54.2% | +4.2 pp |
| 32x3_residual_speed | 54.2% | +4.2 pp |
| 32x3_residual_doc | 50.0% | ≈ chance |
| 32x12_residual_doc | 45.8% | -4.2 pp |
| 32x3_feedopt_residual | 45.8% | -4.2 pp |
| 32x12_feedopt_residual | 37.5% | -12.5 pp |
| 32x12_residual_roughness | 29.2% | -20.8 pp (BELOW chance — expected: this variant has the Ra-predictive component residualized out by design, see §2) |

---

## 4. lr=1e-3 vs lr=1e-4 Comparison (seed 42)

*(all results now complete)*

**Provenance (confirmed):** all 48 cells were matched by `find_missing_runs.py`. lr=1e-3 = the first
seed-42 loco row per (target, group, scalogram); lr=1e-4 = the explicit lr=1e-4 row for 12 cells, or the
second (blank-`lr`) seed-42 row for the other 36 cells. The only missing run is
roughness/secondary/`32x12_feedopt_9win` at lr=1e-3 (queued as gpu_jobs batch A).

### Speed

| Scalogram | lr=1e-3 | lr=1e-4 | Winner |
|-----------|---------|---------|--------|
| 32x12_9win | 100.0% | 50.0% | **1e-3** |
| 32x3_9win | 83.3% | 79.2% | 1e-3 |
| 32x12_feedopt_9win | 83.3% | 62.5% | **1e-3** |
| 32x3_feedopt_9win | 83.3% | 58.3% | **1e-3** |
| 32x12_feedopt_residual | 83.3% | 58.3% | **1e-3** |
| 32x3_feedopt_residual | 79.2% | 62.5% | 1e-3 |
| 32x12_residual_doc | 79.2% | 41.7% | **1e-3** |
| 32x3_residual_doc | 75.0% | 50.0% | **1e-3** |
| 32x12_residual_roughness | 95.8% | 62.5% | **1e-3** |
| 32x3_residual_roughness | 87.5% | 62.5% | **1e-3** |
| 32x12_residual_speed | 100.0% | 58.3% | **1e-3** |
| 32x3_residual_speed | 100.0% | 50.0% | **1e-3** |

### DOC

| Scalogram | lr=1e-3 | lr=1e-4 | Winner |
|-----------|---------|---------|--------|
| 32x12_9win | 70.8% | 29.2% | **1e-3** |
| 32x3_9win | 70.8% | 25.0% | **1e-3** |
| 32x12_feedopt_9win | 83.3% | 29.2% | **1e-3** |
| 32x3_feedopt_9win | 91.7% | 25.0% | **1e-3** |
| 32x12_feedopt_residual | 37.5% | 25.0% | **1e-3** |
| 32x3_feedopt_residual | 58.3% | 25.0% | **1e-3** |
| 32x12_residual_doc | 95.8% | 25.0% | **1e-3** |
| 32x3_residual_doc | 79.2% | 25.0% | **1e-3** |
| 32x12_residual_roughness | 41.7% | 25.0% | **1e-3** |
| 32x3_residual_roughness | 37.5% | 33.3% | 1e-3 |
| 32x12_residual_speed | 75.0% | 25.0% | **1e-3** |
| 32x3_residual_speed | 54.2% | 29.2% | **1e-3** |

### Feed

| Scalogram | lr=1e-3 | lr=1e-4 | Winner |
|-----------|---------|---------|--------|
| 32x12_9win | 41.7% | 33.3% | **1e-3** |
| 32x3_9win | 66.7% | 33.3% | **1e-3** |
| 32x12_feedopt_9win | 45.8% | 33.3% | **1e-3** |
| 32x3_feedopt_9win | 50.0% | 41.7% | **1e-3** |
| 32x12_feedopt_residual | 66.7% | 50.0% | **1e-3** |
| 32x3_feedopt_residual | 79.2% | 41.7% | **1e-3** |
| 32x12_residual_doc | 33.3% | 33.3% | tie |
| 32x3_residual_doc | 41.7% | 29.2% | **1e-3** |
| 32x12_residual_roughness | 66.7% | 41.7% | **1e-3** |
| 32x3_residual_roughness | 87.5% | 58.3% | **1e-3** |
| 32x12_residual_speed | 62.5% | 41.7% | **1e-3** |
| 32x3_residual_speed | 66.7% | 45.8% | **1e-3** |

### Roughness (primary)

| Scalogram | lr=1e-3 | lr=1e-4 | Winner |
|-----------|---------|---------|--------|
| 32x12_9win | 70.8% | 54.2% | 1e-3 |
| 32x3_9win | 62.5% | 50.0% | 1e-3 |
| 32x12_feedopt_9win | 75.0% | 66.7% | 1e-3 |
| 32x3_feedopt_9win | 70.8% | 50.0% | **1e-3** |
| 32x12_feedopt_residual | 37.5% | 41.7% | 1e-4 (+4 pp, within noise) |
| 32x3_feedopt_residual | 45.8% | 45.8% | tie |
| 32x12_residual_doc | 45.8% | 41.7% | 1e-3 |
| 32x3_residual_doc | 50.0% | 45.8% | 1e-3 |
| 32x12_residual_roughness | 29.2% | 50.0% | 1e-4 (+20.8 pp) |
| 32x3_residual_roughness | 58.3% | 45.8% | **1e-3** |
| 32x12_residual_speed | 54.2% | 45.8% | 1e-3 |
| 32x3_residual_speed | 54.2% | 41.7% | **1e-3** |

### Verdict

**lr = 1e-3 wins 44/48 comparisons, 2 are ties, 2 go to lr = 1e-4** (all results complete;
per target: speed 12/12, DOC 12/12, feed 11/12 + 1 tie, roughness 9/12 + 1 tie + 2 for 1e-4).
Ties: `32x12_residual_doc` (feed, 33.3% vs 33.3%) and `32x3_feedopt_residual` (roughness, 45.8% vs 45.8%).
The two 1e-4 wins are both roughness: `32x12_feedopt_residual` (+4.2 pp, within noise) and
`32x12_residual_roughness` (+20.8 pp, against a 1e-3 score of 29.2%, which is itself below the 50% chance level;
the 1e-4 score of 50.0% is exactly chance, so this is not a real 1e-4 advantage).
Across all targets, lr=1e-4 shows severe degradation on doc (most variants drop to
chance = 25%) and large drops on speed (most fall 20–50 pp). All four lr=1e-4 9win
feed results land at or near chance (25–42%), and all four 9win doc results collapse
to chance (25–29%). **Use lr = 1e-3.**

---

## 5. Best Configurations Per Target

| Target | Best Scalogram | lr=1e-3 Score | Chance | +Margin |
|--------|---------------|--------------|--------|---------|
| **Speed** | 32x12_9win (or residual_speed) | 100.0% | 50% | +50.0 pp |
| **DOC** | 32x12_residual_doc | 95.8% | 25% | +70.8 pp |
| **Feed** | 32x3_residual_roughness | 87.5% | 33.3% | +54.2 pp |
| **Roughness** | 32x12_feedopt_9win | 75.0% | 50% | +25.0 pp |

Full commands (lr=1e-3, seed 42):

```bash
# Speed
python cv_evaluate.py --img_dir scalograms_32x12_9win --target speed \
    --models cnn --arch resnet18 --epochs 50 --seeds 42

# DOC
python cv_evaluate.py --img_dir scalograms_32x12_residual_doc --target doc \
    --models cnn --arch resnet18 --epochs 50 --seeds 42

# Feed
python cv_evaluate.py --img_dir scalograms_32x3_residual_roughness --target feed \
    --models cnn --arch resnet18 --epochs 50 --seeds 42

# Roughness
python cv_evaluate.py --img_dir scalograms_32x12_feedopt_9win --target roughness \
    --models cnn --arch resnet18 --epochs 50 --seeds 42
```

---

## 6. Key Findings

**Speed is the easiest and most robust target.** Every variant scores well above chance
(≥75%), and three variants reach 100%. The signal is encoded across all CWT
representations.

**9win variants outperform non-9win for roughness and DOC.** Splitting into scale bands (more, narrower-bandwidth samples per run) helps the harder targets. `feedopt_9win` (CWT scale selection +
9 windows) is the best roughness representation.

**Residual variants are informative diagnostics:**
- `residual_doc` → DOC boosts to 95.8%: removing the linear doc component isolates
  nonlinear doc-specific CWT structure, making it easier to classify
- `residual_roughness` → Feed boosts to 87.5%: Ra is correlated with feed but is not
  a designed factor; removing this confound lets the model focus on genuine feed signal
- `residual_roughness` → DOC drops to ~38%: Ra carries useful DOC information;
  removing it hurts
- `residual_roughness` → Speed stays high (87.5%): Ra does not confound speed

**Feed is the hardest target.** Most variants are only modestly above chance. The
`32x12_residual_doc` variant scores exactly at chance (33.3%), showing doc variation
is a major confound for feed when not removed. Best results require residualization.

**32x12 vs 32x3:** 32x12 is generally slightly better or equal. The main exception is
DOC, where `32x3_feedopt_9win` (91.7%) nearly matches `32x12_residual_doc` (95.8%),
suggesting narrower temporal windows can be sufficient for depth-of-cut.

**lr=1e-3 dominates lr=1e-4** across virtually all variants and targets — especially
for DOC, where lr=1e-4 consistently degrades to chance (25%).

---

## 7. Caveats

1. **Single-seed survey** — all variant comparisons use seed 42 only. Observed seed
   variance on the 32x12 baseline was ±1.9–9.3 pp. Differences < 10 pp between
   variants should not be over-interpreted.

2. **Classifier-stage CV only** for feedopt and residual variants — preprocessing
   (CWT scale selection, residualization) was fit on all 24 runs before LOCO.

3. **Small dataset** — 24 runs total. Clopper-Pearson 95% CI at 60% accuracy spans
   approximately ±20 pp. All numbers are estimates, not guarantees.

4. **ResNet-18 only** — used exclusively based on prior architecture sweep results
   showing it as the most consistent performer across targets.

5. **Residualized variants may be transductive (confirmed against code).** In
   `build_residual_scalograms.py` the residual group is (doc, feed) for speed, (speed, feed) for
   doc, and side (= speed x doc) for feed and roughness. Each of these groups lies entirely within
   one LOCO fold's held-out set (speed folds by doc, DOC folds by speed x feed, feed folds by
   speed x doc, roughness folds by doc), so every test image is centred on a mean computed from
   test-fold images only (the script's own docstring acknowledges only the 1/N self-contribution).
   The 100% `residual_speed` and 95.8% `residual_doc` scores may therefore be optimistic and should
   not be read as clean generalization numbers.

6. **CWT row selection used all 24 runs for every selected dir.** The base 32x12 / 32x3 dirs select
   rows by Spearman correlation with Ra over all 24 runs (`scalogram_readme.md` Option C; `select_cwt_rows`
   in `build_option_c_scalograms.py`), and the feedopt dirs use the same routine with feed as target
   (Spearman rank correlation, as section 2 now states). Residual and 9win
   dirs inherit this. Only `scalograms_64x2_full` is expected to be unselected; I did not verify that
   dir's builder.

7. **Best-of-16 winner's curse.** The per-target "best" configurations in section 5 are the argmax
   over 16 variants of a single seed-42 run; the selected score is upward-biased and the baseline
   seed std (up to +/-9.3 pp) is comparable to many gaps between variants.

---

## 8. Pre-registration (written before multi-seed runs)

**Status: PROPOSED - pending user approval.**

Final configuration per target, chosen by seed-42 argmax (lr = 1e-3):

| Target | Config | Seed-42 score | Note |
|--------|--------|---------------|------|
| Speed | 32x12_9win | 100.0% | Ties with residual_speed (100%); pre-registered tie-break = simplest preprocessing, which excludes the possibly transductive residual (caveat 5) |
| DOC | 32x12_residual_doc | 95.8% | Residualized; see caveat 5 |
| Feed | 32x3_residual_roughness | 87.5% | |
| Roughness | 32x12_feedopt_9win | 75.0% | |

Headline metric: mean +/- std of run_acc_soft over seeds 43-46 only (seed 42 is the selection
seed and is excluded from the headline), with a pooled exact Clopper-Pearson 95% CI over runs
pooled across those seeds. The 32x12 baseline is reported alongside for every target, with the
split each number comes from stated explicitly.
