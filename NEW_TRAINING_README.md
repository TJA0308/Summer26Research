# ResNet18 & ConvNeXt-Tiny: Standard CWT vs SES 4-Channel — Results

**Backbones:** ResNet18, ConvNeXt-Tiny (both ImageNet pretrained)  
**Optimizer:** AdamW, weight_decay=1e-4, cosine LR scheduler  
**Learning rates tested:** lr=1e-3 and lr=1e-4 for both backbones and both pipelines  
**SMOTE:** applied to balance training classes to 8 runs/class for all targets  
**Weighted loss:** feed_coarse only (class imbalance: low=13, med=19, high=7 training runs)  
**Epochs:** speed=30, doc=31, roughness=31, feed_coarse=33

---

## Training Commands

### Pipeline A — Standard CWT (`scalograms_10w`, `cnn_train.py`)

SMOTE CSVs are auto-loaded from the scalogram directory — no flag needed.  
`--augment light` enables random horizontal flip.

#### ResNet18

```powershell
# lr=1e-3
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone resnet18      --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_rn18_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone resnet18      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_rn18_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone resnet18      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_rn18_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet18      --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_rn18_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone resnet18      --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_rn18_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone resnet18      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_rn18_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone resnet18      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_rn18_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet18      --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_rn18_lr1e4.pt
```

#### ResNet50

```powershell
# lr=1e-3
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone resnet50      --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_rn50_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone resnet50      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_rn50_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone resnet50      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_rn50_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet50      --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_rn50_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone resnet50      --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_rn50_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone resnet50      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_rn50_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone resnet50      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_rn50_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet50      --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_rn50_lr1e4.pt
```

#### EfficientNet-B0

```powershell
# lr=1e-3
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_enb0_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone efficientnet_b0 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_enb0_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone efficientnet_b0 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_enb0_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_enb0_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_enb0_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone efficientnet_b0 --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_enb0_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone efficientnet_b0 --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_enb0_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_enb0_lr1e4.pt
```

#### ConvNeXt-Tiny

```powershell
# lr=1e-3
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone convnext_tiny --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_cnxt_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_cnxt_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_cnxt_lr1e3.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_cnxt_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed       --backbone convnext_tiny --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_speed_cnxt_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc         --backbone convnext_tiny --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_doc_cnxt_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness   --backbone convnext_tiny --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --save std_roughness_cnxt_lr1e4.pt
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --augment light --weighted_loss --save std_feed_cnxt_lr1e4.pt
```

---

### Pipeline B — SES 4-Channel (`scalograms_ses_10w`, `cnn_train_hilbert.py`)

`--smote` is required to load the SES SMOTE CSVs. No augmentation.

#### ResNet18

```powershell
# lr=1e-3
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone resnet18      --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_rn18_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone resnet18      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_rn18_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone resnet18      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_rn18_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet18      --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_rn18_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone resnet18      --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_rn18_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone resnet18      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_rn18_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone resnet18      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_rn18_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet18      --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_rn18_lr1e4.pt
```

#### ResNet50

```powershell
# lr=1e-3
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone resnet50      --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_rn50_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone resnet50      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_rn50_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone resnet50      --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_rn50_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet50      --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_rn50_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone resnet50      --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_rn50_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone resnet50      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_rn50_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone resnet50      --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_rn50_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet50      --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_rn50_lr1e4.pt
```

#### EfficientNet-B0

```powershell
# lr=1e-3
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_enb0_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone efficientnet_b0 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_enb0_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone efficientnet_b0 --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_enb0_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_enb0_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_enb0_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone efficientnet_b0 --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_enb0_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone efficientnet_b0 --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_enb0_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_enb0_lr1e4.pt
```

#### ConvNeXt-Tiny

```powershell
# lr=1e-3
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone convnext_tiny --epochs 30 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_cnxt_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_cnxt_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone convnext_tiny --epochs 31 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_cnxt_lr1e3.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_cnxt_lr1e3.pt

# lr=1e-4
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed       --backbone convnext_tiny --epochs 30 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_speed_cnxt_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc         --backbone convnext_tiny --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_doc_cnxt_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness   --backbone convnext_tiny --epochs 31 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --save ses_roughness_cnxt_lr1e4.pt
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-4 --weight_decay 1e-4 --optimizer adamw --scheduler cosine --smote --weighted_loss --save ses_feed_cnxt_lr1e4.pt
```

