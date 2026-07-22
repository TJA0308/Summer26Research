# Steel Milling Vibration Analysis

Classifies steel milling process parameters (spindle speed, depth of cut, feed rate) from raw vibration signals using CNN-based scalogram classification.

## Data

45 runs recorded at 16,393 Hz with three sensor channels: ai4 (feed-axis vibration), ai5 (cross-axis, unused), and ai6 (acoustic). Each run is ~65,000 samples (~4 seconds). Run parameters come from `steel Milling Signal files and Surface Roughness.xlsx`.

| Runs | stlml files | DOC (mm) | Speed | Feed rates (mm/rev) |
|------|-------------|----------|-------|---------------------|
| run1–run3   | stlml_10–12 | 0.015 | 4000 rpm | 5, 6, 7 |
| run4–run6   | stlml_13–15 | 0.015 | 5000 rpm | 6, 7, 8 |
| run7–run9   | stlml_16–18 | 0.030 | 1500 rpm | 3, 4, 5 |
| run10–run12 | stlml_19–21 | 0.030 | 2000 rpm | 3, 4, 5 |
| run13–run15 | stlml_22–24 | 0.030 | 3000 rpm | 4, 5, 6 |
| run16–run18 | stlml_25–27 | 0.030 | 4000 rpm | 5, 6, 7 |
| run19–run21 | stlml_28–30 | 0.030 | 5000 rpm | 6, 7, 8 |
| run22–run24 | stlml_31–33 | 0.060 | 1500 rpm | 3, 4, 5 |
| run25–run27 | stlml_34–36 | 0.060 | 2000 rpm | 3, 4, 5 |
| run28–run30 | stlml_37–39 | 0.060 | 3000 rpm | 4, 5, 6 |
| run31–run33 | stlml_40–42 | 0.060 | 4000 rpm | 5, 6, 7 |
| run34–run36 | stlml_43–45 | 0.060 | 5000 rpm | 6, 7, 8 |
| run37–run39 | stlml_1–3   | 0.015 | 1500 rpm | 3, 4, 5 |
| run40–run42 | stlml_4–6   | 0.015 | 2000 rpm | 3, 4, 5 |
| run43–run45 | stlml_7–9   | 0.015 | 3000 rpm | 4, 5, 6 |

## Trained Models

Five models are saved in the project root:

| File | Predicts | Classes | Test Accuracy | Scalogram dir needed |
|------|----------|---------|---------------|----------------------|
| `model_speed.pt` | Spindle speed | 5 (1500–5000 rpm) | **100%** | `scalograms_ai4_ai6` |
| `model_doc.pt` | Depth of cut | 3 (0.015/0.030/0.060 mm) | **100%** | `scalograms_ai4_ai6` |
| `model_feed_coarse.pt` | Feed rate (coarse) | 3 (low/med/high) | **66.7%** | `scalograms_ai4_ai6` |
| `model_feed.pt` | Feed rate (fine) | 6 (3–8 mm/rev) | **50%** | `scalograms_ai4_ai6_4w` |
| `model_roughness.pt` | Surface roughness (Ra) | 3 (smooth/medium/rough) | **83.3%** | `scalograms_ai4_ai6` |

## Multi-Architecture Experiments (10-window CWT + SMOTE)

Systematic search over backbone architectures and data strategies using 10-window scalograms (`scalograms_10w`) with signal-space SMOTE augmentation. Models saved in `exp_models/` (speed and DOC models saved to project root). All accuracy figures are holdout test-only — test runs were never used to update weights. See `RESULTS.md` for confusion matrices and window-level breakdowns.

### Spindle Speed (5-class, 35 train / 10 test runs)

| Model file | Backbone | Window Acc | Run Majority-Vote | Soft Avg |
|------------|----------|-----------|-------------------|----------|
| `speed_cnxt_10w.pt` | ConvNeXt-Tiny | **96.0%** | **100.0%** | **100.0%** |
| `speed_resnet_10w.pt` | ResNet18 | 90.0% | **100.0%** | **100.0%** |

**SMOTE augmentation** (`smote_speed_labels.csv`) — 4 synthetic runs added:

| Class | Real runs | Synthetic added | Total runs | Total images |
|-------|-----------|----------------|------------|--------------|
| 1500 rpm | 7 | 1 | 8 | 80 |
| 2000 rpm | 7 | 1 | 8 | 80 |
| 3000 rpm | 7 | 1 | 8 | 80 |
| 4000 rpm | 7 | 1 | 8 | 80 |
| 5000 rpm | 7 | 0 | 7 | 70 |
| **Total** | **35** | **4** | **39** | **390** |

Speed was nearly balanced before SMOTE (7 runs/class). 4 synthetic runs were added to classes 0–3; 5000 rpm was not augmented, leaving it with 70 training images vs 80 for the others.

**Window majority-vote** — `speed_cnxt_10w.pt` (ConvNeXt-Tiny):

| Run | True | Predicted | Result | Window votes |
|-----|------|-----------|--------|--------------|
| run9  | 1500 rpm | 1500 rpm | **OK** | 1500×10 |
| run22 | 1500 rpm | 1500 rpm | **OK** | 1500×10 |
| run12 | 2000 rpm | 2000 rpm | **OK** | 2000×10 |
| run27 | 2000 rpm | 2000 rpm | **OK** | 2000×10 |
| run15 | 3000 rpm | 3000 rpm | **OK** | 3000×10 |
| run28 | 3000 rpm | 3000 rpm | **OK** | 3000×10 |
| run2  | 4000 rpm | 4000 rpm | **OK** | 4000×10 |
| run16 | 4000 rpm | 4000 rpm | **OK** | 4000×6, 2000×4 |
| run5  | 5000 rpm | 5000 rpm | **OK** | 5000×10 |
| run36 | 5000 rpm | 5000 rpm | **OK** | 5000×10 |

**Whole-run probability averaging** — `speed_cnxt_10w.pt` (ConvNeXt-Tiny) — **100.0% (10/10)**:

