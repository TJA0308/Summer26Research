# Holdout Test Evaluation Results

**Date:** 2026-05-20  
**Evaluation:** Test-only, zero data leakage — all test runs were held out before training and never used to update model weights.  
**Data:** 45 milling runs, 10 scalogram windows per run (`scalograms_10w`, 224×224 CWT images), SMOTE synthetics excluded from test evaluation.

---

## Methodology

Each test run was selected before training to represent held-out conditions across the DOC/speed/feed parameter space. The evaluation here uses **only those held-out runs** — these images were never seen by any model during training or validation. Two accuracy metrics are reported:

- **Window accuracy** — correct predictions out of all individual scalogram windows (10 per run)
- **Run majority-vote accuracy** — a run is classified by the most-voted class across its 10 windows; this is the operationally relevant metric (one run = one machining pass)

---

## 1. Spindle Speed (5-class: 1500 / 2000 / 3000 / 4000 / 5000 rpm)

**Test runs (10 total, 2 per class):**

| Run | True Speed | DOC |
|-----|-----------|-----|
| run9  | 1500 rpm | 0.030 mm |
| run22 | 1500 rpm | 0.060 mm |
| run12 | 2000 rpm | 0.030 mm |
| run27 | 2000 rpm | 0.060 mm |
| run15 | 3000 rpm | 0.030 mm |
| run28 | 3000 rpm | 0.060 mm |
| run2  | 4000 rpm | 0.015 mm |
| run16 | 4000 rpm | 0.030 mm |
| run5  | 5000 rpm | 0.015 mm |
| run36 | 5000 rpm | 0.060 mm |

### Model A: `speed_cnxt_10w.pt` (ConvNeXt-Tiny, AdamW, 20 epochs)

| Metric | Value |
|--------|-------|
| Window accuracy | **96.0%** (96/100) |
| Run majority-vote | **100.0%** (10/10) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| 1500 rpm | 20/20 | - |
| 2000 rpm | 20/20 | - |
| 3000 rpm | 20/20 | - |
| 4000 rpm | 16/20 | 2000 rpm x4 |
| 5000 rpm | 20/20 | - |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run9  | 1500 rpm | 1500 rpm | OK | 1500x10 |
| run22 | 1500 rpm | 1500 rpm | OK | 1500x10 |
| run12 | 2000 rpm | 2000 rpm | OK | 2000x10 |
| run27 | 2000 rpm | 2000 rpm | OK | 2000x10 |
| run15 | 3000 rpm | 3000 rpm | OK | 3000x10 |
| run28 | 3000 rpm | 3000 rpm | OK | 3000x10 |
| run2  | 4000 rpm | 4000 rpm | OK | 4000x10 |
| run16 | 4000 rpm | 4000 rpm | OK | 4000x6, 2000x4 |
| run5  | 5000 rpm | 5000 rpm | OK | 5000x10 |
| run36 | 5000 rpm | 5000 rpm | OK | 5000x10 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | 1500 | 2000 | 3000 | 4000 | 5000 |
|--|------|------|------|------|------|
| 1500 rpm | **20** | 0 | 0 | 0 | 0 |
| 2000 rpm | 0 | **20** | 0 | 0 | 0 |
| 3000 rpm | 0 | 0 | **20** | 0 | 0 |
| 4000 rpm | 0 | 4 | 0 | **16** | 0 |
| 5000 rpm | 0 | 0 | 0 | 0 | **20** |

4 windows from run16 (4000 rpm, DOC=0.030) were misclassified as 2000 rpm. Majority vote corrects the run-level prediction. All 10 test runs correctly identified at run level.

---

### Model B: `speed_resnet_10w.pt` (ResNet18, AdamW, 20 epochs)