---

---

## Pipelines

### Pipeline A — Standard CWT (`scalograms_10w`, `cnn_train.py`)
- Input: 3-channel RGB PNG, 224×224
- Signal: CWT of raw ai4 accelerometer
- Augmentation: random horizontal flip (light)
- SMOTE CSVs auto-loaded from scalogram directory

### Pipeline B — SES 4-Channel (`scalograms_ses_10w`, `cnn_train_hilbert.py`)
- Input: 4-channel float32 .npy, shape (4, H, W)
  - ch 0: ai4 raw CWT
  - ch 1: ai6 raw CWT
  - ch 2: SES(ai4) = |Hilbert{ai4}|² CWT
  - ch 3: SES(ai6) = |Hilbert{ai6}|² CWT
- Augmentation: none (horizontal flip is physically invalid for CWT time-axis)
- 4th conv channel seeded from average of pretrained 3-channel weights
- SMOTE loaded via `--smote` flag

---

## Speed (5-class: 1500 / 2000 / 3000 / 4000 / 5000 rpm) | 30 epochs

### Training Data

| Pipeline | Real Runs | Runs/Class | SMOTE Added | Effective/Class |
|----------|-----------|-----------|-------------|----------------|
| A (Std CWT) | 35 | 7/class | +1/class (smote_s{c}_0) | 8 |
| B (SES 4-ch) | 30 | 6/class | +2/class (smote_hs{c}_0,1) | 8 |

10 windows per run → 400 training scalograms per pipeline.

### Test Data

Pipeline A: 10 test runs (2/class), 100 windows. Pipeline B: 15 test runs (3/class, one per DOC level), 150 windows.

| Class | Label | Pipeline A Test Runs | Pipeline B Test Runs |
|-------|-------|---------------------|---------------------|
| 0 | 1500 rpm | run9 (DOC=0.030), run22 (DOC=0.060) | run9 (DOC=0.030), run22 (DOC=0.060), run37 (DOC=0.015) |
| 1 | 2000 rpm | run12 (DOC=0.030), run27 (DOC=0.060) | run12 (DOC=0.030), run27 (DOC=0.060), run40 (DOC=0.015) |
| 2 | 3000 rpm | run15 (DOC=0.030), run28 (DOC=0.060) | run15 (DOC=0.030), run28 (DOC=0.060), run43 (DOC=0.015) |
| 3 | 4000 rpm | run2 (DOC=0.015), run16 (DOC=0.030) | run2 (DOC=0.015), run16 (DOC=0.030), run31 (DOC=0.060) |
| 4 | 5000 rpm | run5 (DOC=0.015), run36 (DOC=0.060) | run5 (DOC=0.015), run19 (DOC=0.030), run36 (DOC=0.060) |

### Results

#### Pipeline A — Standard CWT

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 84.0% | 79.0% |
| ResNet50 | **97.0%** | 90.0% |
| EfficientNet-B0 | 85.0% | 85.0% |
| ConvNeXt-Tiny | 20.0% ❌ | 91.0% |

