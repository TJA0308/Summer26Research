# CNN Training Results — Pipeline A & Pipeline D

Comparison of two CWT-based classification pipelines across four milling process
parameter targets. Pipeline A uses a standard 3-channel RGB scalogram; Pipeline D
adds raw ai6 and SES channels as a full 4-channel input.

**Total experiments:** 96  (32 Pipeline A · 32 Pipeline D · 32 Pipeline D+SMOTE)

---

## Pipelines

### Pipeline A — Standard RGB CWT (`std`)

| Item | Detail |
|------|--------|
| Input | 3-channel PNG 224×224 |
| Channels | R=CWT(ai4 raw), G=CWT(ai6 raw), B=0 |
| Backbone | Unmodified ImageNet pretrained |
| Script | `cnn_model/cnn_train.py` |
| Scalograms | `scalograms_10w/` |

### Pipeline D — 4-Channel SES CWT (`ses4ch`)

| Item | Detail |
|------|--------|
| Input | 4-channel .npy 4×224×224 float32 [0,1] |
| ch0 | CWT(ai4 raw) |
| ch1 | CWT(ai6 raw) |
| ch2 | CWT(SES ai4) — squared envelope \|H{x}\|² |
| ch3 | CWT(SES ai6) — squared envelope \|H{x}\|² |
| Backbone | First conv patched to 4-ch (4th kernel = avg of 3-ch weights) |
| Script | `cnn_model/cnn_train_hilbert.py` |
| Scalograms | `scalograms_ses_4ch_10w/` |
| SMOTE | `cnn_model/smote_ses_4ch.py` — signal-space interpolation |

---

## Training Configuration

| Parameter | Value |
|-----------|-------|
| Optimizer | AdamW |
| Weight decay | 1e-4 |
| LR scheduler | Cosine annealing |
| Label smoothing | 0.05 |
| MixUp alpha | 0.2 |
| Batch size | 16 |
| Speed epochs | 30 |
| DOC / Roughness / Feed epochs | 33 |

---

## Data Splits

| Target | Train runs | Test runs | Test selection |
|--------|----------:|----------:|----------------|
| Speed (5-class) | 30 | 15 | 3/class × 5 RPM levels |
| DOC (3-class) | 33 | 12 | 4/class × 3 DOC levels |
| Roughness (3-class) | 33 | 12 | 4/class × 3 Ra classes |
| Feed Coarse (3-class) | 33 | 12 | 4/class × 3 feed rates |