| Metric | Value |
|--------|-------|
| Window accuracy | **90.0%** (90/100) |
| Run majority-vote | **100.0%** (10/10) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| 1500 rpm | 16/20 | 3000 rpm x4 |
| 2000 rpm | 19/20 | 1500 rpm x1 |
| 3000 rpm | 16/20 | 1500 rpm x4 |
| 4000 rpm | 19/20 | 2000 rpm x1 |
| 5000 rpm | 20/20 | - |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run9  | 1500 rpm | 1500 rpm | OK | 1500x10 |
| run22 | 1500 rpm | 1500 rpm | OK | 1500x6, 3000x4 |
| run12 | 2000 rpm | 2000 rpm | OK | 2000x10 |
| run27 | 2000 rpm | 2000 rpm | OK | 2000x9, 1500x1 |
| run15 | 3000 rpm | 3000 rpm | OK | 3000x10 |
| run28 | 3000 rpm | 3000 rpm | OK | 3000x6, 1500x4 |
| run2  | 4000 rpm | 4000 rpm | OK | 4000x10 |
| run16 | 4000 rpm | 4000 rpm | OK | 4000x9, 2000x1 |
| run5  | 5000 rpm | 5000 rpm | OK | 5000x10 |
| run36 | 5000 rpm | 5000 rpm | OK | 5000x10 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | 1500 | 2000 | 3000 | 4000 | 5000 |
|--|------|------|------|------|------|
| 1500 rpm | **16** | 0 | 4 | 0 | 0 |
| 2000 rpm | 1 | **19** | 0 | 0 | 0 |
| 3000 rpm | 4 | 0 | **16** | 0 | 0 |
| 4000 rpm | 0 | 1 | 0 | **19** | 0 |
| 5000 rpm | 0 | 0 | 0 | 0 | **20** |

ResNet18 has more window-level confusion between adjacent RPM classes (1500 rpm <-> 3000 rpm) but still achieves 100% run-level accuracy via majority vote.

---

### Speed Model Comparison

| Model | Backbone | Window Acc | Run MV Acc |
|-------|----------|-----------|-----------|
| `speed_cnxt_10w.pt` | ConvNeXt-Tiny | **96.0%** | **100.0%** |
| `speed_resnet_10w.pt` | ResNet18 | 90.0% | **100.0%** |

Both models achieve perfect run-level accuracy on completely unseen data. ConvNeXt-Tiny is more confident at the window level, which matters if per-window confidence scores are used downstream.

---

## 2. Feed Rate Fine-Grained (6-class: 3 / 4 / 5 / 6 / 7 / 8 mm/rev)

**Test runs (6 total, 1 per class):**

| Run | True Feed | Speed | DOC |
|-----|----------|-------|-----|
| run25 | 3 mm/rev | 2000 rpm | 0.060 mm |
| run13 | 4 mm/rev | 3000 rpm | 0.030 mm |
| run31 | 5 mm/rev | 4000 rpm | 0.060 mm |
| run17 | 6 mm/rev | 4000 rpm | 0.030 mm |
| run5  | 7 mm/rev | 5000 rpm | 0.015 mm |
| run36 | 8 mm/rev | 5000 rpm | 0.060 mm |

### Model A: `feed_rn18_10w_adamw.pt` (ResNet18) — Best Feed

| Metric | Value |
|--------|-------|
| Window accuracy | **48.3%** (29/60) |
| Run majority-vote | **50.0%** (3/6 runs) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| 3 mm/rev | 10/10 | - |
| 4 mm/rev | 0/10 | 6 mm/rev x10 |
| 5 mm/rev | 9/10 | 6 mm/rev x1 |
| 6 mm/rev | 0/10 | 5 mm/rev x10 |
| 7 mm/rev | 0/10 | 6 mm/rev x10 |
| 8 mm/rev | 10/10 | - |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run25 | 3 mm/rev | 3 mm/rev | OK | 3x10 |
| run13 | 4 mm/rev | 6 mm/rev | WRONG | 6x10 |
| run31 | 5 mm/rev | 5 mm/rev | OK | 5x9, 6x1 |
| run17 | 6 mm/rev | 5 mm/rev | WRONG | 5x10 |
| run5  | 7 mm/rev | 6 mm/rev | WRONG | 6x10 |
| run36 | 8 mm/rev | 8 mm/rev | OK | 8x10 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | 3 | 4 | 5 | 6 | 7 | 8 |
|--|---|---|---|---|---|---|
| 3 mm/rev | **10** | 0 | 0 | 0 | 0 | 0 |
| 4 mm/rev | 0 | **0** | 0 | 10 | 0 | 0 |
| 5 mm/rev | 0 | 0 | **9** | 1 | 0 | 0 |
| 6 mm/rev | 0 | 0 | 10 | **0** | 0 | 0 |
| 7 mm/rev | 0 | 0 | 0 | 10 | **0** | 0 |
| 8 mm/rev | 0 | 0 | 0 | 0 | 0 | **10** |