```
RN18  lr=1e-3  █████████████████████░░░░  84.0%
RN18  lr=1e-4  ████████████████████░░░░░  79.0%
RN50  lr=1e-3  ████████████████████████░  97.0% ✓
RN50  lr=1e-4  ██████████████████████░░░  90.0%
ENB0  lr=1e-3  █████████████████████░░░░  85.0%
ENB0  lr=1e-4  █████████████████████░░░░  85.0%
CNXT  lr=1e-3  █████░░░░░░░░░░░░░░░░░░░░  20.0% ❌
CNXT  lr=1e-4  ███████████████████████░░  91.0%
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline A — Per-Window Predictions

**speed_resnet_10w (RN18)** — Window: 90.0% | Run MV: **100.0%** (10/10)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run9 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run22 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 3000 | 3000 | 3000 | 3000 | 1500 | ✓ |
| run12 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run27 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 1500 | 2000 | ✓ |
| run15 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run28 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 1500 | 1500 | 1500 | 1500 | 3000 | ✓ |
| run2 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | ✓ |
| run16 | 4000 | 2000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | ✓ |
| run5 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |
| run36 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |

**speed_cnxt_10w (ConvNeXt-Tiny)** — Window: 96.0% | Run MV: **100.0%** (10/10)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run9 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run22 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run12 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run27 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run28 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run2 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | ✓ |
| run16 | 4000 | 2000 | 4000 | 2000 | 4000 | 2000 | 4000 | 4000 | 4000 | 4000 | 2000 | 4000 | ✓ |
| run5 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |
| run36 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |

#### Pipeline B — SES 4-Channel

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | **93.3%** | 89.3% |
| ResNet50 | **93.3%** | 81.3% |
| EfficientNet-B0 | 86.7% | 77.3% |
| ConvNeXt-Tiny | 90.7% | 80.0% |

```
RN18  lr=1e-3  ███████████████████████░░  93.3% ✓
RN18  lr=1e-4  ██████████████████████░░░  89.3%
RN50  lr=1e-3  ███████████████████████░░  93.3% ✓
RN50  lr=1e-4  ████████████████████░░░░░  81.3%
ENB0  lr=1e-3  ██████████████████████░░░  86.7%
ENB0  lr=1e-4  ███████████████████░░░░░░  77.3%
CNXT  lr=1e-3  ███████████████████████░░  90.7%
CNXT  lr=1e-4  ████████████████████░░░░░  80.0%
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline B — Per-Window Predictions

**ses_speed_rn18 (RN18)** — Window: 90.7% | Run MV: **93.3%** (14/15)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run9 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run22 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run37 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run12 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run27 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run40 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run15 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run28 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run43 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run2 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | ✓ |
| run16 | 4000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✗ |
| run31 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | ✓ |
| run5 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |
| run19 | 5000 | 1500 | 1500 | 1500 | 1500 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |
| run36 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |

**ses_speed_cnxt (ConvNeXt-Tiny)** — Window: 83.3% | Run MV: **86.7%** (13/15)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run9 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run22 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run37 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | 1500 | ✓ |
| run12 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run27 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run40 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✓ |
| run15 | 3000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✗ |
| run28 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run43 | 3000 | 3000 | 1500 | 3000 | 1500 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | ✓ |
| run2 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | ✓ |
| run16 | 4000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | 2000 | ✗ |
| run31 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | 4000 | ✓ |
| run5 | 5000 | 1500 | 1500 | 1500 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |
| run19 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |
| run36 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | 5000 | ✓ |

---

## DOC / Depth of Cut (3-class: 0.015 / 0.030 / 0.060 mm) | 31 epochs

### Training Data

| Pipeline | Real Runs | Class Distribution | SMOTE Added | Effective/Class |
|----------|-----------|------------------|-------------|----------------|
| A (Std CWT) | 36 | 12/12/12 (balanced) | none | 12 |
| B (SES 4-ch) | 31 | 10/10/11 (near-balanced) | +1 for classes 0,1 | 11 |

10 windows per run → 360 / 310 training scalograms (A / B).

### Test Data

Pipeline A: 9 test runs (3/class), 90 windows. Pipeline B: 14 test runs (4-5/class, all RPM speeds represented per DOC level), 140 windows.

| Class | Label | Pipeline A Test Runs | Pipeline B Test Runs |
|-------|-------|---------------------|---------------------|
| 0 | 0.015 mm | run1 (4000rpm), run5 (5000rpm), run43 (3000rpm) | run1 (4000rpm), run5 (5000rpm), run38 (1500rpm), run41 (2000rpm), run43 (3000rpm) |
| 1 | 0.030 mm | run7 (1500rpm), run14 (3000rpm), run19 (5000rpm) | run7 (1500rpm), run11 (2000rpm), run14 (3000rpm), run16 (4000rpm), run19 (5000rpm) |
| 2 | 0.060 mm | run22 (1500rpm), run29 (3000rpm), run36 (5000rpm) | run22 (1500rpm), run25 (2000rpm), run29 (3000rpm), run36 (5000rpm) |