| Run | True | Predicted | Result | Avg prob (top 2) |
|-----|------|-----------|--------|------------------|
| run9  | 1500 rpm | 1500 rpm | **OK** | 1500=1.000, 5000=0.000 |
| run22 | 1500 rpm | 1500 rpm | **OK** | 1500=0.991, 5000=0.009 |
| run12 | 2000 rpm | 2000 rpm | **OK** | 2000=1.000, 3000=0.000 |
| run27 | 2000 rpm | 2000 rpm | **OK** | 2000=1.000, 1500=0.000 |
| run15 | 3000 rpm | 3000 rpm | **OK** | 3000=0.850, 5000=0.142 |
| run28 | 3000 rpm | 3000 rpm | **OK** | 3000=0.999, 5000=0.000 |
| run2  | 4000 rpm | 4000 rpm | **OK** | 4000=1.000, 3000=0.000 |
| run16 | 4000 rpm | 4000 rpm | **OK** | 4000=0.553, 2000=0.419 |
| run5  | 5000 rpm | 5000 rpm | **OK** | 5000=0.999, 1500=0.000 |
| run36 | 5000 rpm | 5000 rpm | **OK** | 5000=0.999, 1500=0.001 |

**Window majority-vote** — `speed_resnet_10w.pt` (ResNet18):

| Run | True | Predicted | Result | Window votes |
|-----|------|-----------|--------|--------------|
| run9  | 1500 rpm | 1500 rpm | **OK** | 1500×10 |
| run22 | 1500 rpm | 1500 rpm | **OK** | 1500×6, 3000×4 |
| run12 | 2000 rpm | 2000 rpm | **OK** | 2000×10 |
| run27 | 2000 rpm | 2000 rpm | **OK** | 2000×9, 1500×1 |
| run15 | 3000 rpm | 3000 rpm | **OK** | 3000×10 |
| run28 | 3000 rpm | 3000 rpm | **OK** | 3000×6, 1500×4 |
| run2  | 4000 rpm | 4000 rpm | **OK** | 4000×10 |
| run16 | 4000 rpm | 4000 rpm | **OK** | 4000×9, 2000×1 |
| run5  | 5000 rpm | 5000 rpm | **OK** | 5000×10 |
| run36 | 5000 rpm | 5000 rpm | **OK** | 5000×10 |

**Whole-run probability averaging** — `speed_resnet_10w.pt` (ResNet18) — **100.0% (10/10)**:

| Run | True | Predicted | Result | Avg prob (top 2) |
|-----|------|-----------|--------|------------------|
| run9  | 1500 rpm | 1500 rpm | **OK** | 1500=0.874, 3000=0.101 |
| run22 | 1500 rpm | 1500 rpm | **OK** | 1500=0.517, 3000=0.465 |
| run12 | 2000 rpm | 2000 rpm | **OK** | 2000=0.998, 3000=0.002 |
| run27 | 2000 rpm | 2000 rpm | **OK** | 2000=0.910, 1500=0.076 |
| run15 | 3000 rpm | 3000 rpm | **OK** | 3000=0.986, 2000=0.011 |
| run28 | 3000 rpm | 3000 rpm | **OK** | 3000=0.674, 1500=0.298 |
| run2  | 4000 rpm | 4000 rpm | **OK** | 4000=1.000, 2000=0.000 |
| run16 | 4000 rpm | 4000 rpm | **OK** | 4000=0.855, 2000=0.094 |
| run5  | 5000 rpm | 5000 rpm | **OK** | 5000=1.000, 1500=0.000 |
| run36 | 5000 rpm | 5000 rpm | **OK** | 5000=0.999, 3000=0.001 |

Both models get all 10 runs correct under both methods. The probability scores reveal where each model is uncertain: run16 (4000 rpm, DOC=0.030) is marginal on ConvNeXt (4000=0.553 vs 2000=0.419), and run22 (1500 rpm, DOC=0.060) is marginal on ResNet18 (1500=0.517 vs 3000=0.465).

---

### Depth of Cut (3-class: 0.015 / 0.030 / 0.060 mm, 36 train / 9 test runs)

| Model file | Backbone | Window Acc | Run Majority-Vote | Soft Avg |
|------------|----------|-----------|-------------------|----------|
| `best_model_doc_resnet18.pt` | ResNet18 | **82.2%** | **88.9%** | **88.9%** |
| `best_model_doc_convnext.pt` | ConvNeXt-Tiny | 77.8% | 77.8% | 77.8% |

**SMOTE augmentation** (`smote_doc_labels.csv`) — applied before training to balance the DOC classes.

**Window majority-vote and whole-run probability averaging** — `best_model_doc_resnet18.pt` (ResNet18, best):

| Run | True | Predicted | Result | Window votes / Avg prob (top 2) |
|-----|------|-----------|--------|---------------------------------|
| run1  | 0.015 mm | 0.015 mm | **OK**    | 0.015×10 / 0.015=0.974, 0.030=0.016 |
| run5  | 0.015 mm | 0.015 mm | **OK**    | 0.015×10 / 0.015=1.000, 0.030=0.000 |
| run43 | 0.015 mm | 0.015 mm | **OK**    | 0.015×10 / 0.015=0.998, 0.030=0.002 |
| run7  | 0.030 mm | 0.030 mm | **OK**    | 0.030×10 / 0.030=0.990, 0.015=0.009 |
| run14 | 0.030 mm | 0.030 mm | **OK**    | 0.030×10 / 0.030=0.884, 0.015=0.089 |
| run19 | 0.030 mm | 0.030 mm | **OK**    | 0.030×6, 0.015×4 / 0.030=0.558, 0.015=0.389 |
| run22 | 0.060 mm | 0.060 mm | **OK**    | 0.060×9, 0.015×1 / 0.060=0.848, 0.015=0.104 |
| run29 | 0.060 mm | 0.060 mm | **OK**    | 0.060×9, 0.015×1 / 0.060=0.885, 0.015=0.092 |
| run36 | 0.060 mm | 0.030 mm | **WRONG** | 0.030×10 / 0.030=0.943, 0.060=0.055 |

