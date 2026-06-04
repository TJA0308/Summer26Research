# CWT vs SES 4-Channel CNN Results — v2

**Regularisation:** label_smooth=0.05, mixup=alpha=0.2  
**Backbones:** ResNet18 (RN18), ResNet50 (RN50), EfficientNet-B0 (ENB0), ConvNeXt-Tiny (CNXT) — all ImageNet pretrained  
**Optimizer:** AdamW · weight_decay=1e-4 · cosine LR scheduler  
**LR tested:** 1e-3 and 1e-4  
**SMOTE:** applied to balance training classes  
**Weighted loss:** feed_coarse only (imbalanced: Low/Med/High)  
**Epochs:** speed=30, doc=33, roughness=33, feed_coarse=33

---

## Pipelines

### Pipeline A — Standard CWT (scalograms_10w, cnn_train.py)
- Input: 3-channel RGB PNG, 224×224
- Signal: CWT of raw ai4 accelerometer
- Augmentation: random horizontal flip (--augment light)
- SMOTE CSVs auto-loaded

### Pipeline B — SES 4-Channel (scalograms_ses_10w, cnn_train_hilbert.py)
- Input: 4-channel float32 .npy (ch0: ai4 CWT, ch1: ai6 CWT, ch2: SES(ai4), ch3: SES(ai6))
- 4th conv channel seeded from average of pretrained 3-channel weights
- SMOTE loaded via --smote

---

## Training / Test Splits

| Target | Train | Test |
|--------|------:|-----:|
| Speed (5-class) | 30 runs (6/class) | 15 runs (3/class, one per DOC) |
| DOC (3-class) | 33 runs (11/class) | 12 runs (4/class) |
| Roughness (3-class) | 33 runs (~19/7/7) | 12 runs (4/class) |
| Feed Coarse (3-class) | 33 runs (11/17/5) | 12 runs (4/class) |

> **Note:** Per-window tables below use legacy eval holdout sets (10 runs std speed, 15 runs ses speed, 9 runs std DOC, 14 runs ses DOC, 6 runs roughness/feed) for continuity with v1 reporting.

---
## Speed — 5-class (1500 / 2000 / 3000 / 4000 / 5000 rpm) | 30 epochs

### Training Data

| Pipeline | Real Runs | Runs/Class | SMOTE | Effective/Class |
|----------|----------:|----------:|-------|----------------:|
| A (Std CWT) | 30 | 6 | +2/class | 8 |
| B (SES 4-ch) | 30 | 6 | +2/class | 8 |

### Results — Pipeline A (Std CWT) — eval on 15-run test set (3/class × 5 RPM)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 91.3% | 92.0% |
| ResNet50 | **100.0%** | 96.7% |
| EfficientNet-B0 | 91.3% | 86.7% |
| ConvNeXt-Tiny | 20.0% ❌ | 90.0% |

### Results — Pipeline B (SES 4-Channel) — eval on 15-run test set (3/class × 5 RPM)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 95.3% | 89.3% |
| ResNet50 | 96.0% | 94.7% |
| EfficientNet-B0 | 94.0% | 79.3% |
| ConvNeXt-Tiny | 30.0% ❌ | 92.0% |

### Per-Window — Pipeline A (legacy holdout)

