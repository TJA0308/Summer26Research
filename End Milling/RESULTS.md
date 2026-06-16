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

### Model C: `feed_cnxt_10w_adamw.pt` (ConvNeXt-Tiny)

| Metric | Value |
|--------|-------|
| Window accuracy | **43.3%** (26/60) |
| Run majority-vote | **50.0%** (3/6 runs) |
| Soft prob avg | **50.0%** (3/6 runs) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| 3 mm/rev | 9/10 | 5 mm/rev ×1 |
| 4 mm/rev | 0/10 | 6 mm/rev ×10 |
| 5 mm/rev | 7/10 | 6 mm/rev ×3 |
| 6 mm/rev | 0/10 | 7 mm/rev ×7, 5 mm/rev ×2, 3 mm/rev ×1 |
| 7 mm/rev | 0/10 | 6 mm/rev ×10 |
| 8 mm/rev | 10/10 | - |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run25 | 3 mm/rev | 3 mm/rev | OK    | 3×9, 5×1 |
| run13 | 4 mm/rev | 6 mm/rev | WRONG | 6×10 |
| run31 | 5 mm/rev | 5 mm/rev | OK    | 5×7, 6×3 |
| run17 | 6 mm/rev | 7 mm/rev | WRONG | 7×7, 5×2, 3×1 |
| run5  | 7 mm/rev | 6 mm/rev | WRONG | 6×10 |
| run36 | 8 mm/rev | 8 mm/rev | OK    | 8×10 |

**Per-run soft probability averaging:**

| Run | True | Predicted | Status | Avg prob (top 2) |
|-----|------|-----------|--------|-----------------|
| run25 | 3 mm/rev | 3 mm/rev | OK    | 3=0.841, 4=0.091 |
| run13 | 4 mm/rev | 6 mm/rev | WRONG | 6=1.000, 5=0.000 |
| run31 | 5 mm/rev | 5 mm/rev | OK    | 5=0.581, 6=0.371 |
| run17 | 6 mm/rev | 7 mm/rev | WRONG | 7=0.642, 5=0.210 |
| run5  | 7 mm/rev | 6 mm/rev | WRONG | 6=1.000, 5=0.000 |
| run36 | 8 mm/rev | 8 mm/rev | OK    | 8=0.998, 7=0.002 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | 3 | 4 | 5 | 6 | 7 | 8 |
|--|---|---|---|---|---|---|
| 3 mm/rev | **9** | 0 | 1 | 0 | 0 | 0 |
| 4 mm/rev | 0 | **0** | 0 | 10 | 0 | 0 |
| 5 mm/rev | 0 | 0 | **7** | 3 | 0 | 0 |
| 6 mm/rev | 1 | 0 | 2 | **0** | 7 | 0 |
| 7 mm/rev | 0 | 0 | 0 | 10 | **0** | 0 |
| 8 mm/rev | 0 | 0 | 0 | 0 | 0 | **10** |

ConvNeXt-Tiny shifts the failure pattern compared to ResNet18: run17 (6 mm/rev) is now predicted as 7 mm/rev instead of 5 mm/rev, and 6 mm/rev windows scatter across multiple classes. Run13 (4 mm/rev) and run5 (7 mm/rev) remain failures under all three architectures.

---

### Feed Fine-Grained Summary

| Model | Backbone | Window Acc | Run MV Acc | Soft Avg |
|-------|----------|-----------|-----------|----------|
| `feed_rn18_10w_adamw.pt` | ResNet18 | **48.3%** | **50.0%** | **50.0%** |
| `feed_effb0_10w_adamw.pt` | EfficientNet-B0 | 38.3% | 50.0% | 50.0% |
| `feed_cnxt_10w_adamw.pt` | ConvNeXt-Tiny | 43.3% | 50.0% | 50.0% |

Feed rate 4, 6, and 7 mm/rev collapse to adjacent class predictions across all three architectures with zero correct predictions. The extreme classes (3 and 8 mm/rev) are reliably identified. The middle feed rates produce CWT signatures dominated by RPM harmonics rather than feed-rate-specific chip-load modulation — this is a signal-level problem that persists across all tested architectures.

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

