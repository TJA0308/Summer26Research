# Steel Milling Vibration Analysis

Converts steel milling vibration signals into scalogram images and trains a CNN to classify spindle speed from those images.

## Data

Each run is a CSV recorded at 16,393 Hz with 3 sensor channels (ai4, ai5, ai6) and ~65,000 samples (~4 seconds). Run parameters come from `steel Milling Signal files and Surface Roughness.xlsx`.

There are 45 runs across 3 depth-of-cut (DOC) conditions and 5 spindle speeds (source: `steel Milling Signal files and Surface Roughness.xlsx`):

| Runs | stlml files | DOC (mm) | Speed | Feed rates (mm/rev) |
|------|-------------|----------|-------|---------------------|
| run1–run3   | stlml_10–12 | 0.015 | 4000 rpm | 5, 6, 7 |
| run4–run6   | stlml_13–15 | 0.015 | 5000 rpm | 6, 7, 8 |
| run7–run9   | stlml_16–18 | 0.03  | 1500 rpm | 3, 4, 5 |
| run10–run12 | stlml_19–21 | 0.03  | 2000 rpm | 3, 4, 5 |
| run13–run15 | stlml_22–24 | 0.03  | 3000 rpm | 4, 5, 6 |
| run16–run18 | stlml_25–27 | 0.03  | 4000 rpm | 5, 6, 7 |
| run19–run21 | stlml_28–30 | 0.03  | 5000 rpm | 6, 7, 8 |
| run22–run24 | stlml_31–33 | 0.06  | 1500 rpm | 3, 4, 5 |
| run25–run27 | stlml_34–36 | 0.06  | 2000 rpm | 3, 4, 5 |
| run28–run30 | stlml_37–39 | 0.06  | 3000 rpm | 4, 5, 6 |
| run31–run33 | stlml_40–42 | 0.06  | 4000 rpm | 5, 6, 7 |
| run34–run36 | stlml_43–45 | 0.06  | 5000 rpm | 6, 7, 8 |
| run37–run39 | stlml_1–3   | 0.015 | 1500 rpm | 3, 4, 5 |
| run40–run42 | stlml_4–6   | 0.015 | 2000 rpm | 3, 4, 5 |
| run43–run45 | stlml_7–9   | 0.015 | 3000 rpm | 4, 5, 6 |

The model is trained to classify **spindle speed only** (5 classes: 1500 / 2000 / 3000 / 4000 / 5000 rpm).

## Pipeline

### 1. Generate scalograms — `scalogram.py`

Converts each CSV into a 224×224 RGB PNG using an analytic Morlet Continuous Wavelet Transform (CWT). Each color channel corresponds to one sensor:

- Red = ai4, Green = ai5, Blue = ai6

The X-axis of the image is time, the Y-axis is frequency (20–4000 Hz, log-spaced). Pixel brightness encodes the instantaneous power at that frequency and time.

**Current settings:**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| FS | 16393 Hz | Original sample rate |
| DOWNSAMPLE | 2 | Effective rate = 8196 Hz |
| F_MIN / F_MAX | 20–4000 Hz | Frequency range |
| N_FREQS | 300 | Frequency bins |
| SIGMA | 8.0 | Morlet cycles — higher = sharper frequency resolution |
| IMG_SIZE | 224 | Output image size (matches ResNet default) |

```bash
# One image per run (default)
python scalogram.py --input_dir ./data --output_dir ./scalograms

# Multiple images per run via windowing (more training data, recommended)
python scalogram.py --input_dir ./data --output_dir ./scalograms --window_sec 0.5 --hop_sec 0.25
```

### 2. Train CNN — `cnn_train.py`

Fine-tunes a pretrained ResNet18 to classify spindle speed (5 classes). Train/test split is by run to prevent data leakage — 2 runs per speed class are held out for testing (10 test, 26 train).

```bash
python cnn_train.py --img_dir ./scalograms

# Options
python cnn_train.py --img_dir ./scalograms --epochs 30 --lr 1e-4 --batch 16
python cnn_train.py --img_dir ./scalograms --freeze   # freeze backbone, train head only
```

The best model (by test accuracy) is saved to `best_model.pt`.

### 3. Predict on a new run — `predict.py`

Generates the scalogram on the fly from a raw CSV and runs the trained model. No pre-generated image needed.

```bash
python predict.py --csv data/run1.csv
python predict.py --csv data/run1.csv --model best_model.pt
```

Output shows the predicted speed class and a probability bar for each of the 5 classes.

## Accuracy levers

| Lever | How | Expected effect |
|-------|-----|-----------------|
| **More images via windowing** | `--window_sec 0.5 --hop_sec 0.25` in `scalogram.py` | ~5–10× more training samples; biggest single gain |
| **Lower learning rate** | `--lr 1e-4` instead of default `1e-3` | Smoother convergence, less overfitting |
| **Freeze backbone first** | `--freeze` flag, then unfreeze and fine-tune | Useful when dataset is small |
| **More epochs** | `--epochs 50` | Allows cosine schedule to decay further |
| **Sharper frequency resolution** | Increase `SIGMA` in `scalogram.py` (e.g. 12.0) | More distinct frequency bands per speed |
| **Stronger augmentation** | Edit `build_transforms()` in `cnn_train.py` | Add `RandomRotation`, `GaussianBlur` |
| **Deeper backbone** | Swap `resnet18` → `resnet50` in `build_model()` | More capacity; helps once dataset is larger |

## Other Files

- `graph.py` — plots raw sensor channels from any subset of CSV files
- `cleanup.py` / `convert_stml_to_csv.py` — convert raw `.txt` signal files to CSV format