### Results

#### Pipeline A — Standard CWT

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 88.9% | 93.3% |
| ResNet50 | 97.8% | 86.7% |
| EfficientNet-B0 | 97.8% | **98.9%** |
| ConvNeXt-Tiny | 33.3% ❌ | 92.2% |

```
RN18  lr=1e-3  ██████████████████████░░░  88.9%
RN18  lr=1e-4  ███████████████████████░░  93.3%
RN50  lr=1e-3  ████████████████████████░  97.8%
RN50  lr=1e-4  ██████████████████████░░░  86.7%
ENB0  lr=1e-3  ████████████████████████░  97.8%
ENB0  lr=1e-4  █████████████████████████  98.9% ✓
CNXT  lr=1e-3  ████████░░░░░░░░░░░░░░░░░  33.3% ❌
CNXT  lr=1e-4  ███████████████████████░░  92.2%
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline A — Per-Window Predictions

**best_model_doc_resnet18 (RN18)** — Window: 82.2% | Run MV: **88.9%** (8/9)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run1 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run5 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run43 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run7 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run14 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run19 | .030 | .015 | .030 | .015 | .030 | .015 | .030 | .015 | .030 | .030 | .030 | .030 | ✓ |
| run22 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .015 | .060 | ✓ |
| run29 | .060 | .060 | .060 | .060 | .015 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |
| run36 | .060 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✗ |

**best_model_doc_convnext (ConvNeXt-Tiny)** — Window: 77.8% | Run MV: **77.8%** (7/9)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run1 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run5 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run43 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run7 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run14 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run19 | .030 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✗ |
| run22 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |
| run29 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |
| run36 | .060 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✗ |

#### Pipeline B — SES 4-Channel

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | **92.1%** | 78.6% |
| ResNet50 | 75.0% | 72.9% |
| EfficientNet-B0 | 91.4% | 76.4% |
| ConvNeXt-Tiny | 35.7% ❌ | 78.6% |

```
RN18  lr=1e-3  ███████████████████████░░  92.1% ✓
RN18  lr=1e-4  ████████████████████░░░░░  78.6%
RN50  lr=1e-3  ███████████████████░░░░░░  75.0%
RN50  lr=1e-4  ██████████████████░░░░░░░  72.9%
ENB0  lr=1e-3  ███████████████████████░░  91.4%
ENB0  lr=1e-4  ███████████████████░░░░░░  76.4%
CNXT  lr=1e-3  █████████░░░░░░░░░░░░░░░░  35.7% ❌
CNXT  lr=1e-4  ████████████████████░░░░░  78.6%
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline B — Per-Window Predictions

**ses_doc_rn18 (RN18)** — Window: 83.6% | Run MV: **85.7%** (12/14)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run1 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run5 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run38 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run41 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run43 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✓ |
| run7 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run11 | .030 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | .015 | ✗ |
| run14 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run16 | .030 | .060 | .060 | .060 | .060 | .060 | .060 | .030 | .060 | .030 | .060 | .060 | ✗ |
| run19 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run22 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .030 | .030 | .030 | .015 | .060 | ✓ |
| run25 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |
| run29 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |
| run36 | .060 | .060 | .060 | .030 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |

**ses_doc_cnxt (ConvNeXt-Tiny)** — Window: 54.3% | Run MV: **57.1%** (8/14)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run1 | .015 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✗ |
| run5 | .015 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✗ |
| run38 | .015 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✗ |
| run41 | .015 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✗ |
| run43 | .015 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✗ |
| run7 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run11 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run14 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run16 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run19 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✓ |
| run22 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .030 | .030 | .030 | .030 | .060 | ✓ |
| run25 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |
| run29 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | .060 | ✓ |
| run36 | .060 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | .030 | ✗ |

---

## Roughness (3-class: Smooth Ra<0.7 / Medium 0.7-1.0 / Rough Ra>1.0 μm) | 31 epochs

### Training Data

