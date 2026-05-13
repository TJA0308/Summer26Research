# Steel Milling Vibration Analysis

Classifies steel milling process parameters (spindle speed, depth of cut, feed rate) from raw vibration signals using CNN-based scalogram classification.

## Data

45 runs recorded at 16,393 Hz with three sensor channels: ai4 (feed-axis vibration), ai5 (cross-axis, unused), and ai6 (acoustic). Each run is ~65,000 samples (~4 seconds). Run parameters come from `steel Milling Signal files and Surface Roughness.xlsx`.

| Runs | stlml files | DOC (mm) | Speed | Feed rates (mm/rev) |
|------|-------------|----------|-------|---------------------|
| run1–run3   | stlml_10–12 | 0.015 | 4000 rpm | 5, 6, 7 |
| run4–run6   | stlml_13–15 | 0.015 | 5000 rpm | 6, 7, 8 |
| run7–run9   | stlml_16–18 | 0.030 | 1500 rpm | 3, 4, 5 |
| run10–run12 | stlml_19–21 | 0.030 | 2000 rpm | 3, 4, 5 |
| run13–run15 | stlml_22–24 | 0.030 | 3000 rpm | 4, 5, 6 |
| run16–run18 | stlml_25–27 | 0.030 | 4000 rpm | 5, 6, 7 |
| run19–run21 | stlml_28–30 | 0.030 | 5000 rpm | 6, 7, 8 |
| run22–run24 | stlml_31–33 | 0.060 | 1500 rpm | 3, 4, 5 |
| run25–run27 | stlml_34–36 | 0.060 | 2000 rpm | 3, 4, 5 |
| run28–run30 | stlml_37–39 | 0.060 | 3000 rpm | 4, 5, 6 |
| run31–run33 | stlml_40–42 | 0.060 | 4000 rpm | 5, 6, 7 |
| run34–run36 | stlml_43–45 | 0.060 | 5000 rpm | 6, 7, 8 |
| run37–run39 | stlml_1–3   | 0.015 | 1500 rpm | 3, 4, 5 |
| run40–run42 | stlml_4–6   | 0.015 | 2000 rpm | 3, 4, 5 |
| run43–run45 | stlml_7–9   | 0.015 | 3000 rpm | 4, 5, 6 |

## Trained Models

Four models are saved in the project root:

| File | Predicts | Classes | Test Accuracy | Scalogram dir needed |
|------|----------|---------|---------------|----------------------|
| `model_speed.pt` | Spindle speed | 5 (1500–5000 rpm) | **100%** | `scalograms_ai4_ai6` |
| `model_doc.pt` | Depth of cut | 3 (0.015/0.030/0.060 mm) | **100%** | `scalograms_ai4_ai6` |
| `model_feed_coarse.pt` | Feed rate (coarse) | 3 (low/med/high) | **66.7%** | `scalograms_ai4_ai6` |
| `model_feed.pt` | Feed rate (fine) | 6 (3–8 mm/rev) | **50%** | `scalograms_ai4_ai6_4w` |

## Pipeline

### 1. Generate scalograms — `cnn_model/scalogram.py`

Converts each CSV into a 224×224 RGB scalogram PNG using an analytic Morlet CWT.

```bash
# 1 window per run (for speed, doc, feed_coarse)
python cnn_model/scalogram.py --input_dir data --output_dir scalograms_ai4_ai6

# 4 windows per run (for feed fine-grained — more training data per run)
python cnn_model/scalogram.py --input_dir data --output_dir scalograms_ai4_ai6_4w --n_windows 4
```

### 2. Train — `cnn_model/cnn_train.py`

Fine-tunes a pretrained ResNet18. Test runs are held out before training and never used to update weights:

- **Speed test runs:** run24, run27, run30, run33, run36
- **Feed test runs:** run25, run13, run31, run17, run5, run36
- **DOC test runs:** run1, run5, run43, run7, run14, run19, run22, run29, run36

```bash
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6 --target speed --save model_speed.pt
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6 --target doc --save model_doc.pt
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6 --target feed_coarse --save model_feed_coarse.pt
python cnn_model/cnn_train.py --img_dir scalograms_ai4_ai6_4w --target feed --epochs 40 --save model_feed.pt
```

## Project Structure

```
data/                     Raw CSV signal files (run1.csv – run45.csv)
cnn_model/                CNN + scalogram pipeline
  scalogram.py            Generates scalogram PNGs from CSVs
  cnn_train.py            Trains ResNet18 classifier
  cnn_svm.py              Alternative: SVM on CNN features
fft_model/                FFT-based frequency classifier
scalograms_ai4_ai6/       1-window scalograms (45 images)
scalograms_ai4_ai6_4w/    4-window scalograms (180 images)
model_speed.pt            Best speed model (100%)
model_doc.pt              Best DOC model (100%)
model_feed_coarse.pt      Best coarse feed model (66.7%)
model_feed.pt             Best fine-grained feed model (50%)
```

See `cnn_model/README.md` for full detail on training options, per-class results, and why feed rate is harder to classify than speed or DOC.
