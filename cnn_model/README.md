# CNN + Scalogram Model

## Overview

Converts raw vibration signals into scalogram images using the Continuous Wavelet Transform (CWT), then fine-tunes a pretrained ResNet18 CNN to classify those images.

```
Raw CSV signals → scalogram.py → PNG images → cnn_train.py → .pt model
```

Three prediction targets are supported: spindle speed, depth of cut (DOC), and feed rate.

---

## How It Works

### Step 1 — Scalogram Generation (`scalogram.py`)

Each CSV contains three vibration channels (ai4, ai5, ai6) sampled at 16,393 Hz. The script applies an analytic Morlet CWT to each channel, producing a 2D time-frequency power map. The two primary channels (ai4 = feed-axis vibration, ai6 = acoustic) are mapped to Red and Green; Blue is zeros.

Output: 224×224 PNG images. The X-axis is time, Y-axis is frequency (20–4000 Hz, log-spaced), and pixel brightness encodes instantaneous power.

**Key parameters:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| FS | 16393 Hz | Original sample rate |
| DOWNSAMPLE | 2 | Effective rate = 8196 Hz |
| F_MIN / F_MAX | 20–4000 Hz | Frequency range |
| N_FREQS | 300 | Frequency resolution bins |
| SIGMA | 8.0 | Morlet cycles — higher = sharper frequency, worse time resolution |
| IMG_SIZE | 224 | Output size (matches ResNet default input) |

**Windowing** (`--n_windows N`): splits each run into N overlapping half-signal windows. This multiplies training data without collecting new runs. Windows are evenly spaced so the last window always ends at the signal end.

### Step 2 — Training (`cnn_train.py`)

Fine-tunes a pretrained ResNet18 on the scalogram images. The final fully-connected layer is replaced with a new head matching the number of output classes. Weights of the best validation epoch are saved automatically.

Supported targets:

| Target | Classes | Labels |
|--------|---------|--------|
| `speed` | 5 | 1500 / 2000 / 3000 / 4000 / 5000 rpm |
| `feed` | 6 | 3 / 4 / 5 / 6 / 7 / 8 mm/rev |
| `feed_coarse` | 3 | low (3–4) / medium (5–6) / high (7–8) mm/rev |
| `doc` | 3 | 0.015 / 0.030 / 0.060 mm |
| `roughness` | 3 | Smooth (Ra<0.7) / Medium (0.7–1.0) / Rough (Ra>1.0) |

---

## Train / Test Split

Test runs are fixed before training and never used to update weights.

**Speed** — 5 test runs (1 per RPM class, all from DOC=0.060):
`run24, run27, run30, run33, run36`

**Feed / Feed Coarse** — 6 test runs (1 per fine-grained class, spread across DOC and speed):

| Run | Feed (mm/rev) | Speed | DOC |
|-----|---------------|-------|-----|
| run25 | 3 | 2000 rpm | 0.060 |
| run13 | 4 | 3000 rpm | 0.030 |
| run31 | 5 | 4000 rpm | 0.060 |
| run17 | 6 | 4000 rpm | 0.030 |
| run5  | 7 | 5000 rpm | 0.015 |
| run36 | 8 | 5000 rpm | 0.060 |

**DOC** — 9 test runs (3 per class, spread across speeds):

| Runs | DOC | Speeds |
|------|-----|--------|
| run1, run5, run43 | 0.015 mm | 4000, 5000, 3000 rpm |
| run7, run14, run19 | 0.030 mm | 1500, 3000, 5000 rpm |
| run22, run29, run36 | 0.060 mm | 1500, 3000, 5000 rpm |

**Roughness** — 6 test runs (2 per class):

| Runs | Ra class | Ra values |
|------|----------|-----------|
| run5, run43 | Smooth (Ra<0.7) | 0.424, 0.364 μm |
| run7, run27 | Medium (0.7–1.0) | 0.930, 0.868 μm |
| run22, run34 | Rough (Ra>1.0) | 1.186, 2.084 μm |