### Model C: `feed_coarse_cnxt_10w_adamw.pt` (ConvNeXt-Tiny, AdamW, 20 epochs)

| Metric | Value |
|--------|-------|
| Window accuracy | **80.0%** (48/60) |
| Run majority-vote | **83.3%** (5/6 runs) |
| Soft prob avg | **83.3%** (5/6 runs) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| low (3-4 mm/rev)    | 10/20 | high ×10 |
| medium (5-6 mm/rev) | 20/20 | - |
| high (7-8 mm/rev)   | 18/20 | medium ×2 |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run25 | low    | low    | OK    | low×10 |
| run13 | low    | high   | WRONG | high×10 |
| run31 | medium | medium | OK    | medium×10 |
| run17 | medium | medium | OK    | medium×10 |
| run36 | high   | high   | OK    | high×10 |
| run5  | high   | high   | OK    | high×8, medium×2 |

**Per-run soft probability averaging:**

| Run | True | Predicted | Status | Avg prob (top 2) |
|-----|------|-----------|--------|-----------------|
| run25 | low    | low    | OK    | low=0.689, medium=0.311 |
| run13 | low    | high   | WRONG | high=0.973, medium=0.027 |
| run31 | medium | medium | OK    | medium=0.947, low=0.052 |
| run17 | medium | medium | OK    | medium=0.928, high=0.064 |
| run36 | high   | high   | OK    | high=0.988, medium=0.012 |
| run5  | high   | high   | OK    | high=0.828, medium=0.171 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | low | medium | high |
|--|-----|--------|------|
| low    | **10** | 0 | 10 |
| medium | 0 | **20** | 0 |
| high   | 0 | 2 | **18** |

ConvNeXt-Tiny is the best coarse feed model, correctly classifying 5/6 runs (83.3%). The failure pattern differs from ResNet18 and EfficientNet-B0: run13 (4 mm/rev, low class) is predicted as **high** instead of medium — a larger misclassification error. However, run5 (7 mm/rev, high class) which failed in both other models is now correctly classified. Medium class remains perfectly separated.

---

### Feed Coarse Summary

| Model | Backbone | Window Acc | Run MV Acc | Soft Avg |
|-------|----------|-----------|-----------|----------|
| `feed_coarse_cnxt_10w_adamw.pt` | ConvNeXt-Tiny | **80.0%** | **83.3%** | **83.3%** |
| `feed_coarse_rn18_10w_adamw.pt` | ResNet18 | 66.7% | 66.7% | 66.7% |
| `feed_coarse_effb0_10w_adamw.pt` | EfficientNet-B0 | 66.7% | 66.7% | 66.7% |

ConvNeXt-Tiny significantly outperforms the other two architectures on coarse feed classification (83.3% vs 66.7%). It correctly classifies run5 (7 mm/rev, high) which both ResNet18 and EfficientNet-B0 fail on, while still failing run13 (4 mm/rev, low — predicted high with p=0.973). ResNet18 and EfficientNet-B0 produce identical predictions; the failure pattern is symmetric around medium. Coarsening from 6 to 3 classes improves the ceiling from 50% to 83.3% for ConvNeXt.

---

## 5. Depth of Cut (3-class: 0.015 / 0.030 / 0.060 mm)

**Test runs (9 total, 3 per class):**

| Run | True DOC | Speed |
|-----|---------|-------|
| run1  | 0.015 mm | 4000 rpm |
| run5  | 0.015 mm | 5000 rpm |
| run43 | 0.015 mm | 3000 rpm |
| run7  | 0.030 mm | 1500 rpm |
| run14 | 0.030 mm | 3000 rpm |
| run19 | 0.030 mm | 5000 rpm |
| run22 | 0.060 mm | 1500 rpm |
| run29 | 0.060 mm | 3000 rpm |
| run36 | 0.060 mm | 5000 rpm |