**ResNet18 lr=1e-3** (std_speed_rn18_lr1e3) — Run MV: **100.0%** (10/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 4000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **100.0%** (10/10)

**ResNet18 lr=1e-4** (std_speed_rn18_lr1e4) — Run MV: **90.0%** (9/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 2000 | ✗ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **90.0%** (9/10)

**ResNet50 lr=1e-3** (std_speed_rn50_lr1e3) — Run MV: **100.0%** (10/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 4000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **100.0%** (10/10)

**ResNet50 lr=1e-4** (std_speed_rn50_lr1e4) — Run MV: **90.0%** (9/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 5000 | ✗ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **90.0%** (9/10)

**EfficientNet-B0 lr=1e-3** (std_speed_enb0_lr1e3) — Run MV: **80.0%** (8/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 5000 | ✗ |
| run16 | 4000 | 2000 | ✗ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **80.0%** (8/10)

**EfficientNet-B0 lr=1e-4** (std_speed_enb0_lr1e4) — Run MV: **90.0%** (9/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 4000 | ✗ |
| run16 | 4000 | 4000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **90.0%** (9/10)

**ConvNeXt-Tiny lr=1e-3** (std_speed_cnxt_lr1e3) — Run MV: **20.0%** (2/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 1500 | ✗ |
| run15 | 3000 | 1500 | ✗ |
| run16 | 4000 | 1500 | ✗ |
| run2 | 4000 | 1500 | ✗ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 1500 | ✗ |
| run28 | 3000 | 1500 | ✗ |
| run36 | 5000 | 1500 | ✗ |
| run5 | 5000 | 1500 | ✗ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **20.0%** (2/10)

**ConvNeXt-Tiny lr=1e-4** (std_speed_cnxt_lr1e4) — Run MV: **80.0%** (8/10)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 2000 | ✗ |
| run16 | 4000 | 5000 | ✗ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **80.0%** (8/10)

### Per-Window — Pipeline B (legacy holdout)

**ResNet18 lr=1e-3** (ses_speed_rn18_lr1e3) — Run MV: **93.3%** (14/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 2000 | ✗ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **93.3%** (14/15)

**ResNet18 lr=1e-4** (ses_speed_rn18_lr1e4) — Run MV: **93.3%** (14/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 4000 | ✓ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 5000 | ✗ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **93.3%** (14/15)

**ResNet50 lr=1e-3** (ses_speed_rn50_lr1e3) — Run MV: **93.3%** (14/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 2000 | ✗ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **93.3%** (14/15)

**ResNet50 lr=1e-4** (ses_speed_rn50_lr1e4) — Run MV: **86.7%** (13/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 1500 | ✗ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 5000 | ✗ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **86.7%** (13/15)

**EfficientNet-B0 lr=1e-3** (ses_speed_enb0_lr1e3) — Run MV: **86.7%** (13/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 2000 | ✗ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 1500 | ✗ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **86.7%** (13/15)

**EfficientNet-B0 lr=1e-4** (ses_speed_enb0_lr1e4) — Run MV: **80.0%** (12/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 2000 | ✗ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 1500 | ✗ |
| run28 | 3000 | 2000 | ✗ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **80.0%** (12/15)

**ConvNeXt-Tiny lr=1e-3** (ses_speed_cnxt_lr1e3) — Run MV: **93.3%** (14/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 5000 | ✗ |
| run16 | 4000 | 4000 | ✓ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **93.3%** (14/15)

**ConvNeXt-Tiny lr=1e-4** (ses_speed_cnxt_lr1e4) — Run MV: **80.0%** (12/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 2000 | ✗ |
| run16 | 4000 | 4000 | ✓ |
| run19 | 5000 | 5000 | ✓ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 2000 | ✓ |
| run28 | 3000 | 2000 | ✗ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 5000 | ✓ |
| run37 | 1500 | 1500 | ✓ |
| run40 | 2000 | 2000 | ✓ |
| run43 | 3000 | 5000 | ✗ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Run MV accuracy: **80.0%** (12/15)

---

## DOC — 3-class (0.015 / 0.030 / 0.060 mm) | 33 epochs

### Training Data

| Pipeline | Real Runs | Class Distribution | SMOTE |
|----------|----------:|------------------|-------|
| A (Std CWT) | 33 | 11/11/11 (balanced) | none |
| B (SES 4-ch) | 33 | 11/11/11 (balanced) | none |

### Results — Pipeline A (Std CWT) — eval on 12-run test set (4/class × 3 DOC)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 77.5% | 84.2% |
| ResNet50 | 89.2% | 90.0% |
| EfficientNet-B0 | 93.3% | 95.0% |
| ConvNeXt-Tiny | 33.3% ❌ | 88.3% |

### Results — Pipeline B (SES 4-Channel) — eval on 12-run test set (4/class × 3 DOC)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 88.3% | 78.3% |
| ResNet50 | 87.5% | 88.3% |
| EfficientNet-B0 | 95.0% | 77.5% |
| ConvNeXt-Tiny | 33.3% ❌ | 81.7% |

### Per-Window — Pipeline A (legacy holdout)

**ResNet18 lr=1e-3** (std_doc_rn18_lr1e3) — Run MV: **77.8%** (7/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **77.8%** (7/9)

**ResNet18 lr=1e-4** (std_doc_rn18_lr1e4) — Run MV: **88.9%** (8/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **88.9%** (8/9)

**ResNet50 lr=1e-3** (std_doc_rn50_lr1e3) — Run MV: **77.8%** (7/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .015 | ✗ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .060 | ✗ |

Run MV accuracy: **77.8%** (7/9)

**ResNet50 lr=1e-4** (std_doc_rn50_lr1e4) — Run MV: **77.8%** (7/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run19 | .030 | .060 | ✗ |
| run22 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **77.8%** (7/9)

**EfficientNet-B0 lr=1e-3** (std_doc_enb0_lr1e3) — Run MV: **88.9%** (8/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **88.9%** (8/9)

**EfficientNet-B0 lr=1e-4** (std_doc_enb0_lr1e4) — Run MV: **100.0%** (9/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **100.0%** (9/9)

**ConvNeXt-Tiny lr=1e-3** (std_doc_cnxt_lr1e3) — Run MV: **33.3%** (3/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .015 | ✗ |
| run19 | .030 | .015 | ✗ |
| run22 | .060 | .015 | ✗ |
| run29 | .060 | .015 | ✗ |
| run36 | .060 | .015 | ✗ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .015 | ✗ |

Run MV accuracy: **33.3%** (3/9)

**ConvNeXt-Tiny lr=1e-4** (std_doc_cnxt_lr1e4) — Run MV: **100.0%** (9/9)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **100.0%** (9/9)

### Per-Window — Pipeline B (legacy holdout)

**ResNet18 lr=1e-3** (ses_doc_rn18_lr1e3) — Run MV: **85.7%** (12/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .030 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **85.7%** (12/14)

**ResNet18 lr=1e-4** (ses_doc_rn18_lr1e4) — Run MV: **85.7%** (12/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .015 | ✗ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **85.7%** (12/14)

**ResNet50 lr=1e-3** (ses_doc_rn50_lr1e3) — Run MV: **78.6%** (11/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .030 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .060 | ✗ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **78.6%** (11/14)

**ResNet50 lr=1e-4** (ses_doc_rn50_lr1e4) — Run MV: **78.6%** (11/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .015 | ✗ |
| run14 | .030 | .015 | ✗ |
| run16 | .030 | .015 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **78.6%** (11/14)

**EfficientNet-B0 lr=1e-3** (ses_doc_enb0_lr1e3) — Run MV: **85.7%** (12/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .015 | ✗ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **85.7%** (12/14)

**EfficientNet-B0 lr=1e-4** (ses_doc_enb0_lr1e4) — Run MV: **78.6%** (11/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .015 | ✗ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .015 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **78.6%** (11/14)

**ConvNeXt-Tiny lr=1e-3** (ses_doc_cnxt_lr1e3) — Run MV: **35.7%** (5/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .015 | ✗ |
| run14 | .030 | .015 | ✗ |
| run16 | .030 | .015 | ✗ |
| run19 | .030 | .015 | ✗ |
| run22 | .060 | .015 | ✗ |
| run25 | .060 | .015 | ✗ |
| run29 | .060 | .015 | ✗ |
| run36 | .060 | .015 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .015 | ✗ |

Run MV accuracy: **35.7%** (5/14)

**ConvNeXt-Tiny lr=1e-4** (ses_doc_cnxt_lr1e4) — Run MV: **78.6%** (11/14)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run11 | .030 | .015 | ✗ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .060 | ✗ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run43 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Run MV accuracy: **78.6%** (11/14)

---

## Roughness — 3-class (Smooth Ra<0.7 / Medium 0.7-1.0 / Rough Ra>1.0 μm) | 33 epochs

### Training Data

| Pipeline | Real Runs | Class Distribution | SMOTE |
|----------|----------:|------------------|-------|
| A (Std CWT) | 33 | ~19 Smooth / 7 Medium / 7 Rough | +SMOTE |
| B (SES 4-ch) | 33 | ~19 Smooth / 7 Medium / 7 Rough | +SMOTE |

### Results — Pipeline A (Std CWT) — eval on 12-run test set (4/class × 3 Ra)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 91.7% | 87.5% |
| ResNet50 | 83.3% | 86.7% |
| EfficientNet-B0 | 91.7% | 88.3% |
| ConvNeXt-Tiny | 33.3% ❌ | 88.3% |

### Results — Pipeline B (SES 4-Channel) — eval on 12-run test set (4/class × 3 Ra)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 83.3% | 80.8% |
| ResNet50 | 83.3% | 83.3% |
| EfficientNet-B0 | 85.8% | 76.7% |
| ConvNeXt-Tiny | 64.2% | 83.3% |

### Per-Window — Pipeline A (legacy holdout)

**ResNet18 lr=1e-3** (std_roughness_rn18_lr1e3) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ResNet18 lr=1e-4** (std_roughness_rn18_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ResNet50 lr=1e-3** (std_roughness_rn50_lr1e3) — Run MV: **100.0%** (6/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Rgh | ✓ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **100.0%** (6/6)

**ResNet50 lr=1e-4** (std_roughness_rn50_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**EfficientNet-B0 lr=1e-3** (std_roughness_enb0_lr1e3) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**EfficientNet-B0 lr=1e-4** (std_roughness_enb0_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ConvNeXt-Tiny lr=1e-3** (std_roughness_cnxt_lr1e3) — Run MV: **33.3%** (2/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Rgh | ✓ |
| run27 | Med | Rgh | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Rgh | ✗ |
| run5 | Smt | Rgh | ✗ |
| run7 | Med | Rgh | ✗ |

Run MV accuracy: **33.3%** (2/6)

**ConvNeXt-Tiny lr=1e-4** (std_roughness_cnxt_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

### Per-Window — Pipeline B (legacy holdout)

**ResNet18 lr=1e-3** (ses_roughness_rn18_lr1e3) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ResNet18 lr=1e-4** (ses_roughness_rn18_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ResNet50 lr=1e-3** (ses_roughness_rn50_lr1e3) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ResNet50 lr=1e-4** (ses_roughness_rn50_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**EfficientNet-B0 lr=1e-3** (ses_roughness_enb0_lr1e3) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**EfficientNet-B0 lr=1e-4** (ses_roughness_enb0_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ConvNeXt-Tiny lr=1e-3** (ses_roughness_cnxt_lr1e3) — Run MV: **33.3%** (2/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Smt | ✗ |
| run34 | Rgh | Smt | ✗ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Smt | ✗ |

Run MV accuracy: **33.3%** (2/6)

**ConvNeXt-Tiny lr=1e-4** (ses_roughness_cnxt_lr1e4) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Run MV accuracy: **83.3%** (5/6)

---

## Feed Coarse — 3-class (Low 3-4 / Medium 5-6 / High 7-8 mm/rev) | 33 epochs

### Training Data

| Pipeline | Real Runs | Class Distribution | SMOTE | Weighted Loss |
|----------|----------:|------------------|-------|:-------------:|
| A (Std CWT) | 33 | 11 Low / 17 Med / 5 High | +SMOTE | ✓ |
| B (SES 4-ch) | 33 | 11 Low / 17 Med / 5 High | +SMOTE | ✓ |

### Results — Pipeline A (Std CWT) — eval on 12-run test set (4/class × 3 feed)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 75.0% | 75.0% |
| ResNet50 | 77.5% | 70.8% |
| EfficientNet-B0 | 74.2% | 75.0% |
| ConvNeXt-Tiny | 75.8% | 81.7% |

### Results — Pipeline B (SES 4-Channel) — eval on 12-run test set (4/class × 3 feed)

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 72.5% | 71.7% |
| ResNet50 | 72.5% | 68.3% |
| EfficientNet-B0 | 75.0% | 70.8% |
| ConvNeXt-Tiny | 39.2% ❌ | 80.0% |

### Per-Window — Pipeline A (legacy holdout)

**ResNet18 lr=1e-3** (std_feed_rn18_lr1e3) — Run MV: **83.3%** (5/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Hi | ✓ |

Run MV accuracy: **83.3%** (5/6)

**ResNet18 lr=1e-4** (std_feed_rn18_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**ResNet50 lr=1e-3** (std_feed_rn50_lr1e3) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Hi | ✗ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Hi | ✓ |

Run MV accuracy: **66.7%** (4/6)

**ResNet50 lr=1e-4** (std_feed_rn50_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**EfficientNet-B0 lr=1e-3** (std_feed_enb0_lr1e3) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**EfficientNet-B0 lr=1e-4** (std_feed_enb0_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**ConvNeXt-Tiny lr=1e-3** (std_feed_cnxt_lr1e3) — Run MV: **33.3%** (2/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Hi | ✗ |
| run17 | Med | Hi | ✗ |
| run25 | Low | Hi | ✗ |
| run31 | Med | Hi | ✗ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Hi | ✓ |

Run MV accuracy: **33.3%** (2/6)

**ConvNeXt-Tiny lr=1e-4** (std_feed_cnxt_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

### Per-Window — Pipeline B (legacy holdout)

**ResNet18 lr=1e-3** (ses_feed_rn18_lr1e3) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**ResNet18 lr=1e-4** (ses_feed_rn18_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**ResNet50 lr=1e-3** (ses_feed_rn50_lr1e3) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Low | ✗ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Hi | ✓ |

Run MV accuracy: **66.7%** (4/6)

**ResNet50 lr=1e-4** (ses_feed_rn50_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**EfficientNet-B0 lr=1e-3** (ses_feed_enb0_lr1e3) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**EfficientNet-B0 lr=1e-4** (ses_feed_enb0_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**ConvNeXt-Tiny lr=1e-3** (ses_feed_cnxt_lr1e3) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)

**ConvNeXt-Tiny lr=1e-4** (ses_feed_cnxt_lr1e4) — Run MV: **66.7%** (4/6)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run25 | Low | Low | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run5 | Hi | Med | ✗ |

Run MV accuracy: **66.7%** (4/6)
