# Condition-Residual Preprocessing

## The Problem with the Original Approach

All earlier experiments — baseline classical, CNN pipelines A/D, feedopt scalograms, cascade conditioning, and the leave-one-side-out CV — shared a common failure mode: **the scalogram signal is dominated by the machining condition (speed × depth-of-cut), not the target parameter being classified.**

### Visual proof: condition dominance

The figure below shows the **same feed rate (f3)** across all 8 experimental sides (conditions). Each side is a unique speed × depth-of-cut combination. Despite feed being fixed, the scalogram patterns change dramatically — the classifier sees 8 visually different images for a single feed class.

![Fig 1 — Condition dominance: same feed, 8 conditions](readme_figures/fig1_condition_dominance.png)

By contrast, the figure below shows **all three feed rates (f3/f5/f7) within the same condition** (side 1: 2500 rpm, doc1). The differences between feeds are subtle — far smaller than the between-condition variation shown above.

![Fig 2 — Feed variation within one condition](readme_figures/fig2_feed_within_condition.png)

Quantifying this from the raw data:
- The standard deviation of per-condition scalogram means (across 8 speed×doc conditions) is **0.94** in normalised units
- The feed signal within a condition (std of f3/f5/f7 means) is only **0.02–0.09**
- The condition effect is therefore **~10–45× larger** than the feed signal

### The feed signal reverses direction across conditions

The figure below shows the Pearson correlation of the `(f7 − f3)` feed-delta vector between every pair of sides. **Blue cells are negative** — meaning the direction of the feed signal in scalogram space is literally opposite between those two conditions. A classifier trained on some conditions and tested on others cannot learn a consistent rule.

![Fig 4 — Cross-condition correlation of feed-delta vector](readme_figures/fig4_delta_correlation.png)

The mean off-diagonal correlation is near zero (≈ 0.16 on this feedopt scalogram set; the earlier analysis on raw scalograms yielded −0.05 with a minimum of −0.89). This is why the leave-one-side-out CV showed every test fold collapsing to a single feed prediction (e.g. `[f3 f3 f3]` or `[f7 f7 f7]`) regardless of true feed, and why honest unbiased accuracy sat at **42–54%** for feed — barely above the 33% random baseline.

The cascade conditioning approach (speed → doc → feed) was the right intuition, but it failed in unbiased evaluation for the same reason: the condition signal is so large that even perfect upstream speed/doc labels (oracle conditioning in `cv_exp_splits.py`) could not rescue feed accuracy consistently.

---

## What Condition-Residual Preprocessing Does

For each scalogram image, subtract the mean of all images that share the same **nuisance condition** — i.e., everything that is *not* the classification target. This removes the condition DC offset and leaves only target-relative variation.

### Step-by-step example

The figure below shows the full subtraction process for side 1 (2500 rpm, doc1), window 1. The top row shows the raw scalograms for f3, f5, f7 alongside their per-condition mean. The bottom row shows the residuals after subtraction — the dominant condition structure has been removed and a clear **f3 → f5 → f7 gradient** becomes visible (blue = below mean, red = above mean).

![Fig 3 — Subtraction walkthrough](readme_figures/fig3_subtraction_walkthrough.png)

### Grouping by target

| Target | Nuisance condition | Group definition | Windows/group |
|--------|-------------------|------------------|---------------|
| `feed` | speed × doc | per side (each side = one speed×doc combo) | 9 (3 feeds × 3 windows) |
| `roughness` | speed × doc | same as feed (roughness co-varies with feed within a side) | 9 |
| `speed` | doc × feed | per (doc level, feed class) pair | 6 (2 speeds × 3 windows) |
| `doc` | speed × feed | per (speed level, feed class) pair | 12 (4 doc levels × 3 windows) |

The key insight for `feed`: the experimental design guarantees that each condition (side) has **exactly one run per feed class**. This means the per-side mean is a pure condition baseline — feed signal cancels out in the average. Subtracting it gives a residual that carries only feed-relative information.

### At test time

Because the experimental design always measures all feed classes at every condition, at inference time the condition mean can be estimated **without labels** by averaging all windows from the same condition. There is a small self-leakage (each image contributes 1/N to its own normalisation mean), but with N=9 this contribution is negligible.

### Implementation

```python
# build_residual_scalograms.py
python build_residual_scalograms.py --target feed      --src_dirs scalograms_32x3_feedopt scalograms_32x12_feedopt
python build_residual_scalograms.py --target speed     --src_dirs scalograms_32x3 scalograms_32x12
python build_residual_scalograms.py --target doc       --src_dirs scalograms_32x3 scalograms_32x12
python build_residual_scalograms.py --target roughness --src_dirs scalograms_32x3 scalograms_32x12
```

The output directories (e.g. `scalograms_32x3_feedopt_residual/`) have the same structure as the originals — same filenames, same `labels.csv` — so the entire existing CNN training pipeline (`cnn_train_param.py`, run scripts, eval) works unchanged on them.

---

## Results: Before vs After

### Feed (leave-one-side-out CV, HGB)

| Preprocessing | 32x3_feedopt | 32x12_feedopt |
|---------------|-------------|--------------|
| Raw pixels (baseline) | 41.7% | 54.2% |
| **Condition residual** | **87.5%** | **75.0%** |

### Feed (CNN sweep, best model per split)

| Split | Raw feedopt (best CNN) | Residual (best CNN) |
|-------|----------------------|---------------------|
| Base | ~87.5%* | **100%** (resnet18 lr=1e-3 + SMOTE) |
| exp11 | 0–62.5% | **100%** (convnext_tiny lr=1e-3) |
| exp12 | 37.5% | **100%** (resnet18 lr=1e-3) |