---

### Model B: `feed_effb0_10w_adamw.pt` (EfficientNet-B0)

| Metric | Value |
|--------|-------|
| Window accuracy | **38.3%** (23/60) |
| Run majority-vote | **50.0%** (3/6 runs) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| 3 mm/rev | 8/10 | 5 mm/rev x2 |
| 4 mm/rev | 0/10 | 6 mm/rev x6, 5 mm/rev x4 |
| 5 mm/rev | 6/10 | 6 mm/rev x4 |
| 6 mm/rev | 0/10 | 5 mm/rev x10 |
| 7 mm/rev | 0/10 | 6 mm/rev x10 |
| 8 mm/rev | 9/10 | 7 mm/rev x1 |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run25 | 3 mm/rev | 3 mm/rev | OK | 3x8, 5x2 |
| run13 | 4 mm/rev | 6 mm/rev | WRONG | 6x6, 5x4 |
| run31 | 5 mm/rev | 5 mm/rev | OK | 5x6, 6x4 |
| run17 | 6 mm/rev | 5 mm/rev | WRONG | 5x10 |
| run5  | 7 mm/rev | 6 mm/rev | WRONG | 6x10 |
| run36 | 8 mm/rev | 8 mm/rev | OK | 8x9, 7x1 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | 3 | 4 | 5 | 6 | 7 | 8 |
|--|---|---|---|---|---|---|
| 3 mm/rev | **8** | 0 | 2 | 0 | 0 | 0 |
| 4 mm/rev | 0 | **0** | 4 | 6 | 0 | 0 |
| 5 mm/rev | 0 | 0 | **6** | 4 | 0 | 0 |
| 6 mm/rev | 0 | 0 | 10 | **0** | 0 | 0 |
| 7 mm/rev | 0 | 0 | 0 | 10 | **0** | 0 |
| 8 mm/rev | 0 | 0 | 0 | 0 | 1 | **9** |

---

### Feed Fine-Grained Summary

| Model | Backbone | Window Acc | Run MV Acc |
|-------|----------|-----------|-----------|
| `feed_rn18_10w_adamw.pt` | ResNet18 | **48.3%** | **50.0%** |
| `feed_effb0_10w_adamw.pt` | EfficientNet-B0 | 38.3% | 50.0% |

Feed rate 4, 6, and 7 mm/rev collapse to adjacent class predictions across both architectures with zero correct predictions. The extreme classes (3 and 8 mm/rev) are reliably identified. The middle feed rates produce CWT signatures dominated by RPM harmonics rather than feed-rate-specific chip-load modulation — this is a signal-level problem that persists across architectures.

---

## 3. Surface Roughness Ra (3-class: Smooth / Medium / Rough)

**Test runs (6 total, 2 per class):**

| Run | True Class | Ra (um) | Speed | DOC |
|-----|-----------|---------|-------|-----|
| run5  | Smooth (Ra<0.7)  | 0.424 | 5000 rpm | 0.015 mm |
| run43 | Smooth (Ra<0.7)  | 0.364 | 3000 rpm | 0.015 mm |
| run7  | Medium (0.7-1.0) | 0.930 | 1500 rpm | 0.030 mm |
| run27 | Medium (0.7-1.0) | 0.868 | 2000 rpm | 0.060 mm |
| run22 | Rough (Ra>1.0)   | 1.186 | 1500 rpm | 0.060 mm |
| run34 | Rough (Ra>1.0)   | 2.084 | 5000 rpm | 0.060 mm |

