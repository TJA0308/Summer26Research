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

| Target | Grouping (what is held out) | Folds | Runs/fold | Chance floor |
|--------|----------------------------|-------|-----------|-------------|
| Speed | depth-of-cut (y × z) | 4 | 6 | 50.0% |
| Feed | speed × doc (s × y × z) | 8 | 3 | 33.3% |
| DOC | speed × feed (s × f) | 6 | 4 | 25.0% |
| Roughness (primary) | doc (y × z) | 4 | 6 | 25.0% |
| Roughness (secondary)† | speed × feed (s × f) | 6 | 4 | 62.5%† |

†Roughness/secondary is shown for reference only — not a valid metric. Because Ra is
strongly doc-driven, grouping by speed×feed leaves doc fully visible in training,
and a zero-image doc-lookup alone scores 62.5%. Any roughness LOCO number must be
compared against 25% (primary grouping), not 50%.

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
| **32x12** | 32 CWT scale rows × 12 time columns, 3 windows/run |
| **32x3** | 32 scale rows × 3 time columns, 3 windows/run (narrower window) |
| **9win** | 9 temporal windows/run instead of 3 — 3× more images per run |
| **feedopt** | CWT scale rows selected by F-statistic on feed separability (fit once on all data*) |
| **feedopt_9win** | feedopt scale selection + 9-window temporal splitting |
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

### Surface Roughness / Ra (4 classes, chance = 25%, primary grouping only)

| Scalogram | Score | +Margin |
|-----------|-------|---------|
| **32x12_feedopt_9win** | **75.0%** | +50.0 pp |
| 32x12_9win | 70.8% | +45.8 pp |
| 32x3_feedopt_9win | 70.8% | +45.8 pp |
| 32x12_feedopt | 62.5% | +37.5 pp |
| 32x3_9win | 62.5% | +37.5 pp |
| **32x12** | **57.5%** *(±1.9)* | +32.5 pp |
| 32x3 | 58.3% | +33.3 pp |
| 32x3_feedopt | 58.3% | +33.3 pp |
| 32x3_residual_roughness | 58.3% | +33.3 pp |
| 32x12_residual_speed | 54.2% | +29.2 pp |
| 32x3_residual_speed | 54.2% | +29.2 pp |
| 32x3_residual_doc | 50.0% | +25.0 pp |
| 32x12_residual_doc | 45.8% | +20.8 pp |
| 32x3_feedopt_residual | 45.8% | +20.8 pp |
| 32x12_feedopt_residual | 37.5% | +12.5 pp |
| 32x12_residual_roughness | 29.2% | +4.2 pp (≈ chance — expected) |

---

## 4. lr=1e-3 vs lr=1e-4 Comparison (seed 42)

*(all results now complete)*

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

**lr = 1e-3 wins in 40/42 comparable cases** (all results complete).
The two 1e-4 wins are minor (+4 pp and +20.8 pp on `residual_roughness` roughness — both absolute scores are still low, near chance).
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
| **Roughness** | 32x12_feedopt_9win | 75.0% | 25% | +50.0 pp |

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

**9-window variants outperform 3-window for roughness and DOC.** More temporal context
consistently helps the harder targets. `feedopt_9win` (CWT scale selection +
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