Pipeline D uses `SPEED_TEST_RUNS_H` / `DOC_TEST_RUNS_H` from `cnn_train_hilbert.py` (balanced sets distinct from Pipeline A's splits).

---

## Speed (5-class, 30 epochs)

### Results — Pipeline A — Speed (5-class, 30 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 93.3% | 93.3% |
| ResNet50 | **100.0%** | **100.0%** |
| EfficientNet-B0 | 93.3% | 93.3% |
| ConvNeXt-Tiny | 20.0% ❌ | 93.3% |


### Results — Pipeline D — Speed (5-class, 30 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 93.3% | **100.0%** |
| ResNet50 | **100.0%** | **100.0%** |
| EfficientNet-B0 | 93.3% | 80.0% |
| ConvNeXt-Tiny | 53.3% | **100.0%** |


### Results — Pipeline D (SMOTE) — Speed (5-class, 30 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 93.3% | **100.0%** |
| ResNet50 | **100.0%** | **100.0%** |
| EfficientNet-B0 | 93.3% | 80.0% |
| ConvNeXt-Tiny | 53.3% | **100.0%** |


### Per-Run Detail — Pipeline A — Speed (5-class, 30 epochs)

**ResNet18 lr=1e-3** (`std_speed_rn18_lr1e3`) — Window: 91.3% | Run MV: **93.3%** (14/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 1500 | ✗ |
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

Window accuracy: **91.3%** (137/150)
Run MV accuracy: **93.3%** (14/15)

**ResNet18 lr=1e-4** (`std_speed_rn18_lr1e4`) — Window: 92.0% | Run MV: **93.3%** (14/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 5000 | ✗ |
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

Window accuracy: **92.0%** (138/150)
Run MV accuracy: **93.3%** (14/15)

**ResNet50 lr=1e-3** (`std_speed_rn50_lr1e3`) — Window: 100.0% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **100.0%** (150/150)
Run MV accuracy: **100.0%** (15/15)

**ResNet50 lr=1e-4** (`std_speed_rn50_lr1e4`) — Window: 96.7% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **96.7%** (145/150)
Run MV accuracy: **100.0%** (15/15)

**EfficientNet-B0 lr=1e-3** (`std_speed_enb0_lr1e3`) — Window: 91.3% | Run MV: **93.3%** (14/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 4000 | ✓ |
| run19 | 5000 | 1500 | ✗ |
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

Window accuracy: **91.3%** (137/150)
Run MV accuracy: **93.3%** (14/15)

**EfficientNet-B0 lr=1e-4** (`std_speed_enb0_lr1e4`) — Window: 86.7% | Run MV: **93.3%** (14/15)

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

Window accuracy: **86.7%** (130/150)
Run MV accuracy: **93.3%** (14/15)

**ConvNeXt-Tiny lr=1e-3** (`std_speed_cnxt_lr1e3`) — Window: 20.0% | Run MV: **20.0%** (3/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 4000 | ✗ |
| run15 | 3000 | 4000 | ✗ |
| run16 | 4000 | 4000 | ✓ |
| run19 | 5000 | 4000 | ✗ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 4000 | ✗ |
| run27 | 2000 | 4000 | ✗ |
| run28 | 3000 | 4000 | ✗ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 4000 | ✗ |
| run37 | 1500 | 4000 | ✗ |
| run40 | 2000 | 4000 | ✗ |
| run43 | 3000 | 4000 | ✗ |
| run5 | 5000 | 4000 | ✗ |
| run9 | 1500 | 4000 | ✗ |

Window accuracy: **20.0%** (30/150)
Run MV accuracy: **20.0%** (3/15)

**ConvNeXt-Tiny lr=1e-4** (`std_speed_cnxt_lr1e4`) — Window: 90.0% | Run MV: **93.3%** (14/15)

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

Window accuracy: **90.0%** (135/150)
Run MV accuracy: **93.3%** (14/15)

### Per-Run Detail — Pipeline D — Speed (5-class, 30 epochs)

**ResNet18 lr=1e-3** (`ses4ch_speed_rn18_lr1e3`) — Window: 94.7% | Run MV: **93.3%** (14/15)

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

Window accuracy: **94.7%** (142/150)
Run MV accuracy: **93.3%** (14/15)

**ResNet18 lr=1e-4** (`ses4ch_speed_rn18_lr1e4`) — Window: 92.7% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **92.7%** (139/150)
Run MV accuracy: **100.0%** (15/15)

**ResNet50 lr=1e-3** (`ses4ch_speed_rn50_lr1e3`) — Window: 98.0% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **98.0%** (147/150)
Run MV accuracy: **100.0%** (15/15)

**ResNet50 lr=1e-4** (`ses4ch_speed_rn50_lr1e4`) — Window: 93.3% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **93.3%** (140/150)
Run MV accuracy: **100.0%** (15/15)

**EfficientNet-B0 lr=1e-3** (`ses4ch_speed_enb0_lr1e3`) — Window: 92.7% | Run MV: **93.3%** (14/15)

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

Window accuracy: **92.7%** (139/150)
Run MV accuracy: **93.3%** (14/15)

**EfficientNet-B0 lr=1e-4** (`ses4ch_speed_enb0_lr1e4`) — Window: 77.3% | Run MV: **80.0%** (12/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 2000 | ✗ |
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

Window accuracy: **77.3%** (116/150)
Run MV accuracy: **80.0%** (12/15)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_speed_cnxt_lr1e3`) — Window: 50.7% | Run MV: **53.3%** (8/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 4000 | ✗ |
| run16 | 4000 | 5000 | ✗ |
| run19 | 5000 | 4000 | ✗ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 1500 | ✗ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 4000 | ✗ |
| run37 | 1500 | 5000 | ✗ |
| run40 | 2000 | 4000 | ✗ |
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **50.7%** (76/150)
Run MV accuracy: **53.3%** (8/15)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_speed_cnxt_lr1e4`) — Window: 97.3% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **97.3%** (146/150)
Run MV accuracy: **100.0%** (15/15)

### Per-Run Detail — Pipeline D (SMOTE) — Speed (5-class, 30 epochs)

**ResNet18 lr=1e-3** (`ses4ch_smote_speed_rn18_lr1e3`) — Window: 94.7% | Run MV: **93.3%** (14/15)

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

Window accuracy: **94.7%** (142/150)
Run MV accuracy: **93.3%** (14/15)

**ResNet18 lr=1e-4** (`ses4ch_smote_speed_rn18_lr1e4`) — Window: 92.7% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **92.7%** (139/150)
Run MV accuracy: **100.0%** (15/15)

**ResNet50 lr=1e-3** (`ses4ch_smote_speed_rn50_lr1e3`) — Window: 98.0% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **98.0%** (147/150)
Run MV accuracy: **100.0%** (15/15)

**ResNet50 lr=1e-4** (`ses4ch_smote_speed_rn50_lr1e4`) — Window: 93.3% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **93.3%** (140/150)
Run MV accuracy: **100.0%** (15/15)

**EfficientNet-B0 lr=1e-3** (`ses4ch_smote_speed_enb0_lr1e3`) — Window: 92.7% | Run MV: **93.3%** (14/15)

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

Window accuracy: **92.7%** (139/150)
Run MV accuracy: **93.3%** (14/15)

**EfficientNet-B0 lr=1e-4** (`ses4ch_smote_speed_enb0_lr1e4`) — Window: 77.3% | Run MV: **80.0%** (12/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | ✓ |
| run16 | 4000 | 2000 | ✗ |
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

Window accuracy: **77.3%** (116/150)
Run MV accuracy: **80.0%** (12/15)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_smote_speed_cnxt_lr1e3`) — Window: 50.7% | Run MV: **53.3%** (8/15)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run12 | 2000 | 2000 | ✓ |
| run15 | 3000 | 4000 | ✗ |
| run16 | 4000 | 5000 | ✗ |
| run19 | 5000 | 4000 | ✗ |
| run2 | 4000 | 4000 | ✓ |
| run22 | 1500 | 1500 | ✓ |
| run27 | 2000 | 1500 | ✗ |
| run28 | 3000 | 3000 | ✓ |
| run31 | 4000 | 4000 | ✓ |
| run36 | 5000 | 4000 | ✗ |
| run37 | 1500 | 5000 | ✗ |
| run40 | 2000 | 4000 | ✗ |
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **50.7%** (76/150)
Run MV accuracy: **53.3%** (8/15)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_smote_speed_cnxt_lr1e4`) — Window: 97.3% | Run MV: **100.0%** (15/15)

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
| run43 | 3000 | 3000 | ✓ |
| run5 | 5000 | 5000 | ✓ |
| run9 | 1500 | 1500 | ✓ |

Window accuracy: **97.3%** (146/150)
Run MV accuracy: **100.0%** (15/15)

---

## DOC (3-class, 33 epochs)

### Results — Pipeline A — DOC (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 75.0% | 91.7% |
| ResNet50 | 91.7% | 91.7% |
| EfficientNet-B0 | 91.7% | **100.0%** |
| ConvNeXt-Tiny | 33.3% ❌ | 91.7% |


### Results — Pipeline D — DOC (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 83.3% | 91.7% |
| ResNet50 | **100.0%** | 83.3% |
| EfficientNet-B0 | **100.0%** | 91.7% |
| ConvNeXt-Tiny | 58.3% | 83.3% |


### Results — Pipeline D (SMOTE) — DOC (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 83.3% | 91.7% |
| ResNet50 | **100.0%** | 83.3% |
| EfficientNet-B0 | **100.0%** | 91.7% |
| ConvNeXt-Tiny | 58.3% | 83.3% |


### Per-Run Detail — Pipeline A — DOC (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`std_doc_rn18_lr1e3`) — Window: 77.5% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .060 | ✗ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **77.5%** (93/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet18 lr=1e-4** (`std_doc_rn18_lr1e4`) — Window: 84.2% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .015 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **84.2%** (101/120)
Run MV accuracy: **91.7%** (11/12)

**ResNet50 lr=1e-3** (`std_doc_rn50_lr1e3`) — Window: 89.2% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **89.2%** (107/120)
Run MV accuracy: **91.7%** (11/12)

**ResNet50 lr=1e-4** (`std_doc_rn50_lr1e4`) — Window: 90.0% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **90.0%** (108/120)
Run MV accuracy: **91.7%** (11/12)

**EfficientNet-B0 lr=1e-3** (`std_doc_enb0_lr1e3`) — Window: 93.3% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **93.3%** (112/120)
Run MV accuracy: **91.7%** (11/12)

**EfficientNet-B0 lr=1e-4** (`std_doc_enb0_lr1e4`) — Window: 95.0% | Run MV: **100.0%** (12/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **95.0%** (114/120)
Run MV accuracy: **100.0%** (12/12)

**ConvNeXt-Tiny lr=1e-3** (`std_doc_cnxt_lr1e3`) — Window: 33.3% | Run MV: **33.3%** (4/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .030 | ✗ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .030 | ✗ |
| run25 | .060 | .030 | ✗ |
| run29 | .060 | .030 | ✗ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .030 | ✗ |
| run41 | .015 | .030 | ✗ |
| run5 | .015 | .030 | ✗ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **33.3%** (40/120)
Run MV accuracy: **33.3%** (4/12)

**ConvNeXt-Tiny lr=1e-4** (`std_doc_cnxt_lr1e4`) — Window: 88.3% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **88.3%** (106/120)
Run MV accuracy: **91.7%** (11/12)

### Per-Run Detail — Pipeline D — DOC (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`ses4ch_doc_rn18_lr1e3`) — Window: 83.3% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **83.3%** (100/120)
Run MV accuracy: **83.3%** (10/12)

**ResNet18 lr=1e-4** (`ses4ch_doc_rn18_lr1e4`) — Window: 87.5% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **87.5%** (105/120)
Run MV accuracy: **91.7%** (11/12)

**ResNet50 lr=1e-3** (`ses4ch_doc_rn50_lr1e3`) — Window: 92.5% | Run MV: **100.0%** (12/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **92.5%** (111/120)
Run MV accuracy: **100.0%** (12/12)

**ResNet50 lr=1e-4** (`ses4ch_doc_rn50_lr1e4`) — Window: 82.5% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .015 | ✗ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **82.5%** (99/120)
Run MV accuracy: **83.3%** (10/12)

**EfficientNet-B0 lr=1e-3** (`ses4ch_doc_enb0_lr1e3`) — Window: 90.0% | Run MV: **100.0%** (12/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **90.0%** (108/120)
Run MV accuracy: **100.0%** (12/12)

**EfficientNet-B0 lr=1e-4** (`ses4ch_doc_enb0_lr1e4`) — Window: 83.3% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **83.3%** (100/120)
Run MV accuracy: **91.7%** (11/12)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_doc_cnxt_lr1e3`) — Window: 60.0% | Run MV: **58.3%** (7/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .015 | ✗ |
| run16 | .030 | .015 | ✗ |
| run19 | .030 | .015 | ✗ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .015 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .015 | ✗ |

Window accuracy: **60.0%** (72/120)
Run MV accuracy: **58.3%** (7/12)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_doc_cnxt_lr1e4`) — Window: 80.0% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **80.0%** (96/120)
Run MV accuracy: **83.3%** (10/12)

### Per-Run Detail — Pipeline D (SMOTE) — DOC (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`ses4ch_smote_doc_rn18_lr1e3`) — Window: 83.3% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **83.3%** (100/120)
Run MV accuracy: **83.3%** (10/12)

**ResNet18 lr=1e-4** (`ses4ch_smote_doc_rn18_lr1e4`) — Window: 87.5% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **87.5%** (105/120)
Run MV accuracy: **91.7%** (11/12)

**ResNet50 lr=1e-3** (`ses4ch_smote_doc_rn50_lr1e3`) — Window: 92.5% | Run MV: **100.0%** (12/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **92.5%** (111/120)
Run MV accuracy: **100.0%** (12/12)

**ResNet50 lr=1e-4** (`ses4ch_smote_doc_rn50_lr1e4`) — Window: 82.5% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .015 | ✗ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **82.5%** (99/120)
Run MV accuracy: **83.3%** (10/12)

**EfficientNet-B0 lr=1e-3** (`ses4ch_smote_doc_enb0_lr1e3`) — Window: 90.0% | Run MV: **100.0%** (12/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .030 | ✓ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **90.0%** (108/120)
Run MV accuracy: **100.0%** (12/12)

**EfficientNet-B0 lr=1e-4** (`ses4ch_smote_doc_enb0_lr1e4`) — Window: 83.3% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .060 | ✓ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **83.3%** (100/120)
Run MV accuracy: **91.7%** (11/12)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_smote_doc_cnxt_lr1e3`) — Window: 60.0% | Run MV: **58.3%** (7/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .015 | ✗ |
| run16 | .030 | .015 | ✗ |
| run19 | .030 | .015 | ✗ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .015 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .015 | ✗ |

Window accuracy: **60.0%** (72/120)
Run MV accuracy: **58.3%** (7/12)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_smote_doc_cnxt_lr1e4`) — Window: 80.0% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run1 | .015 | .015 | ✓ |
| run14 | .030 | .030 | ✓ |
| run16 | .030 | .060 | ✗ |
| run19 | .030 | .030 | ✓ |
| run22 | .060 | .060 | ✓ |
| run25 | .060 | .060 | ✓ |
| run29 | .060 | .060 | ✓ |
| run36 | .060 | .030 | ✗ |
| run38 | .015 | .015 | ✓ |
| run41 | .015 | .015 | ✓ |
| run5 | .015 | .015 | ✓ |
| run7 | .030 | .030 | ✓ |

Window accuracy: **80.0%** (96/120)
Run MV accuracy: **83.3%** (10/12)

---

## Roughness Ra (3-class, 33 epochs)

### Results — Pipeline A — Roughness Ra (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 91.7% | 83.3% |
| ResNet50 | 83.3% | 91.7% |
| EfficientNet-B0 | 91.7% | 91.7% |
| ConvNeXt-Tiny | 33.3% ❌ | 91.7% |


### Results — Pipeline D — Roughness Ra (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 75.0% | 66.7% |
| ResNet50 | 66.7% | 75.0% |
| EfficientNet-B0 | 75.0% | 75.0% |
| ConvNeXt-Tiny | 33.3% ❌ | 66.7% |


### Results — Pipeline D (SMOTE) — Roughness Ra (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 75.0% | 66.7% |
| ResNet50 | 66.7% | 75.0% |
| EfficientNet-B0 | 66.7% | 66.7% |
| ConvNeXt-Tiny | 41.7% ❌ | 66.7% |


### Per-Run Detail — Pipeline A — Roughness Ra (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`std_roughness_rn18_lr1e3`) — Window: 91.7% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Rgh | ✓ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **91.7%** (110/120)
Run MV accuracy: **91.7%** (11/12)

**ResNet18 lr=1e-4** (`std_roughness_rn18_lr1e4`) — Window: 87.5% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Smt | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **87.5%** (105/120)
Run MV accuracy: **83.3%** (10/12)

**ResNet50 lr=1e-3** (`std_roughness_rn50_lr1e3`) — Window: 83.3% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **83.3%** (100/120)
Run MV accuracy: **83.3%** (10/12)

**ResNet50 lr=1e-4** (`std_roughness_rn50_lr1e4`) — Window: 86.7% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Med | ✓ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **86.7%** (104/120)
Run MV accuracy: **91.7%** (11/12)

**EfficientNet-B0 lr=1e-3** (`std_roughness_enb0_lr1e3`) — Window: 91.7% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Med | ✓ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **91.7%** (110/120)
Run MV accuracy: **91.7%** (11/12)

**EfficientNet-B0 lr=1e-4** (`std_roughness_enb0_lr1e4`) — Window: 88.3% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Med | ✓ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **88.3%** (106/120)
Run MV accuracy: **91.7%** (11/12)

**ConvNeXt-Tiny lr=1e-3** (`std_roughness_cnxt_lr1e3`) — Window: 33.3% | Run MV: **33.3%** (4/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Med | ✓ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Med | ✗ |
| run32 | Rgh | Med | ✗ |
| run34 | Rgh | Med | ✗ |
| run38 | Smt | Med | ✗ |
| run40 | Smt | Med | ✗ |
| run43 | Smt | Med | ✗ |
| run5 | Smt | Med | ✗ |
| run7 | Med | Med | ✓ |

Window accuracy: **33.3%** (40/120)
Run MV accuracy: **33.3%** (4/12)

**ConvNeXt-Tiny lr=1e-4** (`std_roughness_cnxt_lr1e4`) — Window: 88.3% | Run MV: **91.7%** (11/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Med | ✓ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **88.3%** (106/120)
Run MV accuracy: **91.7%** (11/12)

### Per-Run Detail — Pipeline D — Roughness Ra (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`ses4ch_roughness_rn18_lr1e3`) — Window: 75.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Med | ✓ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **75.0%** (90/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet18 lr=1e-4** (`ses4ch_roughness_rn18_lr1e4`) — Window: 68.3% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Smt | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **68.3%** (82/120)
Run MV accuracy: **66.7%** (8/12)

**ResNet50 lr=1e-3** (`ses4ch_roughness_rn50_lr1e3`) — Window: 69.2% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Smt | ✗ |
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **69.2%** (83/120)
Run MV accuracy: **66.7%** (8/12)

**ResNet50 lr=1e-4** (`ses4ch_roughness_rn50_lr1e4`) — Window: 75.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **75.0%** (90/120)
Run MV accuracy: **75.0%** (9/12)

**EfficientNet-B0 lr=1e-3** (`ses4ch_roughness_enb0_lr1e3`) — Window: 72.5% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **72.5%** (87/120)
Run MV accuracy: **75.0%** (9/12)

**EfficientNet-B0 lr=1e-4** (`ses4ch_roughness_enb0_lr1e4`) — Window: 65.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **65.0%** (78/120)
Run MV accuracy: **75.0%** (9/12)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_roughness_cnxt_lr1e3`) — Window: 33.3% | Run MV: **33.3%** (4/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Smt | ✗ |
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Smt | ✗ |
| run28 | Rgh | Smt | ✗ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Smt | ✗ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Smt | ✗ |

Window accuracy: **33.3%** (40/120)
Run MV accuracy: **33.3%** (4/12)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_roughness_cnxt_lr1e4`) — Window: 65.8% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Smt | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **65.8%** (79/120)
Run MV accuracy: **66.7%** (8/12)

### Per-Run Detail — Pipeline D (SMOTE) — Roughness Ra (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`ses4ch_smote_roughness_rn18_lr1e3`) — Window: 73.3% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **73.3%** (88/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet18 lr=1e-4** (`ses4ch_smote_roughness_rn18_lr1e4`) — Window: 69.2% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **69.2%** (83/120)
Run MV accuracy: **66.7%** (8/12)

**ResNet50 lr=1e-3** (`ses4ch_smote_roughness_rn50_lr1e3`) — Window: 66.7% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Smt | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **66.7%** (80/120)
Run MV accuracy: **66.7%** (8/12)

**ResNet50 lr=1e-4** (`ses4ch_smote_roughness_rn50_lr1e4`) — Window: 75.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **75.0%** (90/120)
Run MV accuracy: **75.0%** (9/12)

**EfficientNet-B0 lr=1e-3** (`ses4ch_smote_roughness_enb0_lr1e3`) — Window: 69.2% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Smt | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **69.2%** (83/120)
Run MV accuracy: **66.7%** (8/12)

**EfficientNet-B0 lr=1e-4** (`ses4ch_smote_roughness_enb0_lr1e4`) — Window: 65.8% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **65.8%** (79/120)
Run MV accuracy: **66.7%** (8/12)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_smote_roughness_cnxt_lr1e3`) — Window: 52.5% | Run MV: **41.7%** (5/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Smt | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Smt | ✗ |
| run32 | Rgh | Rgh | ✓ |
| run34 | Rgh | Smt | ✗ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Rgh | ✗ |
| run5 | Smt | Med | ✗ |
| run7 | Med | Med | ✓ |

Window accuracy: **52.5%** (63/120)
Run MV accuracy: **41.7%** (5/12)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_smote_roughness_cnxt_lr1e4`) — Window: 68.3% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run11 | Med | Smt | ✗ |
| run19 | Med | Rgh | ✗ |
| run22 | Rgh | Med | ✗ |
| run27 | Med | Med | ✓ |
| run28 | Rgh | Rgh | ✓ |
| run32 | Rgh | Smt | ✗ |
| run34 | Rgh | Rgh | ✓ |
| run38 | Smt | Smt | ✓ |
| run40 | Smt | Smt | ✓ |
| run43 | Smt | Smt | ✓ |
| run5 | Smt | Smt | ✓ |
| run7 | Med | Med | ✓ |

Window accuracy: **68.3%** (82/120)
Run MV accuracy: **66.7%** (8/12)

---

## Feed Rate Coarse (3-class, 33 epochs)

### Results — Pipeline A — Feed Rate Coarse (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 75.0% | 75.0% |
| ResNet50 | 83.3% | 75.0% |
| EfficientNet-B0 | 75.0% | 75.0% |
| ConvNeXt-Tiny | 75.0% | 83.3% |


### Results — Pipeline D — Feed Rate Coarse (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 66.7% | 75.0% |
| ResNet50 | 75.0% | 75.0% |
| EfficientNet-B0 | 58.3% | 75.0% |
| ConvNeXt-Tiny | 33.3% ❌ | 66.7% |


### Results — Pipeline D (SMOTE) — Feed Rate Coarse (3-class, 33 epochs) — eval on test set

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 58.3% | 58.3% |
| ResNet50 | 75.0% | 58.3% |
| EfficientNet-B0 | 66.7% | 75.0% |
| ConvNeXt-Tiny | 66.7% | 66.7% |


### Per-Run Detail — Pipeline A — Feed Rate Coarse (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`std_feed_coarse_rn18_lr1e3`) — Window: 75.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **75.0%** (90/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet18 lr=1e-4** (`std_feed_coarse_rn18_lr1e4`) — Window: 75.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **75.0%** (90/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet50 lr=1e-3** (`std_feed_coarse_rn50_lr1e3`) — Window: 77.5% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Med | ✓ |

Window accuracy: **77.5%** (93/120)
Run MV accuracy: **83.3%** (10/12)

**ResNet50 lr=1e-4** (`std_feed_coarse_rn50_lr1e4`) — Window: 70.8% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Hi | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Med | ✓ |

Window accuracy: **70.8%** (85/120)
Run MV accuracy: **75.0%** (9/12)

**EfficientNet-B0 lr=1e-3** (`std_feed_coarse_enb0_lr1e3`) — Window: 74.2% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **74.2%** (89/120)
Run MV accuracy: **75.0%** (9/12)

**EfficientNet-B0 lr=1e-4** (`std_feed_coarse_enb0_lr1e4`) — Window: 75.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **75.0%** (90/120)
Run MV accuracy: **75.0%** (9/12)

**ConvNeXt-Tiny lr=1e-3** (`std_feed_coarse_cnxt_lr1e3`) — Window: 75.8% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Low | ✓ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Low | ✗ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **75.8%** (91/120)
Run MV accuracy: **75.0%** (9/12)

**ConvNeXt-Tiny lr=1e-4** (`std_feed_coarse_cnxt_lr1e4`) — Window: 81.7% | Run MV: **83.3%** (10/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Med | ✓ |

Window accuracy: **81.7%** (98/120)
Run MV accuracy: **83.3%** (10/12)

### Per-Run Detail — Pipeline D — Feed Rate Coarse (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`ses4ch_feed_coarse_rn18_lr1e3`) — Window: 66.7% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Hi | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **66.7%** (80/120)
Run MV accuracy: **66.7%** (8/12)

**ResNet18 lr=1e-4** (`ses4ch_feed_coarse_rn18_lr1e4`) — Window: 62.5% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Med | ✓ |

Window accuracy: **62.5%** (75/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet50 lr=1e-3** (`ses4ch_feed_coarse_rn50_lr1e3`) — Window: 70.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Hi | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Hi | ✓ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **70.0%** (84/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet50 lr=1e-4** (`ses4ch_feed_coarse_rn50_lr1e4`) — Window: 66.7% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Low | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Hi | ✓ |
| run7 | Low | Low | ✓ |
| run9 | Med | Med | ✓ |

Window accuracy: **66.7%** (80/120)
Run MV accuracy: **75.0%** (9/12)

**EfficientNet-B0 lr=1e-3** (`ses4ch_feed_coarse_enb0_lr1e3`) — Window: 62.5% | Run MV: **58.3%** (7/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Med | ✗ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Med | ✗ |
| run9 | Med | Med | ✓ |

Window accuracy: **62.5%** (75/120)
Run MV accuracy: **58.3%** (7/12)

**EfficientNet-B0 lr=1e-4** (`ses4ch_feed_coarse_enb0_lr1e4`) — Window: 70.8% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **70.8%** (85/120)
Run MV accuracy: **75.0%** (9/12)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_feed_coarse_cnxt_lr1e3`) — Window: 33.3% | Run MV: **33.3%** (4/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Hi | ✗ |
| run17 | Med | Hi | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Hi | ✗ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Hi | ✗ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Hi | ✗ |
| run45 | Med | Hi | ✗ |
| run5 | Hi | Hi | ✓ |
| run7 | Low | Hi | ✗ |
| run9 | Med | Hi | ✗ |

Window accuracy: **33.3%** (40/120)
Run MV accuracy: **33.3%** (4/12)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_feed_coarse_cnxt_lr1e4`) — Window: 60.0% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Med | ✗ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Med | ✓ |

Window accuracy: **60.0%** (72/120)
Run MV accuracy: **66.7%** (8/12)

### Per-Run Detail — Pipeline D (SMOTE) — Feed Rate Coarse (3-class, 33 epochs)

**ResNet18 lr=1e-3** (`ses4ch_smote_feed_coarse_rn18_lr1e3`) — Window: 61.7% | Run MV: **58.3%** (7/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Hi | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **61.7%** (74/120)
Run MV accuracy: **58.3%** (7/12)

**ResNet18 lr=1e-4** (`ses4ch_smote_feed_coarse_rn18_lr1e4`) — Window: 60.8% | Run MV: **58.3%** (7/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Med | ✗ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **60.8%** (73/120)
Run MV accuracy: **58.3%** (7/12)

**ResNet50 lr=1e-3** (`ses4ch_smote_feed_coarse_rn50_lr1e3`) — Window: 70.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Low | ✓ |
| run17 | Med | Hi | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Hi | ✗ |
| run5 | Hi | Hi | ✓ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **70.0%** (84/120)
Run MV accuracy: **75.0%** (9/12)

**ResNet50 lr=1e-4** (`ses4ch_smote_feed_coarse_rn50_lr1e4`) — Window: 58.3% | Run MV: **58.3%** (7/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Low | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **58.3%** (70/120)
Run MV accuracy: **58.3%** (7/12)

**EfficientNet-B0 lr=1e-3** (`ses4ch_smote_feed_coarse_enb0_lr1e3`) — Window: 60.8% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Hi | ✗ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **60.8%** (73/120)
Run MV accuracy: **66.7%** (8/12)

**EfficientNet-B0 lr=1e-4** (`ses4ch_smote_feed_coarse_enb0_lr1e4`) — Window: 65.0% | Run MV: **75.0%** (9/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Hi | ✓ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **65.0%** (78/120)
Run MV accuracy: **75.0%** (9/12)

**ConvNeXt-Tiny lr=1e-3** (`ses4ch_smote_feed_coarse_cnxt_lr1e3`) — Window: 62.5% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Low | ✓ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Low | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Low | ✗ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **62.5%** (75/120)
Run MV accuracy: **66.7%** (8/12)

**ConvNeXt-Tiny lr=1e-4** (`ses4ch_smote_feed_coarse_cnxt_lr1e4`) — Window: 60.0% | Run MV: **66.7%** (8/12)

| Run | True | MV | Result |
|-----|------|-----|--------|
| run13 | Low | Med | ✗ |
| run17 | Med | Med | ✓ |
| run21 | Hi | Hi | ✓ |
| run25 | Low | Low | ✓ |
| run3 | Hi | Med | ✗ |
| run31 | Med | Med | ✓ |
| run36 | Hi | Hi | ✓ |
| run37 | Low | Low | ✓ |
| run45 | Med | Med | ✓ |
| run5 | Hi | Med | ✗ |
| run7 | Low | Low | ✓ |
| run9 | Med | Low | ✗ |

Window accuracy: **60.0%** (72/120)
Run MV accuracy: **66.7%** (8/12)