**Window majority-vote and whole-run probability averaging** — `best_model_doc_convnext.pt` (ConvNeXt-Tiny):

| Run | True | Predicted | Result | Window votes / Avg prob (top 2) |
|-----|------|-----------|--------|---------------------------------|
| run1  | 0.015 mm | 0.015 mm | **OK**    | 0.015×10 / 0.015=0.747, 0.060=0.140 |
| run5  | 0.015 mm | 0.015 mm | **OK**    | 0.015×10 / 0.015=0.857, 0.060=0.084 |
| run43 | 0.015 mm | 0.015 mm | **OK**    | 0.015×10 / 0.015=0.510, 0.060=0.301 |
| run7  | 0.030 mm | 0.030 mm | **OK**    | 0.030×10 / 0.030=0.884, 0.060=0.112 |
| run14 | 0.030 mm | 0.030 mm | **OK**    | 0.030×10 / 0.030=0.820, 0.060=0.146 |
| run19 | 0.030 mm | 0.015 mm | **WRONG** | 0.015×10 / 0.015=0.496, 0.060=0.307 |
| run22 | 0.060 mm | 0.060 mm | **OK**    | 0.060×10 / 0.060=0.832, 0.030=0.147 |
| run29 | 0.060 mm | 0.060 mm | **OK**    | 0.060×10 / 0.060=0.958, 0.030=0.041 |
| run36 | 0.060 mm | 0.015 mm | **WRONG** | 0.015×10 / 0.015=0.373, 0.060=0.330 |

ResNet18 makes a single confident failure on run36 (5000 rpm, 0.060 mm — p=0.943 for 0.030 mm). ConvNeXt-Tiny fails on both 5000 rpm runs in the medium and deep DOC classes (run19 and run36). The 0.015 mm class is perfectly separated by both models.

---

### Feed Rate Fine-Grained (6-class, 39 train / 6 test runs)

| Model file | Backbone | Window Acc | Run Majority-Vote | Soft Avg |
|------------|----------|-----------|-------------------|----------|
| `exp_models/feed_rn18_10w_adamw.pt` | ResNet18 | **48.3%** | 50.0% | 50.0% |
| `feed_cnxt_10w_adamw.pt` | ConvNeXt-Tiny | 43.3% | 50.0% | 50.0% |
| `exp_models/feed_effb0_10w_adamw.pt` | EfficientNet-B0 | 38.3% | 50.0% | 50.0% |

**SMOTE augmentation** (`smote_labels.csv`) — 27 synthetic runs added:

| Class | Real runs | Synthetic added | Total runs | Total images |
|-------|-----------|----------------|------------|--------------|
| 3 mm/rev | 5 | 6 | 11 | 110 |
| 4 mm/rev | 8 | 3 | 11 | 110 |
| 5 mm/rev | 11 | 0 | 11 | 110 |
| 6 mm/rev | 8 | 3 | 11 | 110 |
| 7 mm/rev | 5 | 6 | 11 | 110 |
| 8 mm/rev | 2 | 9 | 11 | 110 |
| **Total** | **39** | **27** | **66** | **660** |

Pre-SMOTE the dataset was severely imbalanced: 8 mm/rev had only 2 training runs (20 images) vs 11 for 5 mm/rev (110 images). SMOTE brought all 6 classes to 11 runs / 110 images by adding up to 9 synthetic runs to the most underrepresented class.

**Window majority-vote** — `feed_rn18_10w_adamw.pt` (ResNet18, best window acc):

| Run | True | Predicted | Result | Window votes |
|-----|------|-----------|--------|--------------|
| run25 | 3 mm/rev | 3 mm/rev | **OK**    | 3×10 |
| run13 | 4 mm/rev | 6 mm/rev  | **WRONG** | 6×10 |
| run31 | 5 mm/rev | 5 mm/rev  | **OK**    | 5×9, 6×1 |
| run17 | 6 mm/rev | 5 mm/rev  | **WRONG** | 5×10 |
| run5  | 7 mm/rev | 6 mm/rev  | **WRONG** | 6×10 |
| run36 | 8 mm/rev | 8 mm/rev  | **OK**    | 8×10 |

**Whole-run probability averaging** — `feed_rn18_10w_adamw.pt` (ResNet18) — **50.0% (3/6)**:

| Run | True | Predicted | Result | Avg prob (top 2) |
|-----|------|-----------|--------|------------------|
| run25 | 3 mm/rev | 3 mm/rev | **OK**    | 3=0.659, 4=0.276 |
| run13 | 4 mm/rev | 6 mm/rev  | **WRONG** | 6=1.000, 5=0.000 |
| run31 | 5 mm/rev | 5 mm/rev  | **OK**    | 5=0.724, 6=0.254 |
| run17 | 6 mm/rev | 5 mm/rev  | **WRONG** | 5=0.961, 7=0.029 |
| run5  | 7 mm/rev | 6 mm/rev  | **WRONG** | 6=0.979, 8=0.021 |
| run36 | 8 mm/rev | 8 mm/rev  | **OK**    | 8=0.888, 5=0.064 |

**Window majority-vote** — `feed_cnxt_10w_adamw.pt` (ConvNeXt-Tiny):

| Run | True | Predicted | Result | Window votes |
|-----|------|-----------|--------|--------------|
| run25 | 3 mm/rev | 3 mm/rev | **OK**    | 3×9, 5×1 |
| run13 | 4 mm/rev | 6 mm/rev  | **WRONG** | 6×10 |
| run31 | 5 mm/rev | 5 mm/rev  | **OK**    | 5×7, 6×3 |
| run17 | 6 mm/rev | 7 mm/rev  | **WRONG** | 7×7, 5×2, 3×1 |
| run5  | 7 mm/rev | 6 mm/rev  | **WRONG** | 6×10 |
| run36 | 8 mm/rev | 8 mm/rev  | **OK**    | 8×10 |