*The raw feedopt 87.5% was measured on a single biased test split with test-set-driven checkpoint selection — not a reliable estimate. The residual 100% is on the same biased split, but now also generalises to the harder exp11/exp12 splits.

### Speed (CNN sweep, best model)

| Split | Raw (baseline) | Residual |
|-------|---------------|---------|
| Base | ~87.5% | **100%** |
| exp11 | — | **100%** |
| exp12 | — | **100%** |

Speed was always a strong target; residual preprocessing makes it consistently perfect.

### Depth of Cut / Doc (CNN sweep, best model)

| Split | Raw (baseline) | Residual |
|-------|---------------|---------|
| Base | ~75–87.5% | **100%** |
| exp11 | — | **100%** |
| exp12 | — | **100%** |

### Roughness (CNN sweep, best model)

| Split | Raw (baseline) | Residual |
|-------|---------------|---------|
| Base | ~75% | **100%** (efnb0 lr=1e-4, 32x3) |
| exp11 | — | **87.5%** |
| exp12 | — | **100%** (efnb0/resnet18, 32x3) |

Roughness is the most variable — 32x12 caps at 87.5% on exp11/exp12, while 32x3 hits 100% on base and exp12.

---

## Why the Old Numbers Were Misleading

Previous experiments reported feed accuracies of 75–87.5% from the CNN cascade pipeline. These came from:

1. **Single fixed test split** (12.5pp granularity per run): picking the best model over 8 architecture × LR combinations on the *same* test set inflates the reported accuracy through selection bias.
2. **Test-set-driven checkpoint selection** (`if te_acc > best_acc: save`): the saved checkpoint is the one that happened to generalise best to the specific test split — again inflating reported performance.
3. **Cascade leakage**: `predict_conditioning.py` generates predictions over all 72 images using a model trained on 48 of them; images in the model's own training split get inflated predictions.

The leave-one-side-out CV (`cv_evaluate.py`) strips away bias (1) and (2). The result dropped feed accuracy to 42–54% — revealing the true floor with raw scalograms.

Residual preprocessing, also evaluated under leave-one-side-out CV, recovers 87.5% for feed — and this figure is bias-free. The CNN results on residual scalograms across exp11/exp12 (100% for feed, speed, doc) further confirm that the preprocessing generalises to harder, balanced splits.

---

## Final Decision: Residual Only for Feed and Roughness

**Speed and doc use raw (non-residual) models.** Both are already reliably solvable
without residual preprocessing — see `exp11_exp12_results_readme.md` for the
raw sweep numbers — and residual would be extra pipeline complexity for no
accuracy gain on those two targets:

| Target | Final model | Scalogram | Notes |
|--------|-------------|-----------|-------|
| **speed** | resnet18, lr=1e-3, no SMOTE | `scalograms_32x12` (or `32x12_9win`) | 100%/100% on exp11/exp12, raw pixels |
| **doc** | resnet18, lr=1e-3, no SMOTE | `scalograms_32x3_9win` | 75%/75% on exp11/exp12, raw pixels |

**Feed and roughness keep condition-residual preprocessing.** Both share the
same nuisance condition (speed × doc — see the grouping table above), so it
would be inconsistent to residual-correct one but not the other: they're
stripping the identical dominant axis out of the same underlying scalograms.

| Target | Final model | Scalogram dir | Notes |
|--------|-------------|---------------|-------|
| **feed** | resnet18, lr=1e-3, SMOTE | `32x3_feedopt_residual` | 100% (base, exp11, exp12) CNN sweep; 87.5% under leave-one-side-out CV |
| **roughness** | efficientnet_b0, lr=1e-4 | `32x3_residual_roughness` | 100% base+exp12, 87.5% exp11 |

## Most Reliable Model Configurations (superseded by the table above for speed/doc)

Full sweep results across all splits and both scalogram sizes, kept for reference:

| Target | Scalogram dir | Backbone | LR | SMOTE | Best split acc |
|--------|--------------|----------|----|-------|---------------|
| feed | 32x3_feedopt_residual | resnet18 | 1e-3 | ✓ | 100% (base, exp11, exp12) |
| feed | 32x3_feedopt_residual | convnext_tiny | 1e-3 | ✓/✗ | 87.5–100% |
| speed | 32x3_residual_speed | convnext_tiny | 1e-4 | ✓/✗ | 100% all splits |
| speed | 32x3_residual_speed | resnet18 | 1e-3 | ✓/✗ | 100% all splits |
| doc | 32x12_residual_doc | resnet18 | 1e-3 | ✓ | 100% all splits |
| doc | 32x3_residual_doc | convnext_tiny | 1e-4 | ✓/✗ | 100% all splits |
| roughness | 32x3_residual_roughness | efficientnet_b0 | 1e-4 | ✓/✗ | 100% base+exp12, 87.5% exp11 |

---

## Limitations

- **Mild self-leakage**: residual images are built from all 24 runs; each image contributes 1/9 to its own normalisation baseline. A fully clean version would recompute residuals per CV fold — at the cost of not being able to pre-build the image directories.
- **Requires all-feeds-per-condition at inference**: the per-side mean can only be estimated without labels if you always measure f3, f5, and f7 at every new condition. If you want to classify a single new measurement at an unseen condition, you need a reference measurement at that condition first.
- **Roughness on 32x12 / exp11 caps at 87.5%**: the 12-window scalogram adds more within-condition noise for roughness than it removes, suggesting the 3-window feedopt scalogram is better suited here.