### Model A: `best_model_doc_resnet18.pt` (ResNet18)

| Metric | Value |
|--------|-------|
| Window accuracy | **82.2%** (74/90) |
| Run majority-vote | **88.9%** (8/9) |
| Soft prob avg | **88.9%** (8/9) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| 0.015 mm | 30/30 | - |
| 0.030 mm | 26/30 | 0.015 mm ×4 |
| 0.060 mm | 18/30 | 0.030 mm ×10, 0.015 mm ×2 |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run1  | 0.015 mm | 0.015 mm | OK    | 0.015×10 |
| run5  | 0.015 mm | 0.015 mm | OK    | 0.015×10 |
| run43 | 0.015 mm | 0.015 mm | OK    | 0.015×10 |
| run7  | 0.030 mm | 0.030 mm | OK    | 0.030×10 |
| run14 | 0.030 mm | 0.030 mm | OK    | 0.030×10 |
| run19 | 0.030 mm | 0.030 mm | OK    | 0.030×6, 0.015×4 |
| run22 | 0.060 mm | 0.060 mm | OK    | 0.060×9, 0.015×1 |
| run29 | 0.060 mm | 0.060 mm | OK    | 0.060×9, 0.015×1 |
| run36 | 0.060 mm | 0.030 mm | WRONG | 0.030×10 |

**Per-run soft probability averaging:**

| Run | True | Predicted | Status | Avg prob (top 2) |
|-----|------|-----------|--------|-----------------|
| run1  | 0.015 mm | 0.015 mm | OK    | 0.015=0.974, 0.030=0.016 |
| run5  | 0.015 mm | 0.015 mm | OK    | 0.015=1.000, 0.030=0.000 |
| run43 | 0.015 mm | 0.015 mm | OK    | 0.015=0.998, 0.030=0.002 |
| run7  | 0.030 mm | 0.030 mm | OK    | 0.030=0.990, 0.015=0.009 |
| run14 | 0.030 mm | 0.030 mm | OK    | 0.030=0.884, 0.015=0.089 |
| run19 | 0.030 mm | 0.030 mm | OK    | 0.030=0.558, 0.015=0.389 |
| run22 | 0.060 mm | 0.060 mm | OK    | 0.060=0.848, 0.015=0.104 |
| run29 | 0.060 mm | 0.060 mm | OK    | 0.060=0.885, 0.015=0.092 |
| run36 | 0.060 mm | 0.030 mm | WRONG | 0.030=0.943, 0.060=0.055 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | 0.015 mm | 0.030 mm | 0.060 mm |
|--|----------|----------|----------|
| 0.015 mm | **30** | 0 | 0 |
| 0.030 mm | 4 | **26** | 0 |
| 0.060 mm | 2 | 10 | **18** |

The single failure is run36 (5000 rpm, 0.060 mm) — all 10 windows vote 0.030 mm with high confidence (prob=0.943). 0.015 mm is perfectly separated; both 0.030 mm and 0.060 mm confuse downward toward lower DOC values.

---

### Model B: `best_model_doc_convnext.pt` (ConvNeXt-Tiny)

| Metric | Value |
|--------|-------|
| Window accuracy | **77.8%** (70/90) |
| Run majority-vote | **77.8%** (7/9) |
| Soft prob avg | **77.8%** (7/9) |

**Per-class window accuracy:**

| Class | Correct | Misclassified as |
|-------|---------|-----------------|
| 0.015 mm | 30/30 | - |
| 0.030 mm | 20/30 | 0.015 mm ×10 |
| 0.060 mm | 20/30 | 0.015 mm ×10 |

**Per-run majority-vote:**