**Whole-run probability averaging** — `feed_cnxt_10w_adamw.pt` (ConvNeXt-Tiny) — **50.0% (3/6)**:

| Run | True | Predicted | Result | Avg prob (top 2) |
|-----|------|-----------|--------|------------------|
| run25 | 3 mm/rev | 3 mm/rev | **OK**    | 3=0.841, 4=0.091 |
| run13 | 4 mm/rev | 6 mm/rev  | **WRONG** | 6=1.000, 5=0.000 |
| run31 | 5 mm/rev | 5 mm/rev  | **OK**    | 5=0.581, 6=0.371 |
| run17 | 6 mm/rev | 7 mm/rev  | **WRONG** | 7=0.642, 5=0.210 |
| run5  | 7 mm/rev | 6 mm/rev  | **WRONG** | 6=1.000, 5=0.000 |
| run36 | 8 mm/rev | 8 mm/rev  | **OK**    | 8=0.998, 7=0.002 |

**Window majority-vote** — `feed_effb0_10w_adamw.pt` (EfficientNet-B0):

| Run | True | Predicted | Result | Window votes |
|-----|------|-----------|--------|--------------|
| run25 | 3 mm/rev | 3 mm/rev | **OK**    | 3×8, 5×2 |
| run13 | 4 mm/rev | 6 mm/rev  | **WRONG** | 6×6, 5×4 |
| run31 | 5 mm/rev | 5 mm/rev  | **OK**    | 5×6, 6×4 |
| run17 | 6 mm/rev | 5 mm/rev  | **WRONG** | 5×10 |
| run5  | 7 mm/rev | 6 mm/rev  | **WRONG** | 6×10 |
| run36 | 8 mm/rev | 8 mm/rev  | **OK**    | 8×9, 7×1 |

**Whole-run probability averaging** — `feed_effb0_10w_adamw.pt` (EfficientNet-B0) — **50.0% (3/6)**:

| Run | True | Predicted | Result | Avg prob (top 2) |
|-----|------|-----------|--------|------------------|
| run25 | 3 mm/rev | 3 mm/rev | **OK**    | 3=0.815, 5=0.121 |
| run13 | 4 mm/rev | 6 mm/rev  | **WRONG** | 6=0.509, 5=0.342 |
| run31 | 5 mm/rev | 5 mm/rev  | **OK**    | 5=0.618, 6=0.351 |
| run17 | 6 mm/rev | 5 mm/rev  | **WRONG** | 5=0.870, 6=0.060 |
| run5  | 7 mm/rev | 6 mm/rev  | **WRONG** | 6=0.999, 7=0.000 |
| run36 | 8 mm/rev | 8 mm/rev  | **OK**    | 8=0.773, 7=0.155 |

All three architectures correctly classify run25, run31, and run36 and fail run13 and run5 under both methods — the wrong predictions are highly confident. ConvNeXt-Tiny shifts the run17 failure from 5 mm/rev to 7 mm/rev. Probability averaging does not recover any additional runs compared to majority voting across any architecture.

---

### Feed Rate Coarse (3-class: low/med/high, 39 train / 6 test runs)

| Model file | Backbone | Window Acc | Run Majority-Vote | Soft Avg |
|------------|----------|-----------|-------------------|----------|
| `feed_coarse_cnxt_10w_adamw.pt` | ConvNeXt-Tiny | **80.0%** | **83.3%** | **83.3%** |
| `exp_models/feed_coarse_rn18_10w_adamw.pt` | ResNet18 | 66.7% | 66.7% | 66.7% |
| `exp_models/feed_coarse_effb0_10w_adamw.pt` | EfficientNet-B0 | 66.7% | 66.7% | 66.7% |

**SMOTE augmentation** (`smote_feed_coarse_labels.csv`) — 18 synthetic runs added:

| Class | Real runs | Synthetic added | Total runs | Total images |
|-------|-----------|----------------|------------|--------------|
| low (3-4 mm/rev)    | 13 | 6  | 19 | 190 |
| medium (5-6 mm/rev) | 19 | 0  | 19 | 190 |
| high (7-8 mm/rev)   | 7  | 12 | 19 | 190 |
| **Total** | **39** | **18** | **57** | **570** |

Pre-SMOTE the high class had only 7 training runs vs 19 for medium. SMOTE added 12 synthetic runs to high and 6 to low, bringing all three classes to exactly 19 runs / 190 images.

**Window majority-vote and whole-run probability averaging** — `feed_coarse_cnxt_10w_adamw.pt` (ConvNeXt-Tiny, best — **83.3%**):

| Run | True | Predicted | Result | Window votes / Avg prob (top 2) |
|-----|------|-----------|--------|---------------------------------|
| run25 | low (3-4)    | low    | **OK**    | low×10 / low=0.689, med=0.311 |
| run13 | low (3-4)    | high   | **WRONG** | high×10 / high=0.973, med=0.027 |
| run31 | medium (5-6) | medium | **OK**    | med×10 / med=0.947, low=0.052 |
| run17 | medium (5-6) | medium | **OK**    | med×10 / med=0.928, high=0.064 |
| run36 | high (7-8)   | high   | **OK**    | high×10 / high=0.988, med=0.012 |
| run5  | high (7-8)   | high   | **OK**    | high×8, med×2 / high=0.828, med=0.171 |

**Window majority-vote and whole-run probability averaging** — ResNet18 and EfficientNet-B0 produce identical predictions (**66.7%** each):

| Run | True | Predicted | Result | ResNet votes / prob | EfficientNet votes / prob |
|-----|------|-----------|--------|---------------------|--------------------------|
| run25 | low (3-4)    | low    | **OK**    | low×10 / low=0.898 | low×10 / low=0.960 |
| run13 | low (3-4)    | medium | **WRONG** | med×10 / med=0.989 | med×10 / med=1.000 |
| run31 | medium (5-6) | medium | **OK**    | med×10 / med=0.999 | med×10 / med=0.935 |
| run17 | medium (5-6) | medium | **OK**    | med×10 / med=0.974 | med×10 / med=0.978 |
| run36 | high (7-8)   | high   | **OK**    | high×10 / high=0.990 | high×10 / high=0.989 |
| run5  | high (7-8)   | medium | **WRONG** | med×10 / med=0.923 | med×10 / med=1.000 |

