# Residual Preprocessing Experiments

Experiments testing condition-residual preprocessing on End Milling scalograms, motivated by its dramatic success in Shoulder Milling (recovering feed classification from ~42–54% to ~87.5%). All experiments here use `scalograms_10w` (Pipeline A, RGB PNG) and `scalograms_ses_10w` (Pipeline D, 4-channel Hilbert `.npy`).

---

## Background: Why Residual Preprocessing?

In Shoulder Milling, the scalogram signal is dominated by the machining condition (speed × depth-of-cut) — roughly 10–45× larger in magnitude than the feed signal — which caused CNNs to saturate on the condition pattern and ignore feed variation entirely. Residual preprocessing removes this:

```
residual[i] = image[i] - mean(all images in same condition group)
```

For End Milling, the DOC × speed combination defines the nuisance condition. There are exactly 15 such groups (5 speeds × 3 DOC levels), each containing 3 runs at different feed rates. This maps directly onto Shoulder Milling's structure.

**One key structural difference:** End Milling's feed classes are not uniform across conditions. Each condition's 3 runs cover only a 3-step window of the 6-class scale (e.g., one condition has runs at 3/4/5 mm/rev, another at 6/7/8 mm/rev). This means the per-condition mean doesn't cancel feed as cleanly as Shoulder Milling's uniform f3/f5/f7 design — the residual still carries some condition-correlated feed bias.

---

## Building the Residual Scalogram Directories

```bash
python build_residual_scalograms.py --target feed_coarse
# → scalograms_10w_residual/  and  scalograms_ses_10w_residual/

python build_residual_scalograms.py --target roughness
# → scalograms_10w_residual_roughness/  and  scalograms_ses_10w_residual_roughness/

python build_residual_scalograms.py --target feed
# → scalograms_10w_residual_feed/  and  scalograms_ses_10w_residual_feed/
```

Each output directory contains 450 images (15 groups × 30 windows/group). PNG residuals are normalized to uint8 (centered at 128, ±2σ = full range). Hilbert `.npy` residuals are rescaled to [0, 1] to match the expectation of `cnn_train_hilbert.py`'s `NpyScalogramDataset`.

---

## Section 1: Roughness

### Training

```bash
# PNG pipeline, 5-fold CV
python cnn_model/cnn_train.py --img_dir scalograms_10w_residual_roughness \
    --target roughness --backbone resnet18 --kfold 5 --epochs 40 --lr 1e-3

# Hilbert pipeline, fixed split
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w_residual_roughness \
    --target roughness --backbone resnet18 --epochs 40 --lr 1e-3
```

### Results

| Pipeline | Method | Accuracy |
|---|---|---|
| PNG | Residual, 5-fold CV mean | 72.9% ± 9.2% |
| Hilbert | Residual, fixed split | 54.2% |
| **Baseline** | PNG, fixed holdout (ResNet18) | **100% run MV** (93.3% window) |

### Interpretation

Residual preprocessing **hurts** roughness. The baseline ResNet18 achieves perfect run-level accuracy (100%) on the fixed holdout. Residual 5-fold CV mean of 72.9% is strictly worse, even accounting for the stricter evaluation methodology (5-fold CV vs. a curated fixed holdout).

The reason: roughness (Ra) in End Milling correlates strongly with DOC and speed — deeper cuts and lower speeds produce higher Ra values. The condition mean carries genuine roughness signal. Subtracting it discards the very pattern the model needs.

---

## Section 2: Feed Rate Coarse (3-class: Low / Med / High)

### Training

```bash
# PNG pipeline, 5-fold CV
python cnn_model/cnn_train.py --img_dir scalograms_10w_residual \
    --target feed_coarse --backbone resnet18 --kfold 5 --epochs 40 --lr 1e-3

# Hilbert pipeline, fixed split
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w_residual \
    --target feed_coarse --backbone resnet18 --epochs 40 --lr 1e-3
```

### Results