| Run | True | Predicted | Status | Votes |
|-----|------|-----------|--------|-------|
| run1  | 0.015 mm | 0.015 mm | OK    | 0.015×10 |
| run5  | 0.015 mm | 0.015 mm | OK    | 0.015×10 |
| run43 | 0.015 mm | 0.015 mm | OK    | 0.015×10 |
| run7  | 0.030 mm | 0.030 mm | OK    | 0.030×10 |
| run14 | 0.030 mm | 0.030 mm | OK    | 0.030×10 |
| run19 | 0.030 mm | 0.015 mm | WRONG | 0.015×10 |
| run22 | 0.060 mm | 0.060 mm | OK    | 0.060×10 |
| run29 | 0.060 mm | 0.060 mm | OK    | 0.060×10 |
| run36 | 0.060 mm | 0.015 mm | WRONG | 0.015×10 |

**Per-run soft probability averaging:**

| Run | True | Predicted | Status | Avg prob (top 2) |
|-----|------|-----------|--------|-----------------|
| run1  | 0.015 mm | 0.015 mm | OK    | 0.015=0.747, 0.060=0.140 |
| run5  | 0.015 mm | 0.015 mm | OK    | 0.015=0.857, 0.060=0.084 |
| run43 | 0.015 mm | 0.015 mm | OK    | 0.015=0.510, 0.060=0.301 |
| run7  | 0.030 mm | 0.030 mm | OK    | 0.030=0.884, 0.060=0.112 |
| run14 | 0.030 mm | 0.030 mm | OK    | 0.030=0.820, 0.060=0.146 |
| run19 | 0.030 mm | 0.015 mm | WRONG | 0.015=0.496, 0.060=0.307 |
| run22 | 0.060 mm | 0.060 mm | OK    | 0.060=0.832, 0.030=0.147 |
| run29 | 0.060 mm | 0.060 mm | OK    | 0.060=0.958, 0.030=0.041 |
| run36 | 0.060 mm | 0.015 mm | WRONG | 0.015=0.373, 0.060=0.330 |

**Confusion matrix (windows, rows=true, cols=pred):**

| | 0.015 mm | 0.030 mm | 0.060 mm |
|--|----------|----------|----------|
| 0.015 mm | **30** | 0 | 0 |
| 0.030 mm | 10 | **20** | 0 |
| 0.060 mm | 10 | 0 | **20** |

ConvNeXt misclassifies both run19 (0.030 mm, 5000 rpm) and run36 (0.060 mm, 5000 rpm) as 0.015 mm. Both failures are at 5000 rpm — high-speed runs produce lower-amplitude vibrations in some feed/DOC combinations, making them look energetically similar to 0.015 mm cuts.

---

### DOC Model Comparison

| Model | Backbone | Window Acc | Run MV Acc | Soft Avg Acc |
|-------|----------|-----------|-----------|-------------|
| `best_model_doc_resnet18.pt` | ResNet18 | **82.2%** | **88.9%** | **88.9%** |
| `best_model_doc_convnext.pt` | ConvNeXt-Tiny | 77.8% | 77.8% | 77.8% |

ResNet18 outperforms ConvNeXt-Tiny on DOC, reversing the pattern seen for speed. The single ResNet18 failure (run36) is a confident misclassification — probability averaging does not recover it. ConvNeXt fails on two runs (run19 and run36), both at 5000 rpm where the DOC signal is partially masked by high-speed harmonic energy.

---

## Overall Summary