ConvNeXt-Tiny fixes run5 (7 mm/rev, high) which both other models fail, pushing run-level accuracy to 83.3%. It fails run13 (4 mm/rev, low) with a larger error (predicted high, p=0.973) vs ResNet18/EfficientNet-B0 which predict medium. Medium class is perfectly separated across all architectures.

---

### Surface Roughness Ra (3-class, 39 train / 6 test runs, SMOTE-balanced)

| Model file | Backbone | Window Acc | Run Majority-Vote |
|------------|----------|-----------|-------------------|
| `exp_models/roughness_rn18_10w_adamw.pt` | ResNet18 | **93.3%** | **100.0%** |
| `exp_models/roughness_effb0_10w_adamw.pt` | EfficientNet-B0 | 83.3% | — |

**SMOTE augmentation** (`smote_roughness_labels.csv`) — 24 synthetic runs added:

| Class | Real runs | Synthetic added | Total runs | Total images |
|-------|-----------|----------------|------------|--------------|
| Smooth (Ra<0.7)  | 21 | 0  | 21 | 210 |
| Medium (0.7-1.0) | 9  | 12 | 21 | 210 |
| Rough (Ra>1.0)   | 9  | 12 | 21 | 210 |
| **Total** | **39** | **24** | **63** | **630** |

Pre-SMOTE Smooth dominated with 21 training runs vs only 9 each for Medium and Rough (2.3× imbalance). SMOTE added 12 synthetic runs to each minority class, bringing all three to 21 runs / 210 images.

**Window majority-vote** — `roughness_rn18_10w_adamw.pt` (ResNet18, best):

| Run | True | Ra (μm) | Predicted | Result | Window votes |
|-----|------|---------|-----------|--------|--------------|
| run5  | Smooth | 0.424 | Smooth | **OK** | Smooth×10 |
| run43 | Smooth | 0.364 | Smooth | **OK** | Smooth×10 |
| run7  | Medium | 0.930 | Medium | **OK** | Medium×10 |
| run27 | Medium | 0.868 | Medium | **OK** | Medium×7, Rough×3 |
| run22 | Rough  | 1.186 | Rough  | **OK** | Rough×10 |
| run34 | Rough  | 2.084 | Rough  | **OK** | Rough×9, Medium×1 |

**Whole-run probability averaging** — `roughness_rn18_10w_adamw.pt` (ResNet18) — **100.0% (6/6)**:

| Run | True | Ra (μm) | Predicted | Result | Avg prob (top 2) |
|-----|------|---------|-----------|--------|------------------|
| run5  | Smooth | 0.424 | Smooth | **OK** | Smooth=0.999, Medium=0.000 |
| run43 | Smooth | 0.364 | Smooth | **OK** | Smooth=1.000, Rough=0.000 |
| run7  | Medium | 0.930 | Medium | **OK** | Medium=0.998, Smooth=0.001 |
| run27 | Medium | 0.868 | Medium | **OK** | Medium=0.621, Rough=0.375 |
| run22 | Rough  | 1.186 | Rough  | **OK** | Rough=0.798, Medium=0.170 |
| run34 | Rough  | 2.084 | Rough  | **OK** | Rough=0.760, Medium=0.238 |

All 6 runs correctly classified under both methods. Probability averaging makes the boundary uncertainty visible: run27 (Medium, Ra=0.868 μm) averages to Medium=0.621 vs Rough=0.375 — a soft 62/38 split that majority vote would also handle correctly if inverted. Exceeds the 70% target.

---

## Pipeline A & D — Systematic Sweep (128 models)

Systematic search over four backbone architectures, two learning rates, two data pipelines, and with/without SMOTE. All models use 10-window scalograms and the same held-out test runs; only training data differs between pipelines.

- **Pipeline A** — standard RGB CWT scalograms (`scalograms_10w`) with and without signal-space SMOTE. 64 models (4 targets × 4 backbones × 2 LRs × 2). SMOTE models: `exp_models_a/`, results: `exp_results_a/`. No-SMOTE results: `exp_results_v2/` (prefix `std_`).
- **Pipeline D** — SES 4-channel scalograms (`scalograms_ses_10w`) with and without SMOTE. 64 models (4 targets × 4 backbones × 2 LRs × 2). Models: `exp_models_d/`, results: `exp_results_d/`.

**Backbone key:** `rn18` = ResNet-18, `rn50` = ResNet-50, `enb0` = EfficientNet-B0, `cnxt` = ConvNeXt-Tiny. **LR key:** `lr1e3` = 1e-3, `lr1e4` = 1e-4. Win = window accuracy (10 windows × N test runs); Run = majority-vote run accuracy.

---

### Spindle Speed (5-class, 15 test runs)

#### Pipeline A — Standard RGB CWT (±SMOTE)

| Backbone | LR | No-SMOTE Win | No-SMOTE Run | SMOTE Win | SMOTE Run |
|----------|----|-------------|-------------|-----------|-----------|
| ResNet-18 | 1e-3 | 91.3% | 93.3% | **98.0%** | **100.0%** |
| ResNet-18 | 1e-4 | 92.0% | 93.3% | 93.3% | 93.3% |
| ResNet-50 | 1e-3 | **100.0%** | **100.0%** | **98.7%** | **100.0%** |
| ResNet-50 | 1e-4 | 96.7% | **100.0%** | 89.3% | 86.7% |
| EfficientNet-B0 | 1e-3 | 91.3% | 93.3% | 83.3% | 86.7% |
| EfficientNet-B0 | 1e-4 | 86.7% | 93.3% | 92.7% | 93.3% |
| ConvNeXt-Tiny | 1e-3 | 20.0% | 20.0% | 20.0% | 20.0% |
| ConvNeXt-Tiny | 1e-4 | 90.0% | 93.3% | 91.3% | 93.3% |

