# CNN + Scalogram Model

## Overview

This approach converts raw vibration signals into scalogram images using the Continuous Wavelet Transform (CWT), then trains a pretrained ResNet/EfficientNet CNN to classify those images.

The three scripts work in sequence:

```
Raw CSV signals → scalogram.py → PNG images → cnn_train.py → .pt model → predict.py → prediction
```

---

## How It Works

### Step 1: Scalogram Generation (`scalogram.py`)

Each raw CSV file contains three channels of vibration data (ai4, ai5, ai6) sampled at 16,393 Hz. The script applies a Morlet Continuous Wavelet Transform to each channel, producing a 2D time-frequency power map. The three channel maps are stacked as RGB channels into a single 224×224 PNG image.

Each run is split into 2 overlapping windows, producing 2 images per run (90 images total across 45 runs).

### Step 2: Training (`cnn_train.py`)

A pretrained ResNet18 (or ResNet50 / EfficientNet-B0) backbone is fine-tuned on the scalogram images. The final classification layer is replaced to match the number of output classes for the chosen target.

Supported targets:

| Target | Classes | Labels |
|--------|---------|--------|
| `speed` | 5 | 1500 / 2000 / 3000 / 4000 / 5000 rpm |
| `feed`  | 6 | 3 / 4 / 5 / 6 / 7 / 8 mm/rev |
| `doc`   | 3 | 0.015 / 0.030 / 0.060 mm |

The test set is held out before training and never used to update weights. Best model weights are saved automatically.

### Step 3: Inference (`predict.py`)

Loads a trained `.pt` model and predicts the class of a new raw CSV file. It generates the scalogram on the fly and averages predictions across 2 windows.

---

## Commands

All commands should be run from inside this folder (`cnn_model/`).

**Generate scalograms** (run once before training):
```bash
python scalogram.py --data_dir ../data --out_dir ../scalograms
```

**Train each model:**
```bash
python cnn_train.py --img_dir ../scalograms --target speed
python cnn_train.py --img_dir ../scalograms --target feed
python cnn_train.py --img_dir ../scalograms --target doc
```

**Optional training flags:**
```
--backbone     resnet18 | resnet50 | efficientnet_b0   (default: resnet18)
--augment      none | light | strong                   (default: light)
--epochs       30                                      (default: 30)
--lr           0.001                                   (default: 0.001)
--freeze                                               (freeze backbone, train head only)
```

**Predict on a new file:**
```bash
python predict.py --csv ../data/run24.csv --target speed
python predict.py --csv ../data/run13.csv --target feed
python predict.py --csv ../data/run7.csv  --target doc
```

---

## Trained Model Files

| File | Target | Classes |
|------|--------|---------|
| `best_model.pt`      | Speed | 5 |
| `best_model_feed.pt` | Feed  | 6 |
| `best_model_doc.pt`  | DOC   | 3 |

---

## Test / Train Split

Test runs are held out before any training and never seen by the model during training:

**Speed** — 5 test runs (1 per RPM class, all DOC=0.060):
run24, run27, run30, run33, run36

**Feed** — 6 test runs (1 per mm/rev class, spread across DOC/speed):
run25 (3mm), run13 (4mm), run31 (5mm), run17 (6mm), run5 (7mm), run36 (8mm)

**DOC** — 9 test runs (3 per DOC class, spread across speeds):
run1, run5, run43 (0.015mm) | run7, run14, run19 (0.030mm) | run22, run29, run36 (0.060mm)

---

## Limitations

The scalogram normalization rescales each image independently to fill the full 0-255 range, which removes absolute amplitude information. Because DOC and feed primarily change signal amplitude rather than frequency structure, the CNN struggles to distinguish them reliably. The FFT/SVM model in `../fft_model/` is better suited for DOC and feed classification for this reason.

Speed classification works well because different RPMs place harmonic peaks at distinct frequency positions, which survive normalization.