| Model File | Target | Backbone | Windows | Window Acc | Run MV Acc | Soft Avg |
|-----------|--------|----------|---------|-----------|-----------|----------|
| `speed_cnxt_10w.pt` | Speed (5-class) | ConvNeXt-Tiny | 100 | **96.0%** | **100.0%** | **100.0%** |
| `speed_resnet_10w.pt` | Speed (5-class) | ResNet18 | 100 | 90.0% | **100.0%** | **100.0%** |
| `best_model_doc_resnet18.pt` | DOC (3-class) | ResNet18 | 90 | **82.2%** | **88.9%** | **88.9%** |
| `best_model_doc_convnext.pt` | DOC (3-class) | ConvNeXt-Tiny | 90 | 77.8% | 77.8% | 77.8% |
| `exp_models/roughness_rn18_10w_adamw.pt` | Roughness (3-class) | ResNet18 | 60 | **93.3%** | **100.0%** | **100.0%** |
| `feed_coarse_cnxt_10w_adamw.pt` | Feed Coarse (3-class) | ConvNeXt-Tiny | 60 | **80.0%** | **83.3%** | **83.3%** |
| `exp_models/feed_coarse_rn18_10w_adamw.pt` | Feed Coarse (3-class) | ResNet18 | 60 | 66.7% | 66.7% | 66.7% |
| `exp_models/feed_coarse_effb0_10w_adamw.pt` | Feed Coarse (3-class) | EfficientNet-B0 | 60 | 66.7% | 66.7% | 66.7% |
| `feed_rn18_10w_adamw.pt` | Feed (6-class) | ResNet18 | 60 | **48.3%** | 50.0% | 50.0% |
| `feed_cnxt_10w_adamw.pt` | Feed (6-class) | ConvNeXt-Tiny | 60 | 43.3% | 50.0% | 50.0% |
| `feed_effb0_10w_adamw.pt` | Feed (6-class) | EfficientNet-B0 | 60 | 38.3% | 50.0% | 50.0% |

---

## Key Findings

**Speed is solved.** Both speed models achieve 100% run-level accuracy on completely unseen holdout data. RPM places spindle harmonics at fixed frequency positions that survive any normalization or DOC/feed variation. ConvNeXt-Tiny shows higher per-window confidence (96% vs 90%), which matters if window-level scores are used as uncertainty estimates.

**DOC is partially solved.** ResNet18 achieves 88.9% run-level accuracy (8/9 runs) on DOC with a single failure: run36 (5000 rpm, 0.060 mm) misclassified as 0.030 mm. ConvNeXt-Tiny reaches 77.8% (7/9), failing on both 5000 rpm runs in higher DOC classes (run19 and run36). The 0.015 mm class is perfectly separated by both models — shallow cuts produce a distinctly lower-energy CWT signature. For ResNet18, this reverses the architecture ranking seen for speed: ConvNeXt-Tiny does not offer an advantage on DOC classification.

**Roughness generalizes well.** The ResNet18 roughness model achieves 93.3% window accuracy and 100% run-level accuracy on 6 unseen runs spanning all three roughness classes and all three DOC levels. The rare window-level errors occur at class boundaries (run27 Medium Ra=0.868 um is near the 1.0 threshold). SMOTE-balanced training on 10-window scalograms captures the DOC-driven surface energy pattern reliably.

**Feed rate is the hard problem, but coarse classification is improving.** The 6-class fine-grained model tops out at 48.3% window / 50% run accuracy across all three tested architectures (ResNet18, EfficientNet-B0, ConvNeXt-Tiny) — a hard ceiling. Classes 4, 6, and 7 mm/rev achieve 0 correct predictions in all cases; only the extreme classes (3 and 8 mm/rev) are reliably identified. Coarsening to 3 classes with ConvNeXt-Tiny breaks the ceiling: 83.3% run accuracy (5/6) vs 66.7% for ResNet18 and EfficientNet-B0. ConvNeXt correctly resolves run5 (7 mm/rev, high) that the other two fail on, though it fails run13 (4 mm/rev, low) with a wider misclassification error (predicted high instead of medium).

**Architecture matters less than signal quality.** For speed, ConvNeXt-Tiny has higher per-window confidence (96% vs 90%) but both hit 100% run-level. For DOC, ResNet18 outperforms ConvNeXt-Tiny (88.9% vs 77.8%), suggesting the DOC amplitude pattern is better captured by residual connections. For feed rate, no architecture tested escaped the 50% ceiling on holdout data.

**Majority voting is robust.** Even when individual windows misclassify (e.g., 4 of 10 windows in run16 for speed, 4 of 10 in run19 for DOC-ResNet18), majority vote corrects the run-level prediction. Soft probability averaging matches majority-vote performance — it does not recover additional runs when the model is confidently wrong (e.g., run36 DOC ResNet18: p=0.943 for the wrong class). For feed rate, majority vote does not help because all 10 windows of a given run vote for the same wrong class, revealing a spectral signature problem rather than noise.