ConvNeXt-Tiny collapses at lr=1e-3 regardless of SMOTE. ResNet-50 at lr=1e-3 reaches 100% window and run accuracy without SMOTE; SMOTE has little effect on speed for Pipeline A.

#### Pipeline D — SES 4-Channel (SMOTE has no effect on speed)

| Model | Backbone | LR | Window Acc | Run Acc |
|-------|----------|----|-----------|---------|
| `ses4ch_speed_rn18_lr1e3` | ResNet-18 | 1e-3 | 94.7% | 93.3% |
| `ses4ch_speed_rn18_lr1e4` | ResNet-18 | 1e-4 | 92.7% | **100.0%** |
| `ses4ch_speed_rn50_lr1e3` | ResNet-50 | 1e-3 | **98.0%** | **100.0%** |
| `ses4ch_speed_rn50_lr1e4` | ResNet-50 | 1e-4 | 93.3% | **100.0%** |
| `ses4ch_speed_enb0_lr1e3` | EfficientNet-B0 | 1e-3 | 92.7% | 93.3% |
| `ses4ch_speed_enb0_lr1e4` | EfficientNet-B0 | 1e-4 | 77.3% | 80.0% |
| `ses4ch_speed_cnxt_lr1e3` | ConvNeXt-Tiny | 1e-3 | 50.7% | 53.3% |
| `ses4ch_speed_cnxt_lr1e4` | ConvNeXt-Tiny | 1e-4 | **97.3%** | **100.0%** |

SMOTE produces identical results to no-SMOTE for all 8 backbone/LR combinations (see `ses4ch_smote_speed_*`). ConvNeXt-Tiny collapses again at lr=1e-3; at lr=1e-4 it reaches 97.3% window / 100% run.

---

### Depth of Cut (3-class: 0.015 / 0.030 / 0.060 mm, 12 test runs)

#### Pipeline A — Standard RGB CWT (±SMOTE)

| Backbone | LR | No-SMOTE Win | No-SMOTE Run | SMOTE Win | SMOTE Run |
|----------|----|-------------|-------------|-----------|-----------|
| ResNet-18 | 1e-3 | 77.5% | 75.0% | 90.0% | 91.7% |
| ResNet-18 | 1e-4 | 84.2% | 91.7% | 85.8% | 91.7% |
| ResNet-50 | 1e-3 | 89.2% | 91.7% | 82.5% | 83.3% |
| ResNet-50 | 1e-4 | 90.0% | 91.7% | 85.8% | 91.7% |
| EfficientNet-B0 | 1e-3 | 93.3% | 91.7% | **94.2%** | **100.0%** |
| EfficientNet-B0 | 1e-4 | **95.0%** | **100.0%** | **95.0%** | **100.0%** |
| ConvNeXt-Tiny | 1e-3 | 33.3% | 33.3% | 33.3% | 33.3% |
| ConvNeXt-Tiny | 1e-4 | 88.3% | 91.7% | 83.3% | 91.7% |

EfficientNet-B0 at lr=1e-4 reaches 100% run accuracy with and without SMOTE. SMOTE notably improves ResNet-18 at lr=1e-3 (75% -> 91.7% run) but has little effect on other backbones.

#### Pipeline D — SES 4-Channel (SMOTE has no effect on DOC)

| Model | Backbone | LR | Window Acc | Run Acc |
|-------|----------|----|-----------|---------|
| `ses4ch_doc_rn18_lr1e3` | ResNet-18 | 1e-3 | 83.3% | 83.3% |
| `ses4ch_doc_rn18_lr1e4` | ResNet-18 | 1e-4 | 87.5% | 91.7% |
| `ses4ch_doc_rn50_lr1e3` | ResNet-50 | 1e-3 | **92.5%** | **100.0%** |
| `ses4ch_doc_rn50_lr1e4` | ResNet-50 | 1e-4 | 82.5% | 83.3% |
| `ses4ch_doc_enb0_lr1e3` | EfficientNet-B0 | 1e-3 | **90.0%** | **100.0%** |
| `ses4ch_doc_enb0_lr1e4` | EfficientNet-B0 | 1e-4 | 83.3% | 91.7% |
| `ses4ch_doc_cnxt_lr1e3` | ConvNeXt-Tiny | 1e-3 | 60.0% | 58.3% |
| `ses4ch_doc_cnxt_lr1e4` | ConvNeXt-Tiny | 1e-4 | 80.0% | 83.3% |

SMOTE produces identical results to no-SMOTE for all DOC models (see `ses4ch_smote_doc_*`). ResNet-50 and EfficientNet-B0 at lr=1e-3 both reach 100% run accuracy.

---

### Feed Rate Coarse (3-class: Low / Med / High, 12 test runs)

#### Pipeline A — Standard RGB CWT (±SMOTE)

| Backbone | LR | No-SMOTE Win | No-SMOTE Run | SMOTE Win | SMOTE Run |
|----------|----|-------------|-------------|-----------|-----------|
| ResNet-18 | 1e-3 | 75.0% | 75.0% | 65.8% | 66.7% |
| ResNet-18 | 1e-4 | 75.0% | 75.0% | 71.7% | 75.0% |
| ResNet-50 | 1e-3 | 77.5% | **83.3%** | 72.5% | 75.0% |
| ResNet-50 | 1e-4 | 70.8% | 75.0% | 65.8% | 66.7% |
| EfficientNet-B0 | 1e-3 | 74.2% | 75.0% | 64.2% | 66.7% |
| EfficientNet-B0 | 1e-4 | 75.0% | 75.0% | **75.0%** | 75.0% |
| ConvNeXt-Tiny | 1e-3 | **75.8%** | 75.0% | 33.3% | 33.3% |
| ConvNeXt-Tiny | 1e-4 | **81.7%** | **83.3%** | 71.7% | 75.0% |