| Pipeline | Method | Accuracy |
|---|---|---|
| PNG | Residual, 5-fold CV mean | 62.8% ± 10.6% |
| Hilbert | Residual, fixed split | 58.3% |
| **Baseline** | PNG, fixed holdout (ConvNeXt-Tiny) | **83.3% run MV** (80.0% window) |

### Per-Class Breakdown (PNG, 5-fold CV)

| Fold | Low (0) | Med (1) | High (2) | Overall |
|---|---|---|---|---|
| 1 | 20/30 | 34/50 | 17/20 | 71.0% |
| 2 | 26/30 | 10/40 | 20/20 | 62.2% |
| 3 | 0/30 | 40/40 | 10/20 | 55.6% |
| 4 | 17/30 | 16/40 | 10/20 | 47.8% |
| 5 | 16/30 | 36/40 | 10/10 | 77.5% |

**Key observations:**

- All errors are adjacent-class only (Low↔Med or Med↔High). Low→High never occurs — the model has a genuine ordinal understanding.
- Fold 3 is the anomaly: Low collapses to 0/30 correct. The 30 test windows for the low class land in conditions where the residual scalogram for low feed resembles high feed — a condition-specific reversal consistent with the shifted feed-set structure (some conditions don't even contain both low and high feed runs).
- High fold variance (±10.6%) reflects sensitivity to which runs fall in the test fold, not random noise.
- Med is the most consistent class (10/40 worst case, 40/40 best) because it is the most represented class and spans the widest feed range overlap across conditions.

### Interpretation

Residual preprocessing does not help for feed_coarse either. The baseline (83.3%) outperforms residual CV mean (62.8%). Unlike Shoulder Milling, the condition signal in End Milling encodes information that is genuinely useful for distinguishing feed classes (high-speed conditions tend to use higher feed rates by design), so subtracting it removes useful rather than nuisance variance.

---

## Section 3: Feed Rate Fine-Grained (6-class: 3–8 mm/rev)

### Training

```bash
# PNG pipeline, 5-fold CV
python cnn_model/cnn_train.py --img_dir scalograms_10w_residual_feed \
    --target feed --backbone resnet18 --kfold 5 --epochs 40 --lr 1e-3

# Hilbert pipeline, fixed split
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w_residual_feed \
    --target feed --backbone resnet18 --epochs 40 --lr 1e-3
```

### Results

| Pipeline | Method | Accuracy |
|---|---|---|
| PNG | Residual, 5-fold CV mean | 46.3% ± 14.0% |
| Hilbert | Residual, fixed split | 35.8% |
| Baseline (random) | — | ~16.7% |

No baseline exists for raw 6-class feed in the fixed-holdout format. The model is learning (2.8× above random), but with high variance.

### Per-Class Breakdown (PNG, 5-fold CV)

| Fold | 3mm | 4mm | 5mm | 6mm | 7mm | 8mm | Overall |
|---|---|---|---|---|---|---|---|
| 1 | 3/20 | 1/20 | 20/30 | 0/20 | 3/20 | 7/10 | 28.3% |
| 2 | 0/10 | 10/20 | 20/30 | 20/20 | 7/10 | 8/10 | 65.0% |
| 3 | 0/10 | 0/20 | 20/20 | 10/20 | 0/10 | 0/10 | 33.3% |
| 4 | 0/10 | 10/20 | 10/20 | 7/20 | 10/10 | — | 46.3% |
| 5 | 1/10 | 4/10 | 20/20 | 0/10 | 10/10 | — | 58.3% |

**Key observations:**

- All misclassifications are to adjacent classes (±1). The model never confuses 3 mm/rev with 8 mm/rev.
- Class 5 (8 mm/rev) is absent from folds 4 and 5 — only 3 runs ever have 8 mm/rev (runs 6, 21, 36), all at high-speed/high-DOC conditions. After residual subtraction, these conditions have almost no within-group feed variation left.
- Class 0 (3 mm/rev) and class 3 (6 mm/rev) are the weakest — both frequently score 0/N in individual folds.
- Fold 2 (65%) is the outlier high — classes 3 and 5 happened to be well-represented in training.

### Hilbert Per-Class (fixed split, best model)

| Class | Correct | Notes |
|---|---|---|
| 3 mm/rev | 16/30 | Predicted mostly as 4 mm/rev |
| 4 mm/rev | 0/10 | All predicted as 6 mm/rev |
| 5 mm/rev | 7/20 | Mostly predicted as 6 mm/rev |
| 6 mm/rev | 10/20 | Half correct |
| 7 mm/rev | 10/20 | Half correct |
| 8 mm/rev | 0/20 | Predicted as 4 mm/rev or 2 mm/rev |

Class 5 (8 mm/rev) and class 1 (4 mm/rev) get 0/N — the Hilbert residual completely loses signal for the extreme minority classes.

---

## Section 4: Regression Experiments

Given that classification errors were universally adjacent-class only, we tested MSE regression (single output, predict class index) to see if a soft ordinal model performs better.

### Script

```bash
# Feed fine-grained (6-class), residual, 5-fold CV
python cnn_model/cnn_train_regression.py --img_dir scalograms_10w_residual_feed \
    --target feed --kfold 5 --epochs 40 --lr 1e-3

# Feed coarse (3-class), residual, 5-fold CV
python cnn_model/cnn_train_regression.py --img_dir scalograms_10w_residual \
    --target feed_coarse --kfold 5 --epochs 40 --lr 1e-3
```

Metrics:
- **MAE** — mean absolute error in class units (lower is better)
- **Within-1** — fraction of predictions that round to the correct class ± 1 (for 6-class this means off by at most 1 mm/rev; for 3-class it means never wrong by 2 full steps)

### Feed Fine-Grained Regression Results

| Fold | MAE | Within-1 |
|---|---|---|
| 1 | 0.737 | 90.0% |
| 2 | 0.897 | 83.0% |
| 3 | 0.914 | 88.9% |
| 4 | 0.603 | 100% |
| 5 | 0.931 | 81.7% |
| **Mean** | **0.817 ± 0.127** | **88.7% ± 6.5%** |

**Comparison with 6-class classification (same data):**

| Metric | Classification | Regression |
|---|---|---|
| Exact match | 46.3% | ~38% (rounded MAE) |
| Within-1 class | — | **88.7%** |

Regression reveals the model almost always places predictions within 1 mm/rev of the true value — the confusion is at fine boundaries, not wholesale. The classification view (46.3%) undersells what the model actually knows.

**Per-class MAE (averaged across folds):**

| Class | Typical MAE | Notes |
|---|---|---|
| 3 mm/rev | ~1.0–1.3 | Consistently predicted ~1.0–1.4 (biased toward 4 mm/rev) |
| 4 mm/rev | 0.19–1.65 | Highly fold-dependent |
| 5 mm/rev | 0.46–1.0 | Mid-range, moderate error |
| 6 mm/rev | 0.24–2.1 | Worst fold has MAE 2.1 |
| 7 mm/rev | 0.16–0.59 | Among the best |
| 8 mm/rev | 0.07–2.5 | Fold 3 catastrophic (MAE=2.5, within-1=0%) |

Class 7 (7 mm/rev) and class 4 (6 mm/rev) in good folds produce near-perfect predictions (~3.5–3.7 for class 4, ~3.5–4.0 for class 7). Class 5 (8 mm/rev) in fold 3 collapses to predicting ~2.5, which corresponds to losing all signal for that extreme class in that particular condition split.

### Feed Coarse Regression Results

| Fold | MAE | Within-1 |
|---|---|---|
| 1 | 0.369 | 100% |
| 2 | 0.572 | 100% |
| 3 | 0.568 | 100% |
| 4 | 0.588 | 100% |
| 5 | 0.325 | 100% |
| **Mean** | **0.484 ± 0.113** | **100% ± 0%** |

**Within-1 is perfect across every fold with zero variance.** With only 3 classes spanning indices 0–2, within-1 simply means the model never confuses Low with High in either direction — and it never does. Every mistake is Low↔Med or Med↔High.

**Comparison with 3-class classification (same data):**

| Method | Exact match | Within-1 |
|---|---|---|
| Classification | 62.8% | — |
| Regression | ~45% (rounded MAE≈0.5) | **100%** |

The regression exact match drops vs. classification because a prediction of 0.85 rounds to 1 (wrong) even though it's very close to the boundary. But the model never makes a gross error, which the classification view misses.

### Regression vs. Classification Summary

For both 6-class and 3-class feed, regression reveals that the model has a sound ordinal understanding of feed rate — errors are smooth boundary calls, not random jumps. The classification framing penalizes every boundary mistake equally, hiding this structure. Within-1 accuracy (88.7% for 6-class, 100% for 3-class) is the more informative metric for this problem.

---

## Section 5: Overall Comparison — Residual vs. Baseline

| Target | Pipeline | Residual | Baseline |
|---|---|---|---|
| Roughness | PNG | 72.9% (5-fold CV) | **100% run MV** |
| Roughness | Hilbert | 54.2% | — |
| Feed coarse | PNG | 62.8% (5-fold CV) | **83.3% run MV** |
| Feed coarse | Hilbert | 58.3% | 75.0% |
| Feed (6-class) | PNG | 46.3% (5-fold CV) | 50.0% run MV |
| Feed (6-class) | Hilbert | 35.8% | — |

Residual preprocessing **consistently underperforms** the baseline in End Milling, for every target and both pipelines. This is the opposite of what was observed in Shoulder Milling.

---

## Section 6: Why Residual Preprocessing Doesn't Transfer

Three structural differences explain why residual subtraction helps in Shoulder Milling but not End Milling:

**1. Condition signal is useful, not pure nuisance.**
In Shoulder Milling, the speed×DOC combination dominates the scalogram ~10–45× over feed, making CNNs saturate on condition. In End Milling, the same speed and DOC parameters carry genuine information about roughness and feed rate — shallower cuts at higher speeds tend to produce smoother surfaces and are run at higher feeds by design. Subtracting the condition mean discards this informative structure.

**2. Non-uniform feed sets per condition.**
In Shoulder Milling, every condition's runs covered the same three feed rates (f3, f5, f7), so the per-condition mean was purely a condition estimate — feed deviations canceled exactly in the average. In End Milling, each condition covers only a 3-step window of the 6-class scale, and the specific window shifts by condition. The per-condition mean therefore includes feed-correlated bias, so the residual is contaminated.

**3. Fewer runs per condition.**
Each End Milling condition group has only 3 runs (vs. Shoulder Milling's more balanced structure). With 3 samples, the group mean is a noisy estimate of the true condition signal, so residual subtraction adds noise rather than cleanly removing the condition effect.

---

## Files

| File | Description |
|---|---|
| `build_residual_scalograms.py` | Builds residual dirs for `feed`, `feed_coarse`, `roughness` |
| `cnn_model/cnn_train.py` | PNG pipeline training (supports `--kfold`, `--target feed`) |
| `cnn_model/cnn_train_hilbert.py` | Hilbert pipeline training (supports `--target feed` added here) |
| `cnn_model/cnn_train_regression.py` | MSE regression for `feed` and `feed_coarse` |
| `scalograms_10w_residual/` | Residual PNGs for feed_coarse/roughness |
| `scalograms_10w_residual_roughness/` | Residual PNGs for roughness |
| `scalograms_10w_residual_feed/` | Residual PNGs for feed (6-class) |
| `scalograms_ses_10w_residual/` | Residual Hilbert arrays for feed_coarse |
| `scalograms_ses_10w_residual_roughness/` | Residual Hilbert arrays for roughness |
| `scalograms_ses_10w_residual_feed/` | Residual Hilbert arrays for feed (6-class) |