| Pipeline | Real Runs | Class Distribution | SMOTE Added | Notes |
|----------|-----------|------------------|-------------|-------|
| A (Std CWT) | 39 | ~21 smooth / 9 med / 9 rough | yes (balances to majority) | heavily imbalanced |
| B (SES 4-ch) | 39 | same splits | yes | same labels, different features |

10 windows per run → 390 real training scalograms per pipeline.

### Test Data

Both pipelines share the same 6 test runs (2/class), 60 windows total.

| Class | Label | Test Runs | Conditions |
|-------|-------|-----------|-----------|
| 0 | Smooth (Ra < 0.7 μm) | run5 (Ra=0.424), run43 (Ra=0.364) | 5000rpm DOC=0.015; 3000rpm DOC=0.015 |
| 1 | Medium (Ra 0.7–1.0 μm) | run7 (Ra=0.930), run27 (Ra=0.868) | 1500rpm DOC=0.030; 2000rpm DOC=0.060 |
| 2 | Rough (Ra > 1.0 μm) | run22 (Ra=1.186), run34 (Ra=2.084) | 1500rpm DOC=0.060; 5000rpm DOC=0.060 |

### Results

#### Pipeline A — Standard CWT

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 83.3% | 83.3% |
| ResNet50 | **88.3%** | 80.0% |
| EfficientNet-B0 | 83.3% | 83.3% |
| ConvNeXt-Tiny | 63.3% | 83.3% |

```
RN18  lr=1e-3  █████████████████████░░░░  83.3%
RN18  lr=1e-4  █████████████████████░░░░  83.3%
RN50  lr=1e-3  ██████████████████████░░░  88.3% ✓
RN50  lr=1e-4  ████████████████████░░░░░  80.0%
ENB0  lr=1e-3  █████████████████████░░░░  83.3%
ENB0  lr=1e-4  █████████████████████░░░░  83.3%
CNXT  lr=1e-3  ████████████████░░░░░░░░░  63.3%
CNXT  lr=1e-4  █████████████████████░░░░  83.3%
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline A — Per-Window Predictions

**roughness_resnet_10w (RN18)** — Window: 93.3% | Run MV: **100.0%** (6/6)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✓ |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✓ |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run27 | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | ✓ |
| run34 | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | ✓ |

#### Pipeline B — SES 4-Channel

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 83.3% | 81.7% |
| ResNet50 | 83.3% | 83.3% |
| EfficientNet-B0 | 83.3% | 83.3% |
| ConvNeXt-Tiny | 65.0% | **85.0%** |

```
RN18  lr=1e-3  █████████████████████░░░░  83.3%
RN18  lr=1e-4  ████████████████████░░░░░  81.7%
RN50  lr=1e-3  █████████████████████░░░░  83.3%
RN50  lr=1e-4  █████████████████████░░░░  83.3%
ENB0  lr=1e-3  █████████████████████░░░░  83.3%
ENB0  lr=1e-4  █████████████████████░░░░  83.3%
CNXT  lr=1e-3  ████████████████░░░░░░░░░  65.0%
CNXT  lr=1e-4  █████████████████████░░░░  85.0% ✓
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline B — Per-Window Predictions

**ses_roughness_rn18 (RN18)** — Window: 83.3% | Run MV: **83.3%** (5/6)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✓ |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✓ |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | ✓ |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Smt | Med | ✗ |

**ses_roughness_cnxt (ConvNeXt-Tiny)** — Window: 50.0% | Run MV: **50.0%** (3/6)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✓ |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✓ |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✗ |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run34 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | ✗ |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Med | ✗ |

---

## Feed Coarse (3-class: Low 3-4 / Med 5-6 / High 7-8 mm/rev) | 33 epochs

### Training Data

| Pipeline | Real Runs | Class Distribution | SMOTE Added | Notes |
|----------|-----------|------------------|-------------|-------|
| A (Std CWT) | 39 | 13 low / 19 med / 7 high | yes | `--weighted_loss` used |
| B (SES 4-ch) | 39 | same splits | yes | `--weighted_loss` used |

10 windows per run → 390 real training scalograms per pipeline.

### Test Data

Both pipelines share the same 6 test runs (2/class), 60 windows total.

