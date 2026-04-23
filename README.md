# Steel Milling Vibration Analysis

Converts steel milling vibration signals into scalogram images and trains a CNN to classify spindle speed from those images.

## Data

Each run is a CSV recorded at 16,393 Hz with 3 sensor channels (ai4, ai5, ai6) and ~65,000 samples (~4 seconds). Run parameters come from `steel Milling Signal files and Surface Roughness.xlsx`.

The 9 current runs all share DOC = 0.015 mm and vary by spindle speed and feed rate:

| Runs | Speed | Feed (mm/rev) |
|------|-------|---------------|
| run1, run2, run3 | 1500 rpm | 3, 4, 5 |
| run4, run5, run6 | 2000 rpm | 3, 4, 5 |
| run7, run8, run9 | 3000 rpm | 4, 5, 6 |

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
| N_FREQS | 256 | Frequency bins |
| SIGMA | 8.0 | Morlet cycles — higher = sharper frequency resolution |
| IMG_SIZE | 224 | Output image size (matches ResNet default) |

```bash
# One image per run (current default)
python scalogram.py --input_dir ./data --output_dir ./scalograms_cnn

# Multiple images per run via windowing (more training data)
python scalogram.py --input_dir ./data --output_dir ./scalograms_cnn --window_sec 0.5 --hop_sec 0.25
```

### 2. Train CNN — `cnn_train.py`

Fine-tunes a pretrained ResNet18 to classify spindle speed (3 classes: 1500 / 2000 / 3000 rpm).

Train/test split is by run to prevent data leakage — runs 3, 6, and 9 are held out for testing, the remaining 6 are used for training.

```bash
python cnn_train.py --img_dir ./scalograms_cnn

# Options
python cnn_train.py --img_dir ./scalograms_cnn --epochs 30 --lr 1e-4 --batch 16
```

The best model (by test accuracy) is saved to `best_model.pt`.

## Current Limitations

With only 9 runs, the training set has 6 images and the test set has 3. The model memorizes training data immediately and test accuracy is not statistically meaningful. Results will improve significantly once the full 45-run dataset is available.

## Other Files

- `graph.py` — plots raw sensor channels from any subset of CSV files
- `cleanup.py` — converts raw `.txt` signal files to CSV format