### Model: `roughness_rn18_10w_adamw.pt` (ResNet18, AdamW, 20 epochs) — Best Roughness

| Metric | Value |
|--------|-------|
| Window accuracy | **93.3%** (56/60) |
| Run majority-vote | **100.0%** (6/6 runs) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| Smooth (Ra<0.7)  | 20/20 | - |
| Medium (0.7-1.0) | 17/20 | Rough x3 |
| Rough (Ra>1.0)   | 19/20 | Medium x1 |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run5  | Smooth | Smooth | OK | Smooth x10 |
| run43 | Smooth | Smooth | OK | Smooth x10 |
| run7  | Medium | Medium | OK | Medium x10 |
| run27 | Medium | Medium | OK | Medium x7, Rough x3 |
| run22 | Rough  | Rough  | OK | Rough x10 |
| run34 | Rough  | Rough  | OK | Rough x9, Medium x1 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | Smooth | Medium | Rough |
|--|--------|--------|-------|
| Smooth | **20** | 0 | 0 |
| Medium | 0 | **17** | 3 |
| Rough  | 0 | 1 | **19** |

All 6 test runs correctly classified by majority vote. The 4 window-level misclassifications are at class boundaries: run27 (Medium, Ra=0.868 um) is near the 1.0 threshold; run34 (Rough, Ra=2.084 um) has one window classified as Medium. Smooth is perfectly separated — DOC=0.015 mm produces a distinctly lower-energy CWT signature.

---

## 4. Feed Rate Coarse (3-class: low 3-4 / medium 5-6 / high 7-8 mm/rev)

**Test runs (6 total, same as fine-grained feed):**

| Run | True Class | Actual Feed |
|-----|-----------|-------------|
| run25 | low (3-4)    | 3 mm/rev |
| run13 | low (3-4)    | 4 mm/rev |
| run31 | medium (5-6) | 5 mm/rev |
| run17 | medium (5-6) | 6 mm/rev |
| run36 | high (7-8)   | 8 mm/rev |
| run5  | high (7-8)   | 7 mm/rev |

### Model A: `feed_coarse_rn18_10w_adamw.pt` (ResNet18, AdamW, 20 epochs)

| Metric | Value |
|--------|-------|
| Window accuracy | **66.7%** (40/60) |
| Run majority-vote | **66.7%** (4/6 runs) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| low (3-4 mm/rev)    | 10/20 | medium x10 |
| medium (5-6 mm/rev) | 20/20 | - |
| high (7-8 mm/rev)   | 10/20 | medium x10 |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run25 | low    | low    | OK    | low x10 |
| run13 | low    | medium | WRONG | medium x10 |
| run31 | medium | medium | OK    | medium x10 |
| run17 | medium | medium | OK    | medium x10 |
| run36 | high   | high   | OK    | high x10 |
| run5  | high   | medium | WRONG | medium x10 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | low | medium | high |
|--|-----|--------|------|
| low    | **10** | 10 | 0 |
| medium | 0 | **20** | 0 |
| high   | 0 | 10 | **10** |

---

### Model B: `feed_coarse_effb0_10w_adamw.pt` (EfficientNet-B0, AdamW, 20 epochs)

| Metric | Value |
|--------|-------|
| Window accuracy | **66.7%** (40/60) |
| Run majority-vote | **66.7%** (4/6 runs) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| low (3-4 mm/rev)    | 10/20 | medium x10 |
| medium (5-6 mm/rev) | 20/20 | - |
| high (7-8 mm/rev)   | 10/20 | medium x10 |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run25 | low    | low    | OK    | low x10 |
| run13 | low    | medium | WRONG | medium x10 |
| run31 | medium | medium | OK    | medium x10 |
| run17 | medium | medium | OK    | medium x10 |
| run36 | high   | high   | OK    | high x10 |
| run5  | high   | medium | WRONG | medium x10 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | low | medium | high |
|--|-----|--------|------|
| low    | **10** | 10 | 0 |
| medium | 0 | **20** | 0 |
| high   | 0 | 10 | **10** |

