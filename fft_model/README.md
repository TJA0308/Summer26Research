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

The feature extraction method differs by target:

**Speed** — harmonic peak power (60 features):
The spindle rotation creates vibration peaks at exact harmonic frequencies. A spindle at 1500 rpm vibrates at 25 Hz, 50 Hz, 75 Hz, 100 Hz (fundamental + 3 harmonics). The feature vector samples FFT power at all 5 RPM classes x 4 harmonics x 3 channels. The class whose harmonic slots have the highest power wins.

| RPM  | Fundamental | Harmonic 2 | Harmonic 3 | Harmonic 4 |
|------|-------------|------------|------------|------------|
| 1500 | 25.0 Hz     | 50.0 Hz    | 75.0 Hz    | 100.0 Hz   |
| 2000 | 33.3 Hz     | 66.7 Hz    | 100.0 Hz   | 133.3 Hz   |
| 3000 | 50.0 Hz     | 100.0 Hz   | 150.0 Hz   | 200.0 Hz   |
| 4000 | 66.7 Hz     | 133.3 Hz   | 200.0 Hz   | 266.7 Hz   |
| 5000 | 83.3 Hz     | 166.7 Hz   | 250.0 Hz   | 333.3 Hz   |

**DOC** — broadband log-power (90 features, 30 bands x 3 channels):
Depth of cut scales the overall cutting force amplitude. Log-power summed across 30 log-spaced frequency bands (20-4000 Hz) preserves the absolute amplitude differences between DOC levels that distinguish the classes.

**Feed** — see Two-Stage Approach below.

### Step 3: SVM

A Support Vector Machine with an RBF kernel (C=10, gamma=scale) finds decision boundaries in the feature space. StandardScaler normalizes the features before the SVM sees them.

### Evaluation: Leave-One-Run-Out Cross-Validation

Every run is used as a test example exactly once. For each of the 45 runs, the SVM trains on the remaining 44 and predicts the left-out run. This gives a fair, out-of-sample accuracy estimate without needing a fixed held-out split.

---

## Feed Rate: Two-Stage Approach

### Why naive feed classification fails

Feed rate (3-8 mm/rev) primarily changes signal amplitude, similar to DOC. When a single classifier tries to predict feed across all 45 runs, it gets confused because:
- Speed changes the harmonic positions (dominant effect)
- DOC changes the overall amplitude uniformly (strong effect)
- Feed also changes amplitude, but more subtly

The SVM cannot reliably isolate the feed signal when DOC and speed are also varying.

### The fix: two stages

**Stage 1 — Predict speed first (97.8% accurate)**

Use the harmonic-peak SVM to predict the spindle speed. This works near-perfectly because each RPM leaves a unique frequency fingerprint.

**Stage 2 — Predict feed within the speed group**

Once speed is known, the problem shrinks dramatically:
- At a fixed speed, only 3 feed values appear in the dataset (not 6)
- Speed variation no longer confounds the classifier

| Speed | Feed values present |
|-------|-------------------|
| 1500 rpm | 3, 4, 5 mm/rev |
| 2000 rpm | 3, 4, 5 mm/rev |
| 3000 rpm | 4, 5, 6 mm/rev |
| 4000 rpm | 5, 6, 7 mm/rev |
| 5000 rpm | 6, 7, 8 mm/rev |

The Stage 2 classifier also uses **normalized spectral features**: each frequency band's power is divided by the total signal power before taking the log. This cancels out DOC's uniform amplitude effect (since DOC scales all bands equally, ratios between bands remain the same regardless of DOC). What remains is the spectral shape difference caused by feed rate alone.

```
raw feature:        log(power_in_band)
normalized feature: log(power_in_band / total_power)
```

### Summary of the pipeline

```
New signal
    │
    ├─► extract_speed_features() ─► Speed SVM ─► predicted speed (e.g. 4000 rpm)
    │
    └─► extract_feed_features_normalized()
              │
              └─► Feed SVM trained only on 4000 rpm runs ─► predicted feed (5/6/7 mm/rev)
```

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
python fft_model/freq_classify.py --target doc   --data_dir ./data --predict data/run7.csv
python fft_model/freq_classify.py --target feed  --data_dir ./data --predict data/run13.csv
```

---

## Results

| Target | Accuracy | Method |
|--------|----------|--------|
| Speed  | 97.8% (44/45) | Harmonic peak SVM |
| DOC    | 95.6% (43/45) | Broadband log-power SVM |
| Feed   | ~11% (5/45)   | Two-stage: speed → normalized feed |

### Why feed accuracy is low

Feed rate is fundamentally difficult to classify from vibration signals in this dataset for two reasons:

**1. DOC and feed have nearly identical effects on amplitude.**
Cutting force scales with DOC × feed. Both variables increase signal power in the same way. Even after normalizing out amplitude, the spectral *shape* differences between feed values are too small to detect reliably.

**2. Too few training examples per group.**
Within each speed group there are only 9 runs (3 DOC levels × 3 feed values). After leaving one out for testing, the SVM trains on 8 examples across 3 classes — roughly 2-3 examples per class. This is not enough to learn a reliable boundary.

The only robust fixes would be collecting significantly more data, or using a direct force sensor rather than vibration.

---

## When to Use FFT/SVM vs CNN

| Situation | FFT/SVM | CNN |
|-----------|---------|-----|
| Predicting spindle speed | Excellent | Good |
| Predicting depth of cut | Good | Poor (amplitude normalized away in scalogram) |
| Predicting feed rate | Good (two-stage) | Poor (amplitude normalized away in scalogram) |
| No GPU available | Yes | Slow without GPU |
| Need to inspect which frequencies matter | Easy | Hard |