| Class | Label | Test Runs | Conditions |
|-------|-------|-----------|-----------|
| 0 | Low (3–4 mm/rev) | run25 (3 mm/rev), run13 (4 mm/rev) | 2000rpm DOC=0.060; 3000rpm DOC=0.030 |
| 1 | Med (5–6 mm/rev) | run31 (5 mm/rev), run17 (6 mm/rev) | 4000rpm DOC=0.060; 4000rpm DOC=0.030 |
| 2 | High (7–8 mm/rev) | run5 (7 mm/rev), run36 (8 mm/rev) | 5000rpm DOC=0.015; 5000rpm DOC=0.060 |

### Results

#### Pipeline A — Standard CWT

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | **78.3%** | 66.7% |
| ResNet50 | 68.3% | 63.3% |
| EfficientNet-B0 | 66.7% | 61.7% |
| ConvNeXt-Tiny | 33.3% ❌ | 65.0% |

```
RN18  lr=1e-3  ████████████████████░░░░░  78.3% ✓
RN18  lr=1e-4  █████████████████░░░░░░░░  66.7%
RN50  lr=1e-3  █████████████████░░░░░░░░  68.3%
RN50  lr=1e-4  ████████████████░░░░░░░░░  63.3%
ENB0  lr=1e-3  █████████████████░░░░░░░░  66.7%
ENB0  lr=1e-4  ███████████████░░░░░░░░░░  61.7%
CNXT  lr=1e-3  ████████░░░░░░░░░░░░░░░░░  33.3% ❌
CNXT  lr=1e-4  ████████████████░░░░░░░░░  65.0%
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline A — Per-Window Predictions

**feed_coarse_cnxt_10w_adamw (ConvNeXt-Tiny)** — Window: 80.0% | Run MV: **83.3%** (5/6)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | ✓ |
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | ✗ |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run5 | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | ✓ |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | ✓ |

#### Pipeline B — SES 4-Channel

| Backbone | lr=1e-3 | lr=1e-4 |
|---------|:-------:|:-------:|
| ResNet18 | 66.7% | 63.3% |
| ResNet50 | **75.0%** | 65.0% |
| EfficientNet-B0 | 61.7% | 58.3% |
| ConvNeXt-Tiny | 58.3% | 71.7% |

```
RN18  lr=1e-3  █████████████████░░░░░░░░  66.7%
RN18  lr=1e-4  ████████████████░░░░░░░░░  63.3%
RN50  lr=1e-3  ███████████████████░░░░░░  75.0% ✓
RN50  lr=1e-4  ████████████████░░░░░░░░░  65.0%
ENB0  lr=1e-3  ███████████████░░░░░░░░░░  61.7%
ENB0  lr=1e-4  ███████████████░░░░░░░░░░  58.3%
CNXT  lr=1e-3  ███████████████░░░░░░░░░░  58.3%
CNXT  lr=1e-4  ██████████████████░░░░░░░  71.7%
               |         |         |    |
               0%       40%       80%  100%
```

#### Pipeline B — Per-Window Predictions

**ses_feed_coarse_rn18 (RN18)** — Window: 66.7% | Run MV: **66.7%** (4/6)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | ✓ |
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✗ |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | ✓ |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✗ |

**ses_feed_coarse_cnxt (ConvNeXt-Tiny)** — Window: 33.3% | Run MV: **33.3%** (2/6)

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|----|-----|-----|
| run25 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✗ |
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✗ |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✓ |
| run36 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✗ |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | ✗ |

---

## Overall Comparison

### Best Result per Target

| Target | Best Accuracy | Model | Pipeline |
|--------|:------------:|-------|---------|
| Speed | **97.0%** | ResNet50 lr=1e-3 | Std CWT |
| DOC | **98.9%** | EfficientNet-B0 lr=1e-4 | Std CWT |
| Roughness | **88.3%** | ResNet50 lr=1e-3 | Std CWT |
| Feed Coarse | **78.3%** | ResNet18 lr=1e-3 | Std CWT |

```
Speed        ████████████████████████░  97.0%  Std CWT RN50 lr=1e-3
DOC          █████████████████████████  98.9%  Std CWT ENB0 lr=1e-4
Roughness    ██████████████████████░░░  88.3%  Std CWT RN50 lr=1e-3
Feed Coarse  ████████████████████░░░░░  78.3%  Std CWT RN18 lr=1e-3
             |         |         |    |
             0%       40%       80%  100%