---

### Feed Coarse Summary

| Model | Backbone | Window Acc | Run MV Acc |
|-------|----------|-----------|-----------|
| `feed_coarse_rn18_10w_adamw.pt` | ResNet18 | **66.7%** | **66.7%** |
| `feed_coarse_effb0_10w_adamw.pt` | EfficientNet-B0 | **66.7%** | **66.7%** |

Both architectures produce identical predictions. The failures are run13 (4 mm/rev labeled low, but near the low/medium boundary) and run5 (7 mm/rev labeled high, but near the high/medium boundary). Coarsening the label space improves overall accuracy from 48% to 67% but does not resolve the boundary-case problem.

---

## Overall Summary

| Model File | Target | Backbone | Windows | Window Acc | Run MV Acc |
|-----------|--------|----------|---------|-----------|-----------|
| `speed_cnxt_10w.pt` | Speed (5-class) | ConvNeXt-Tiny | 100 | **96.0%** | **100.0%** |
| `speed_resnet_10w.pt` | Speed (5-class) | ResNet18 | 100 | 90.0% | **100.0%** |
| `exp_models/feed_rn18_10w_adamw.pt` | Feed (6-class) | ResNet18 | 60 | **48.3%** | 50.0% |
| `exp_models/feed_effb0_10w_adamw.pt` | Feed (6-class) | EfficientNet-B0 | 60 | 38.3% | 50.0% |
| `exp_models/roughness_rn18_10w_adamw.pt` | Roughness (3-class) | ResNet18 | 60 | **93.3%** | **100.0%** |
| `exp_models/feed_coarse_rn18_10w_adamw.pt` | Feed Coarse (3-class) | ResNet18 | 60 | **66.7%** | **66.7%** |
| `exp_models/feed_coarse_effb0_10w_adamw.pt` | Feed Coarse (3-class) | EfficientNet-B0 | 60 | **66.7%** | **66.7%** |

---

## Key Findings

**Speed is solved.** Both speed models achieve 100% run-level accuracy on completely unseen holdout data. RPM places spindle harmonics at fixed frequency positions that survive any normalization or DOC/feed variation. ConvNeXt-Tiny shows higher per-window confidence (96% vs 90%), which matters if window-level scores are used as uncertainty estimates.

**Roughness generalizes well.** The ResNet18 roughness model achieves 93.3% window accuracy and 100% run-level accuracy on 6 unseen runs spanning all three roughness classes and all three DOC levels. The rare window-level errors occur at class boundaries (run27 Medium Ra=0.868 um is near the 1.0 threshold). SMOTE-balanced training on 10-window scalograms captures the DOC-driven surface energy pattern reliably.

**Feed rate is the hard problem.** The 6-class fine-grained model tops out at 48.3% window / 50% run accuracy. The 3-class coarse version reaches 66.7%, an improvement, but both share the same root failure: the middle-range feed rates (4, 6, 7 mm/rev) produce CWT signatures dominated by RPM harmonics rather than feed-specific modulation. Classes 4, 6, and 7 mm/rev achieve 0 correct predictions across all architectures. The extreme classes (3 and 8 mm/rev) are reliably identified because they represent the strongest departure from the median spectral pattern.

**Architecture matters less than signal quality.** For speed and roughness, ResNet18 and ConvNeXt-Tiny converge to the same run-level accuracy — the signal is strong enough that the model cannot fail. For feed rate, no architecture tested (ResNet18, EfficientNet-B0, ConvNeXt-Tiny) escaped the 50% ceiling on holdout data.

**Majority voting is robust.** Even when individual windows misclassify (e.g., 4 of 10 windows in run16 and run22 for speed), majority vote corrects the run-level prediction for speed and roughness. For feed rate, majority vote does not help because the misclassifications are systematic — all 10 windows of a given run vote for the same wrong class, revealing that the confusion is about the fundamental spectral signature, not noise.