Ra labels come from `steel Milling Signal files and Surface Roughness.xlsx`. Class distribution: 23 Smooth / 11 Medium / 11 Rough.

---

## Saved Models

All saved to the project root. Run from `cnn_model/` or adjust paths accordingly.

| File | Target | Accuracy | Scalogram directory | Windows |
|------|--------|----------|---------------------|---------|
| `../model_speed.pt` | Speed (5-class) | **100%** | `scalograms_ai4_ai6` | 1 |
| `../model_doc.pt` | DOC (3-class) | **100%** | `scalograms_ai4_ai6` | 1 |
| `../model_feed_coarse.pt` | Feed coarse (3-class) | **66.7%** | `scalograms_ai4_ai6` | 1 |
| `../model_feed.pt` | Feed fine-grained (6-class) | **50%** | `scalograms_ai4_ai6_4w` | 4 |
| `../model_roughness.pt` | Surface roughness Ra (3-class) | **83.3%** | `scalograms_ai4_ai6` | 1 |

`model_feed_coarse.pt` classifies feed rate into low (3–4 mm/rev), medium (5–6 mm/rev), and high (7–8 mm/rev). `model_feed.pt` attempts all six individual feed values but is harder to distinguish due to RPM/DOC confounding.

---

## Multi-Architecture Experiments (`exp_models/`)

`experiment_runner.py` sweeps backbone architectures and data strategies on 10-window scalograms with SMOTE. Run with:

```bash
python experiment_runner.py --target feed      # feed rate experiments
python experiment_runner.py --target roughness # roughness experiments
python experiment_runner.py --target both      # speed + feed (default)
```

### Feed Rate Results (6-class, AdamW, cosine LR, 20 epochs, batch=16)

| Model | Backbone | Window Acc | Run MV Acc |
|-------|----------|-----------|-----------|
| `feed_rn18_10w_adamw.pt` | ResNet18 | **48.3%** | **50.0%** |
| `feed_cnxt_10w_adamw.pt` | ConvNeXt-Tiny | 43.3% | 50.0% |
| `feed_effb0_10w_adamw.pt` | EfficientNet-B0 | 38.3% | 50.0% |

Classes 4 mm/rev, 6 mm/rev, and 7 mm/rev achieve 0 correct predictions across all three architectures. The extreme classes (3 and 8 mm/rev) are reliably identified. All architectures hit the same 50% run-level ceiling — the failure is in the signal, not the model.

### DOC Results (3-class: 0.015/0.030/0.060 mm, AdamW, cosine LR, 20 epochs, batch=16)

| Model | Backbone | Window Acc | Run MV Acc | Soft Avg |
|-------|----------|-----------|-----------|----------|
| `best_model_doc_resnet18.pt` | ResNet18 | **82.2%** | **88.9%** | **88.9%** |
| `best_model_doc_convnext.pt` | ConvNeXt-Tiny | 77.8% | 77.8% | 77.8% |

ResNet18 (8/9 runs correct) outperforms ConvNeXt-Tiny (7/9) on DOC. Both perfectly separate 0.015 mm. The single ResNet18 failure is run36 (5000 rpm, 0.060 mm → predicted 0.030 mm, p=0.943). ConvNeXt-Tiny additionally fails on run19 (5000 rpm, 0.030 mm), with both failures concentrated at 5000 rpm where the DOC signal is partially masked by high-speed harmonics.

### Feed Coarse Results (3-class: low/med/high, AdamW, cosine LR, 20 epochs, batch=16)

| Model | Backbone | Window Acc | Run MV Acc |
|-------|----------|-----------|-----------|
| `feed_coarse_cnxt_10w_adamw.pt` | ConvNeXt-Tiny | **80.0%** | **83.3%** |
| `feed_coarse_rn18_10w_adamw.pt` | ResNet18 | 66.7% | 66.7% |
| `feed_coarse_effb0_10w_adamw.pt` | EfficientNet-B0 | 66.7% | 66.7% |

