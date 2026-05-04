# FFT + SVM Model

## Overview

This approach extracts frequency-domain features from raw vibration signals using the Fast Fourier Transform (FFT), then trains a Support Vector Machine (SVM) to classify those features.

```
Raw CSV signals → FFT → feature vector → SVM → prediction
```

No images are generated. No GPU is needed. The full pipeline runs in seconds.

---

## How It Works

### Step 1: FFT

Each raw CSV file contains three vibration channels (ai4, ai5, ai6) sampled at 16,393 Hz. The FFT converts each channel from the time domain into the frequency domain, producing a spectrum showing how much power exists at each frequency.

### Step 2: Feature Extraction

Rather than feeding the raw spectrum into the SVM, the power is summarised into a compact feature vector. The method differs by target:

**Speed** — harmonic peak power:
The spindle rotation creates vibration peaks at exact harmonic frequencies. A spindle at 1500 rpm vibrates at 25 Hz, 50 Hz, 75 Hz, 100 Hz (fundamental + 3 harmonics). The feature vector samples the FFT power at all 5 RPM classes x 4 harmonics x 3 channels = 60 features. The class whose harmonic slots have the highest power wins.

| RPM  | Fundamental | Harmonic 2 | Harmonic 3 | Harmonic 4 |
|------|-------------|------------|------------|------------|
| 1500 | 25.0 Hz     | 50.0 Hz    | 75.0 Hz    | 100.0 Hz   |
| 2000 | 33.3 Hz     | 66.7 Hz    | 100.0 Hz   | 133.3 Hz   |
| 3000 | 50.0 Hz     | 100.0 Hz   | 150.0 Hz   | 200.0 Hz   |
| 4000 | 66.7 Hz     | 133.3 Hz   | 200.0 Hz   | 266.7 Hz   |
| 5000 | 83.3 Hz     | 166.7 Hz   | 250.0 Hz   | 333.3 Hz   |

**DOC** — broadband log-power (30 bands, 20-4000 Hz):
Depth of cut scales the overall cutting force amplitude. The feature vector captures log-power summed across 30 log-spaced frequency bands, preserving absolute amplitude differences between DOC levels.

**Feed** — broadband log-power (50 bands, 20-4000 Hz):
Feed rate similarly affects force amplitude. Uses 50 bands for finer amplitude resolution across the 6 feed classes (3-8 mm/rev).

### Step 3: SVM

A Support Vector Machine with an RBF kernel (C=10, gamma=scale) finds decision boundaries in the feature space. StandardScaler normalizes the features before the SVM sees them.

### Evaluation: Leave-One-Run-Out Cross-Validation

Every run is used as a test example exactly once. For each of the 45 runs, the SVM trains on the remaining 44 and predicts the left-out run. This gives a fair, out-of-sample accuracy estimate for every run without needing a fixed held-out split.

After CV, a final model is trained on all 45 runs and can be used for single-file prediction.

---

## Commands

All commands should be run from the **project root** (`Summer26Research/`).

**Run cross-validation for each target:**
```bash
python fft_model/freq_classify.py --target speed --data_dir ./data
python fft_model/freq_classify.py --target doc   --data_dir ./data
python fft_model/freq_classify.py --target feed  --data_dir ./data
```

**Predict on a single new file:**
```bash
python fft_model/freq_classify.py --target speed --data_dir ./data --predict data/run24.csv
python fft_model/freq_classify.py --target feed  --data_dir ./data --predict data/run13.csv
python fft_model/freq_classify.py --target doc   --data_dir ./data --predict data/run7.csv
```

---

## When to Use FFT/SVM vs CNN

| Situation | FFT/SVM | CNN |
|-----------|---------|-----|
| Predicting spindle speed | Excellent | Good |
| Predicting depth of cut | Good | Poor (amplitude normalized away) |
| Predicting feed rate | Good | Poor (amplitude normalized away) |
| No GPU available | Yes | Slow without GPU |
| Need to inspect which frequencies matter | Easy | Hard |