SMOTE hurts feed coarse in Pipeline A across the board: no-SMOTE beats or ties SMOTE for every backbone/LR combination. ConvNeXt-Tiny at lr=1e-4 reaches the best no-SMOTE result (81.7% window / 83.3% run); SMOTE collapses it at lr=1e-3.

#### Pipeline D — SES 4-Channel (SMOTE effect varies)

| Model | Backbone | LR | No-SMOTE Win | No-SMOTE Run | SMOTE Win | SMOTE Run |
|-------|----------|----|-------------|-------------|-----------|-----------|
| `ses4ch_feed_coarse_rn18_lr1e3` | ResNet-18 | 1e-3 | 66.7% | 66.7% | 61.7% | 58.3% |
| `ses4ch_feed_coarse_rn18_lr1e4` | ResNet-18 | 1e-4 | 62.5% | 75.0% | 60.8% | 58.3% |
| `ses4ch_feed_coarse_rn50_lr1e3` | ResNet-50 | 1e-3 | **70.0%** | **75.0%** | **70.0%** | **75.0%** |
| `ses4ch_feed_coarse_rn50_lr1e4` | ResNet-50 | 1e-4 | 66.7% | 75.0% | 58.3% | 58.3% |
| `ses4ch_feed_coarse_enb0_lr1e3` | EfficientNet-B0 | 1e-3 | 62.5% | 58.3% | 60.8% | 66.7% |
| `ses4ch_feed_coarse_enb0_lr1e4` | EfficientNet-B0 | 1e-4 | **70.8%** | **75.0%** | 65.0% | 75.0% |
| `ses4ch_feed_coarse_cnxt_lr1e3` | ConvNeXt-Tiny | 1e-3 | 33.3% | 33.3% | 62.5% | 66.7% |
| `ses4ch_feed_coarse_cnxt_lr1e4` | ConvNeXt-Tiny | 1e-4 | 60.0% | 66.7% | 60.0% | 66.7% |

Unlike speed and DOC, SMOTE has mixed effects: it harms ResNet-18 and ResNet-50 at lr=1e-4 but rescues ConvNeXt-Tiny at lr=1e-3 from a degenerate solution (33.3% -> 62.5%). Best run accuracy is 75% (multiple models).

---

### Surface Roughness Ra (3-class: Smooth / Medium / Rough, 12 test runs)

#### Pipeline A — Standard RGB CWT (±SMOTE)

| Backbone | LR | No-SMOTE Win | No-SMOTE Run | SMOTE Win | SMOTE Run |
|----------|----|-------------|-------------|-----------|-----------|
| ResNet-18 | 1e-3 | **91.7%** | **91.7%** | 62.5% | 66.7% |
| ResNet-18 | 1e-4 | 87.5% | 83.3% | 68.3% | 66.7% |
| ResNet-50 | 1e-3 | 83.3% | 83.3% | 69.2% | 66.7% |
| ResNet-50 | 1e-4 | 86.7% | **91.7%** | 67.5% | **75.0%** |
| EfficientNet-B0 | 1e-3 | **91.7%** | **91.7%** | 71.7% | 66.7% |
| EfficientNet-B0 | 1e-4 | 88.3% | **91.7%** | **73.3%** | **75.0%** |
| ConvNeXt-Tiny | 1e-3 | 33.3% | 33.3% | 33.3% | 33.3% |
| ConvNeXt-Tiny | 1e-4 | 88.3% | **91.7%** | 72.5% | **75.0%** |

SMOTE dramatically harms roughness classification in Pipeline A — no-SMOTE models achieve 83-91% run accuracy vs 66-75% with SMOTE. ResNet-18 and EfficientNet-B0 at lr=1e-3 reach 91.7% without SMOTE. ConvNeXt-Tiny collapses at lr=1e-3 in both cases.

#### Pipeline D — SES 4-Channel (SMOTE has mixed effects)

| Model | Backbone | LR | No-SMOTE Win | No-SMOTE Run | SMOTE Win | SMOTE Run |
|-------|----------|----|-------------|-------------|-----------|-----------|
| `ses4ch_roughness_rn18_lr1e3` | ResNet-18 | 1e-3 | **75.0%** | **75.0%** | 73.3% | **75.0%** |
| `ses4ch_roughness_rn18_lr1e4` | ResNet-18 | 1e-4 | 68.3% | 66.7% | 69.2% | 66.7% |
| `ses4ch_roughness_rn50_lr1e3` | ResNet-50 | 1e-3 | 69.2% | 66.7% | 66.7% | 66.7% |
| `ses4ch_roughness_rn50_lr1e4` | ResNet-50 | 1e-4 | **75.0%** | **75.0%** | **75.0%** | **75.0%** |
| `ses4ch_roughness_enb0_lr1e3` | EfficientNet-B0 | 1e-3 | 72.5% | **75.0%** | 69.2% | 66.7% |
| `ses4ch_roughness_enb0_lr1e4` | EfficientNet-B0 | 1e-4 | 65.0% | **75.0%** | 65.8% | 66.7% |
| `ses4ch_roughness_cnxt_lr1e3` | ConvNeXt-Tiny | 1e-3 | 33.3% | 33.3% | 52.5% | 41.7% |
| `ses4ch_roughness_cnxt_lr1e4` | ConvNeXt-Tiny | 1e-4 | 65.8% | 66.7% | 68.3% | 66.7% |

Maximum run accuracy in Pipeline D matches Pipeline A at 75%. SMOTE is neutral-to-harmful for most models; ResNet-50 at lr=1e-4 is SMOTE-invariant. ConvNeXt-Tiny at lr=1e-3 partially recovers with SMOTE (33.3% -> 52.5% window) but doesn't reach useful accuracy.

---

## Pipeline

### 1. Generate scalograms — `cnn_model/scalogram.py`

Converts each CSV into a 224×224 RGB scalogram PNG using an analytic Morlet CWT.