ConvNeXt-Tiny is the clear winner on coarse feed classification (83.3% vs 66.7% for both other architectures). It correctly classifies run5 (7 mm/rev, high) that ResNet18 and EfficientNet-B0 both fail on. Its single failure is run13 (4 mm/rev, low) predicted as high with p=0.973 — a wider error than ResNet/EfficientNet which predict medium. Medium class is perfectly separated by all architectures.

### Roughness Results (3-class, AdamW, cosine LR, 20 epochs, batch=16)

| Model | Backbone | Data | Accuracy |
|-------|----------|------|----------|
| `roughness_rn18_10w_adamw.pt` | ResNet18 | `scalograms_10w` + SMOTE | **93.3%** |
| `roughness_effb0_10w_adamw.pt` | EfficientNet-B0 | `scalograms_10w` + SMOTE | 83.3% |

SMOTE balanced Medium and Rough training classes from 9 runs each to 21 (matching Smooth). ResNet18 achieved 93.3% (56/60): 20/20 Smooth, 17/20 Medium, 19/20 Rough.

---

## Commands

All commands should be run from inside `cnn_model/`.

### Generate scalograms

```bash
# 1 window per run — used for speed, doc, and feed_coarse models
python scalogram.py --input_dir ../data --output_dir ../scalograms_ai4_ai6

# 4 windows per run — used for feed fine-grained model
python scalogram.py --input_dir ../data --output_dir ../scalograms_ai4_ai6_4w --n_windows 4
```

### Train models

```bash
# Speed — 100% test accuracy
python cnn_train.py --img_dir ../scalograms_ai4_ai6 --target speed \
    --epochs 30 --augment light --save ../model_speed.pt

# DOC — 100% test accuracy
python cnn_train.py --img_dir ../scalograms_ai4_ai6 --target doc \
    --epochs 30 --augment light --save ../model_doc.pt

# Feed coarse (3-class) — 66.7% test accuracy
python cnn_train.py --img_dir ../scalograms_ai4_ai6 --target feed_coarse \
    --epochs 30 --augment light --save ../model_feed_coarse.pt

# Feed fine-grained (6-class) — 50% test accuracy, needs 4-window scalograms
python cnn_train.py --img_dir ../scalograms_ai4_ai6_4w --target feed \
    --epochs 40 --augment light --save ../model_feed.pt

# Surface roughness Ra (3-class) — 83.3% test accuracy
python cnn_train.py --img_dir ../scalograms_ai4_ai6 --target roughness \
    --epochs 30 --augment light --save ../model_roughness.pt
```

### Optional training flags

| Flag | Default | Effect |
|------|---------|--------|
| `--backbone` | `resnet18` | `resnet18`, `resnet50`, or `efficientnet_b0` |
| `--augment` | `light` | `none`, `light`, or `strong` |
| `--epochs` | `30` | Number of training epochs |
| `--lr` | `0.001` | Learning rate |
| `--freeze` | off | Freeze backbone, train classification head only |
| `--weighted_loss` | off | Weight CE loss inversely by class frequency |
| `--n_windows` | `1` | Windows per run in scalogram generation |

---

## Why Speed and DOC Are Easy, Feed Is Hard

Speed classification works because different RPMs place spindle harmonics at distinct frequency positions in the scalogram — these survive any normalization.

DOC classification works because deeper cuts produce larger-amplitude vibrations, which the model detects from the overall energy pattern.

Feed rate is harder because its effect on the scalogram is subtle relative to the dominant speed harmonics. The feed rate changes chip load per revolution, which modulates vibration at the tooth-pass frequency — but this signal is partially masked by the RPM-dependent frequency structure. All feed models plateau around 50–67% despite increasing data and normalization strategies.