```

### Full Results Grid — Pipeline A (Std CWT)

| Backbone | LR | Speed | DOC | Roughness | Feed | Avg |
|---------|:--:|:-----:|:---:|:---------:|:----:|:---:|
| ResNet18 | 1e-3 | 84.0% | 88.9% | 83.3% | **78.3%** | 83.6% |
| ResNet18 | 1e-4 | 79.0% | 93.3% | 83.3% | 66.7% | 80.6% |
| ResNet50 | 1e-3 | **97.0%** | 97.8% | **88.3%** | 68.3% | **87.9%** |
| ResNet50 | 1e-4 | 90.0% | 86.7% | 80.0% | 63.3% | 80.0% |
| EfficientNet-B0 | 1e-3 | 85.0% | 97.8% | 83.3% | 66.7% | 83.2% |
| EfficientNet-B0 | 1e-4 | 85.0% | **98.9%** | 83.3% | 61.7% | 82.2% |
| ConvNeXt-Tiny | 1e-3 | 20.0% ❌ | 33.3% ❌ | 63.3% | 33.3% ❌ | 37.5% ❌ |
| ConvNeXt-Tiny | 1e-4 | 91.0% | 92.2% | 83.3% | 65.0% | 82.9% |

### Full Results Grid — Pipeline B (SES 4-Channel)

| Backbone | LR | Speed | DOC | Roughness | Feed | Avg |
|---------|:--:|:-----:|:---:|:---------:|:----:|:---:|
| ResNet18 | 1e-3 | **93.3%** | **92.1%** | 83.3% | 66.7% | **83.9%** |
| ResNet18 | 1e-4 | 89.3% | 78.6% | 81.7% | 63.3% | 78.2% |
| ResNet50 | 1e-3 | **93.3%** | 75.0% | 83.3% | **75.0%** | 81.7% |
| ResNet50 | 1e-4 | 81.3% | 72.9% | 83.3% | 65.0% | 75.6% |
| EfficientNet-B0 | 1e-3 | 86.7% | 91.4% | 83.3% | 61.7% | 80.8% |
| EfficientNet-B0 | 1e-4 | 77.3% | 76.4% | 83.3% | 58.3% | 73.8% |
| ConvNeXt-Tiny | 1e-3 | 90.7% | 35.7% ❌ | 65.0% | 58.3% | 62.4% |
| ConvNeXt-Tiny | 1e-4 | 80.0% | 78.6% | **85.0%** | 71.7% | 78.8% |

### Key Findings

1. **ResNet50 + Std CWT is the strongest overall configuration** — 87.9% average, peaks at 97.0% speed and 97.8% DOC at lr=1e-3. Deeper capacity helps on the 3-channel RGB pipeline.
2. **EfficientNet-B0 achieves the highest single result** — 98.9% DOC on Std CWT at lr=1e-4. Both RN50 and ENB0 exceed 97% on DOC with Std CWT; the task is nearly solved at this pipeline.
3. **Roughness converges to ~83% for most backbones** — nearly every config on both pipelines hits 83.3%, suggesting a ceiling from the 6-run test set. SES ConvNeXt lr=1e-4 at 85.0% is the only outlier above.
4. **SES pipeline underperforms on DOC** — all SES configs score 35-92% on DOC vs 87-99% for Std CWT. DOC-level differences appear as global energy shifts that the raw CWT captures well; envelope channels don't add signal.
5. **Feed_coarse remains the hardest target** — best 78.3% (Std CWT RN18 lr=1e-3), with most configs in the 60-75% range. The 13/19/7 class imbalance and large intra-class variation limit all backbones.
6. **ConvNeXt + lr=1e-3 collapses on Std CWT** — 20-33% across speed, DOC, feed_coarse. LayerNorm sensitivity to LR; all BatchNorm backbones (RN18, RN50, ENB0) are unaffected at 1e-3.

