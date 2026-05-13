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

---

## Saved Models

All saved to the project root. Run from `cnn_model/` or adjust paths accordingly.

| File | Target | Accuracy | Scalogram directory | Windows |
|------|--------|----------|---------------------|---------|
| `../model_speed.pt` | Speed (5-class) | **100%** | `scalograms_ai4_ai6` | 1 |
| `../model_doc.pt` | DOC (3-class) | **100%** | `scalograms_ai4_ai6` | 1 |
| `../model_feed_coarse.pt` | Feed coarse (3-class) | **66.7%** | `scalograms_ai4_ai6` | 1 |
| `../model_feed.pt` | Feed fine-grained (6-class) | **50%** | `scalograms_ai4_ai6_4w` | 4 |

`model_feed_coarse.pt` classifies feed rate into low (3–4 mm/rev), medium (5–6 mm/rev), and high (7–8 mm/rev). `model_feed.pt` attempts all six individual feed values but is harder to distinguish due to RPM/DOC confounding.

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