```bash
# 1 window per run (for speed, doc, feed_coarse)
python cnn_model/scalogram.py --input_dir data --output_dir scalograms_ai4_ai6

# 4 windows per run (for feed fine-grained — more training data per run)
python cnn_model/scalogram.py --input_dir data --output_dir scalograms_ai4_ai6_4w --n_windows 4
```

### 2. Train — `cnn_model/cnn_train.py`

Fine-tunes a pretrained ResNet18. Test runs are held out before training and never used to update weights:

- **Speed test runs:** run24, run27, run30, run33, run36
- **Feed test runs:** run25, run13, run31, run17, run5, run36
- **DOC test runs:** run1, run5, run43, run7, run14, run19, run22, run29, run36

```bash
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6 --target speed --save model_speed.pt
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6 --target doc --save model_doc.pt
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6 --target feed_coarse --save model_feed_coarse.pt
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6_4w --target feed --epochs 40 --save model_feed.pt
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6 --target roughness --epochs 30 --augment light --save model_roughness.pt
```

## Project Structure

```
data/                     Raw CSV signal files (run1.csv – run45.csv)
cnn_model/                CNN + scalogram pipeline
  scalogram.py            Generates scalogram PNGs from CSVs
  cnn_train.py            Trains ResNet18 classifier
  cnn_svm.py              Alternative: SVM on CNN features
fft_model/                FFT-based frequency classifier
scalograms_ai4_ai6/       1-window scalograms (45 images)
scalograms_ai4_ai6_4w/    4-window scalograms (180 images)
model_speed.pt            Best speed model (100%)
model_doc.pt              Best DOC model (100%)
model_feed_coarse.pt      Best coarse feed model (66.7%)
model_feed.pt             Best fine-grained feed model (50%)
model_roughness.pt        Best surface roughness model (83.3%)
```

See `cnn_model/README.md` for full detail on training options, per-class results, and why feed rate is harder to classify than speed or DOC.

---

## Precomputed-Feature Scalogram Pipeline (32×3 / 32×12)

A second pipeline built from the **precomputed per-run feature spreadsheets**
(`data/STLMILAE_DOC{015,03,06}.xlsx`) rather than raw waveforms. Features:
32 FFT bins, 64 Mexican-hat CWT scales, 64 Coiflet CWT scales, DWT statistics.

### Image layouts

| Dir suffix | Description |
|---|---|
| `scalograms_32x3` | 32×3: FFT col + 2 CWT cols, scales selected by roughness correlation |
| `scalograms_32x3_feedopt` | Same, scales selected by feed rate correlation |
| `scalograms_32x3_speedopt` | Same, scales selected by speed correlation |
| `scalograms_32x3_docopt` | Same, scales selected by DOC correlation |
| `scalograms_32x12` | 32×12: all 12 feature columns |
| `*_9win` | Row-split into 9 pseudo-windows instead of 3 |
| `*_residual*` | Residual-corrected (group-mean subtracted per speed/DOC combination) |

Builders: `build_32x3_features.py`, `build_32x12_features.py`, `build_residual_scalograms.py`.

### Training

```powershell
# Plain
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet18 --lr 1e-3

# Cascade (conditioned on predicted feed rate)
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-3 --conditioned
python predict_conditioning_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-3 --cascade_predicted

# K-fold CV
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet50 --kfold 5

# Full sweeps
powershell -File run_everything_detailed.ps1        # 552 commands
powershell -File run_sweep_32xN_detailed.ps1        # 256 plain runs
powershell -File run_sweep_cascade_detailed.ps1     # 272 cascade runs
powershell -File run_sweep_residual_detailed.ps1    # 192 residual runs
powershell -File run_sweep_speedopt_docopt.ps1      # 128 speedopt/docopt runs
```

### Best results — single train/test split (70/30 by run)

| Target | Approach | Run acc | Win acc | Model |
|---|---|---|---|---|
| Speed | Feedopt cascade layout | **86.7%** | 64.4% | convnext_tiny / scalograms_32x12_feedopt / LR=1e-4 |
| DOC | Docopt scale selection | **83.3%** | 80.6% | resnet18 / scalograms_32x3_docopt / LR=1e-3 |
| Feed coarse | Residual + cascade | **83.3%** | 69.4% | resnet50 / scalograms_32x3_feedopt_9win_residual / conditioned |
| Roughness | Residual correction | **83.3%** | 83.3% | convnext_tiny / scalograms_32x3 / conditioned |

### K-fold CV results (5-fold stratified) — honest generalisation estimate

| Target | Model | Run majority-vote | Run soft-vote | Window acc |
|---|---|---|---|---|
| Speed | resnet18 / scalograms_32x12_feedopt | 0.700 ± 0.089 | **0.740 ± 0.080** | 0.640 ± 0.077 |
| DOC | resnet18 / scalograms_32x3_docopt | 0.756 ± 0.163 | 0.756 ± 0.163 | 0.719 ± 0.136 |
| Feed coarse | resnet50 / scalograms_32x3_feedopt_9win_residual | 0.618 ± 0.118 | 0.591 ± 0.175 | 0.542 ± 0.066 |
| Roughness | resnet50 / scalograms_32x12_residual_roughness | **0.719 ± 0.087** | 0.719 ± 0.087 | 0.698 ± 0.054 |

K-fold JSON files: `cnn_model/models_<target>_<dir>/<arch>_lr<lr>_kfold5_results.json`

### Why results are lower than the raw time series pipeline

- **No genuine windowing:** the 3 or 9 windows per run are row-splits of a single
  pre-computed feature matrix, not independent time segments. Effective sample size
  is 45 runs regardless of window count.
- **Pre-summarised features:** FFT and CWT values were computed over the full run
  before being stored in Excel — the time axis is already gone.
- **Scale selection mismatch:** CWT scales were historically selected by roughness/feed
  correlation; speedopt/docopt variants were added but the improvement was marginal.
- **Path forward:** locate the raw `stlml_1`–`stlml_45` signal files (recorded at
  16,393 Hz, ~65,000 samples/run) and rebuild scalograms with genuine temporal
  windowing to recover 90%+ speed accuracy.
