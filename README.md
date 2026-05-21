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

Systematic search over backbone architectures and data strategies using 10-window scalograms (`scalograms_10w`) with signal-space SMOTE augmentation. Models saved in `exp_models/` (speed models saved to project root). All accuracy figures are holdout test-only — test runs were never used to update weights. See `RESULTS.md` for confusion matrices and window-level breakdowns.

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

### Feed Rate Fine-Grained (6-class, 39 train / 6 test runs)

| Model file | Backbone | Window Acc | Run Majority-Vote |
|------------|----------|-----------|-------------------|
| `exp_models/feed_rn18_10w_adamw.pt` | ResNet18 | **48.3%** | 50.0% |
| `exp_models/feed_effb0_10w_adamw.pt` | EfficientNet-B0 | 38.3% | 50.0% |

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

**Window majority-vote** — `feed_rn18_10w_adamw.pt` (ResNet18, best):

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

Both models correctly classify run25, run31, and run36. Both fail on run13, run17, and run5 under both methods — the wrong predictions are highly confident (e.g., run13: ResNet p=1.000 for 6 mm/rev). Probability averaging does not recover any additional runs compared to majority voting.

---

### Feed Rate Coarse (3-class: low/med/high, 39 train / 6 test runs)

| Model file | Backbone | Window Acc | Run Majority-Vote |
|------------|----------|-----------|-------------------|
| `exp_models/feed_coarse_rn18_10w_adamw.pt` | ResNet18 | **66.7%** | **66.7%** |
| `exp_models/feed_coarse_effb0_10w_adamw.pt` | EfficientNet-B0 | **66.7%** | **66.7%** |

**SMOTE augmentation** (`smote_feed_coarse_labels.csv`) — 18 synthetic runs added:

| Class | Real runs | Synthetic added | Total runs | Total images |
|-------|-----------|----------------|------------|--------------|
| low (3-4 mm/rev)    | 13 | 6  | 19 | 190 |
| medium (5-6 mm/rev) | 19 | 0  | 19 | 190 |
| high (7-8 mm/rev)   | 7  | 12 | 19 | 190 |
| **Total** | **39** | **18** | **57** | **570** |

Pre-SMOTE the high class had only 7 training runs vs 19 for medium. SMOTE added 12 synthetic runs to high and 6 to low, bringing all three classes to exactly 19 runs / 190 images.

**Window majority-vote** and **whole-run probability averaging** — both architectures produce identical run-level predictions under both methods:

| Run | True | Predicted | Result | ResNet votes / prob | EfficientNet votes / prob |
|-----|------|-----------|--------|---------------------|--------------------------|
| run25 | low (3-4)    | low    | **OK**    | low×10 / low=0.898 | low×10 / low=0.960 |
| run13 | low (3-4)    | medium | **WRONG** | med×10 / med=0.989 | med×10 / med=1.000 |
| run31 | medium (5-6) | medium | **OK**    | med×10 / med=0.999 | med×10 / med=0.935 |
| run17 | medium (5-6) | medium | **OK**    | med×10 / med=0.974 | med×10 / med=0.978 |
| run36 | high (7-8)   | high   | **OK**    | high×10 / high=0.990 | high×10 / high=0.989 |
| run5  | high (7-8)   | medium | **WRONG** | med×10 / med=0.923 | med×10 / med=1.000 |

run13 (4 mm/rev, boundary of low) and run5 (7 mm/rev, boundary of high) fail under both methods in both architectures — the same two runs that fail in fine-grained classification.

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
