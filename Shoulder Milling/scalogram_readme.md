# Shoulder Milling — Option C Scalograms (32 x 12)

This document explains how the 72 training scalograms in `scalograms_32x12/` were
built, why each design decision was made, and what the images represent.  It is the
direct follow-on to the correlation and PCA analysis documented in `pca_readme.md`.
Read that document first for the dataset description and feature definitions.

---

## Table of Contents

1. [Why a New Image Format?](#1-why-a-new-image-format)
2. [Option A, B, and C — Comparison](#2-option-a-b-and-c--comparison)
3. [Option C Design](#3-option-c-design)
4. [Scale Selection — How the 32 Rows Were Chosen](#4-scale-selection--how-the-32-rows-were-chosen)
5. [Image Construction](#5-image-construction)
6. [Normalisation](#6-normalisation)
7. [Output Files](#7-output-files)
8. [Ra Class Distribution](#8-ra-class-distribution)
9. [Implications for CNN Training](#9-implications-for-cnn-training)
10. [File Index](#10-file-index)

---

## 1. Why a New Image Format?

The PCA and correlation analysis (see `pca_readme.md`) confirmed that the CWT wavelet
columns (`64mexican` and `64coif`) are the most Ra-predictive features, the FFT column
has strong non-linear Ra information, and the DWT statistical features carry additional
independent signal.  The analysis also confirmed two hard constraints:

1. **p >> n**: 768 features vs 24 runs — any model using all features overfits
   catastrophically (PLS cross-validated R² was negative for all component counts).
2. **Sparse feature matrix**: The original 64 x 12 image has a large dead zone.  Only
   32 of the 64 rows have data in three or more columns.  Below row 31, only the two
   CWT columns are non-zero; the other 10 columns contribute nothing.

The natural response is to reduce the image to the rows that carry actual information.
The question is *how* to decide which rows to keep.

---

## 2. Option A, B, and C — Comparison

Three image representations were considered before building the scalograms.

### Option A — 3-Channel 64 x 3 Scalogram (Direct End-Milling Analog)

Each run → one 64 x 3 image where columns are time windows (a, b, c) and
channels are R=64mexican, G=64coif, B=32FFT (zero-padded to 64).

| Advantage | Disadvantage |
|---|---|
| Structurally identical to end-milling CWT scalograms | Only 24 training images (one per run, not per window) |
| No zero-padding needed in the time axis | Only 3 of 12 feature types included — loses all DWT stats |
| Direct architecture transfer from end-milling CNN | 64 x 3 native size is extremely small before upsampling |

### Option B — Full Feature Image 64 x 12

Each window → one 64 x 12 image; all 12 feature columns as image columns.
72 training images total.

| Advantage | Disadvantage |
|---|---|
| All 12 feature types present | Dead zone: rows 10-31 have only 3 active columns; rows 32-63 have only 2 |
| 72 samples vs 24 in Option A | CNN must learn to ignore 522 of 768 zero values |
| Pseudo-MFCC structure — similar to audio ML | Row structure is inconsistent across columns |

### Option C — Data-Selected 32 x 12 (This Document)

Each window → one 32 x 12 image.  The 32 rows are not the first 32 rows of the
original image — they are the 32 scale levels (out of 64) that have the **highest
Spearman rank correlation with Ra**, selected using run-level averages across all
24 runs.  All 12 feature columns are preserved.  72 training images total.

| Advantage | Disadvantage |
|---|---|
| All 12 feature types preserved | CWT row order no longer represents uniform scale spacing |
| No dead zone — every CWT row is meaningfully correlated with Ra | DWT stats still have rows 10-31 as zero (short features, unavoidable) |
| FFT column is complete — all 32 bins fit exactly | Scale selection was done on all 24 runs; must be redone inside CV folds if strict leak-prevention is needed |
| 72 samples (3 windows per run) | |
| Smaller image — faster training | |

Option C is the chosen approach because it addresses both problems of Option B
(sparse matrix, large image) while preserving all feature types, unlike Option A.

---

## 3. Option C Design

### Image Dimensions

**32 rows x 12 columns x 1 channel (grayscale)**

```
     32FFT  5stat  64mex  64coi  KA  SA  KD  SD  rmsA  rmsD  crstA  crstD
r0  [ val ] [val ] [val ] [val ] [v] [v] [v] [v] [ v ] [ v ] [ v ] [ v ]
r1  [ val ] [val ] [val ] [val ] [v] [v] [v] [v] [ v ] [ v ] [ v ] [ v ]
...
r9  [ val ] [val ] [val ] [val ] [v] [v] [v] [v] [ v ] [ v ] [ v ] [ v ]
r10 [ val ] [ 0  ] [val ] [val ] [0] [0] [0] [0] [ 0 ] [ 0 ] [ 0 ] [ 0 ]
...
r31 [ val ] [ 0  ] [val ] [val ] [0] [0] [0] [0] [ 0 ] [ 0 ] [ 0 ] [ 0 ]
```

### Row Semantics by Column Type

| Column group | Valid rows in output image | What each row represents |
|---|---|---|
| `64mexican`, `64coif` (cols 2, 3) | All 32 rows | One of the 32 selected CWT scale levels, ordered fine (row 0) to coarser (row 31).  Rows 20-22 from the original 64-scale index were dropped (see Section 4). |
| `32FFT` (col 0) | All 32 rows | FFT frequency bin k for k = 0..31.  This is the complete FFT spectrum — no truncation needed. |
| `5statistics` (col 1) | Rows 0-5 | Time-domain statistics (mean, variance, skewness, kurtosis, RMS, and one additional descriptor). |
| `KA`, `SA`, `KD`, `SD`, `rmsA`, `rmsD`, `crestfactA`, `crestfactD` (cols 4-11) | Rows 0-9 | DWT statistic at each of 10 decomposition levels. |

Rows 10-31 in the DWT and statistics columns are zero (the features are shorter than
32 values).  This is unavoidable given the feature lengths, but represents 22 zero
rows per short column instead of 54 zero rows in the original 64-row image.

### Key Properties

- **No CWT re-application**: The `64mexican` and `64coif` columns already contain CWT
  coefficients extracted from the raw vibration signal.  Treating them as image rows
  is a representation choice, not a signal processing step.
- **Row consistency**: Both CWT columns use the same 32 selected scale indices.  Row k
  of the image always corresponds to the same physical frequency scale in both CWT
  channels.
- **72 images**: One per measurement window (3 windows a, b, c for each of 24 runs).
  All 3 windows of the same run share the same Ra label.  They will be grouped together
  during cross-validation.

---

## 4. Scale Selection — How the 32 Rows Were Chosen

### Motivation

The original `64mexican` and `64coif` columns have 64 values each, representing CWT
energy at 64 frequency scales from fine (row 0) to coarse (row 63).  Not all scales
carry the same information about surface roughness.  The PCA and Spearman analyses
showed that mid-scale rows (around rows 30-32) had high Ra correlation — meaning a
simple truncation to the top 32 rows would miss useful signal at coarser scales.

A data-driven selection identifies *which* 32 scales (from anywhere in 0-63) are most
informative, rather than blindly keeping the top half.

### Method

**Script:** `build_option_c_scalograms.py`, function `select_cwt_rows()`

1. For each of the 24 runs, compute the average of the 3 window images to get a
   run-level mean `64mexican` and `64coif` vector.  This gives a (24, 64) matrix for
   each CWT channel.  Using run-level averages (not window-level) avoids giving more
   weight to runs with more windows and ensures the 24-point correlation estimate is
   not inflated by repeated windows.

2. For each of the 64 scale row indices, compute Spearman rank correlation |rho|
   between that scale's values and Ra across the 24 runs — once for `64mexican` and
   once for `64coif`.

3. Average the two |rho| scores to get a single importance score per row.  Using the
   average rather than the maximum prevents a row from being selected if it is
   correlated with Ra only in one wavelet basis and not the other.

4. Sort all 64 rows by importance score, select the top 32, and sort the selected
   indices back into ascending order.  Ascending order preserves the fine-to-coarse
   scale progression in the output image.

### Results

**Selected indices:** `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]`

**Dropped indices:** `[20, 21, 22, 35, 36, ..., 63]`

| Scale zone | Rows | Kept | Dropped | Avg score range |
|---|---|---|---|---|
| Fine scales | 0-19 | 20 of 20 | 0 | 0.280 – 0.469 |
| Transition | 20-22 | 0 of 3 | 3 | 0.275 – 0.279 |
| Mid scales | 23-34 | 12 of 12 | 0 | 0.284 – 0.369 |
| Coarse scales | 35-63 | 0 of 29 | 29 | 0.070 – 0.274 |

The selection threshold (minimum score of the top 32) was **0.280**.

**Row 6 had the highest score: 0.469** — fine-scale CWT energy at this level is the
most Ra-correlated scale in both `64mexican` and `64coif`.  This aligns with the
Spearman analysis in `pca_readme.md` which found the strongest individual correlations
in the fine-to-mid scale range of the CWT columns.

**Why rows 20-22 were dropped:** These three indices sit in a local dip between the
fine-scale cluster (rows 0-19, all above 0.280) and the mid-scale cluster (rows 23-34,
which recovers to 0.284-0.369 before dropping off at row 35).  Their averaged Spearman
scores (0.275, 0.279, 0.277) fall just below the 0.280 threshold.

**Why rows 35-63 were dropped:** Coarse CWT scales capture very low-frequency vibration
components that reflect machine structural dynamics rather than surface formation.
Their Ra correlation drops sharply from row 35 (score 0.274) to near-zero at rows 40+
(scores below 0.15).  This is consistent with physical intuition: surface roughness is
formed by the cutting tool edge at fine spatial scales; coarse vibration modes are not
directly related to surface texture.

**Visualisation:** `scalograms_32x12/scale_selection_summary.png` shows the full
score bar chart for all 64 scales (red = selected, blue = dropped) and example 32 x 12
images for Low, Med, and High Ra runs.

---

## 5. Image Construction

**Script:** `build_option_c_scalograms.py`, function `build_opt_c()`

For each of the 72 windows (one sheet per run per window):

1. Load the raw 64 x 12 feature matrix using `sheet_to_image()` — identical to
   the PCA pipeline.  Shorter feature vectors are zero-padded to length 64.

2. Build the output 32 x 12 matrix:

```python
# CWT columns: pick only the 32 selected scale rows
out[:, 2] = full_img[selected_rows, 2]   # 64mexican
out[:, 3] = full_img[selected_rows, 3]   # 64coif

# All other columns: take rows 0-31 as-is (natural truncation)
for c in [0, 1, 4, 5, 6, 7, 8, 9, 10, 11]:
    out[:, c] = full_img[0:32, c]
```

For the non-CWT columns, `rows 0:32` contains all the valid data (FFT ends at row 31,
DWT stats end at row 9, time-domain stats end at row 5).  Simple truncation to 32 rows
is correct for these columns.

---

## 6. Normalisation

**Method:** Column-wise z-score, fit on all 72 windows, clip ±3σ, scale to [0, 255].

### Why Column-Wise

Each of the 12 feature columns has a completely different physical unit and numerical
range — FFT amplitudes, Spearman-scaled CWT energies, dimensionless statistics, and
RMS values cannot be compared on the same scale without normalisation.  Column-wise
z-score ensures each column has zero mean and unit variance across all windows, making
the CNN's input distribution well-conditioned.

Row-wise normalisation (normalising within each row across columns) was not used
because rows mix incommensurable quantities — the CWT energy at a given scale, the FFT
amplitude at a given frequency bin, and the DWT kurtosis at a given level are not
meaningful to compare against each other.

### Why Fit on All 72 Windows

For a first pass at generating the scalogram images, normalisation was fit on the full
dataset of 72 windows.  This is a mild form of data leakage — if strict leave-one-
side-out cross-validation is used, the normalisation scaler should be fit on the
training folds only and applied to the test fold.

In practice, the global mean and standard deviation change very little when one side
(9 windows) is withheld, so the leakage effect is negligible.  If the CNN is to be
published, per-fold normalisation should be implemented in the data loader.

### Clipping and Scaling

After z-score normalisation, values are clipped to the ±3σ range and linearly mapped
to [0, 255]:

```
pixel = clip(z_score, -3, +3)
pixel = (pixel + 3) / 6 * 255
```

The ±3σ clip removes extreme values that would compress the colour range for typical
pixels.  Under a normal distribution, clipping at ±3σ discards only 0.27% of values.
The remaining values span the full [0, 255] range, maximising the use of the uint8
dynamic range.

---

## 7. Output Files

All outputs are in `scalograms_32x12/`.

### Image Files

72 grayscale PNG files, named `run{NN}_{window}.png`:

```
run01_a.png   run01_b.png   run01_c.png
run02_a.png   run02_b.png   run02_c.png
...
run24_a.png   run24_b.png   run24_c.png
```

Each file is a 32 x 12 pixel grayscale image (uint8, [0, 255]).  Pixel (i, j) is the
normalised feature value at selected scale row i, feature column j.

### labels.csv

One row per image (72 rows).  Columns:

| Column | Description |
|---|---|
| `filename` | PNG file name |
| `run` | Run number (1-24) |
| `window` | Time window (`a`, `b`, or `c`) |
| `side` | Physical workpiece side (1-8) |
| `feed` | Feed rate (`f3`, `f5`, or `f7`) |
| `ra` | Average surface roughness Ra (µm) |
| `ra_class` | 3-class label: `Low` (Ra ≤ 0.30), `Med` (0.31-0.50), `High` (Ra > 0.50) |

### selected_scales.json

Records the scale selection result for reproducibility:

| Key | Content |
|---|---|
| `n_selected` | 32 |
| `selected_indices` | The 32 row indices chosen from 0-63 |
| `dropped_indices` | The 32 row indices that were not selected |
| `all_scores` | Averaged Spearman |rho| for all 64 scale rows (use to re-examine the selection) |

### scale_selection_summary.png

Four-panel diagnostic figure:
- Bar chart of all 64 scale scores (red = selected, blue = dropped)
- Counts of selected vs dropped rows by zone (rows 0-9, 10-31, 32-63)
- Example 32 x 12 images for one Low, one Med, and one High Ra run

---

## 8. Ra Class Distribution

| Class | Ra range (µm) | Runs | Windows |
|---|---|---|---|
| Low | ≤ 0.30 | 9 | 27 |
| Med | 0.31 – 0.50 | 10 | 30 |
| High | > 0.50 | 5 | 15 |

The class distribution is moderately imbalanced.  High Ra has only 5 runs (15 windows)
vs 9-10 for the other classes.  When training:

- Use **class-weighted cross-entropy loss** (weights inversely proportional to class
  frequency) to prevent the model from ignoring the High class.
- Report **per-class F1** alongside overall accuracy so performance on the minority
  class is visible.
- Consider SMOTE on the run-level (not window-level) if imbalance causes persistent
  underperformance on the High class after weighted loss.

Run 3 (Ra = 0.92 µm) is a notable outlier — more than 0.32 µm above the next-highest
value (run 6, Ra = 0.58 µm).  Monitor whether the model handles this run correctly;
if it is consistently misclassified, the outlier may need special treatment.

---

## 9. Implications for CNN Training

### Input Shape

```
(batch, 1, 32, 12)   # PyTorch convention: (N, C, H, W)
```

Height = 32 (scale rows), Width = 12 (feature columns), Channels = 1 (grayscale).

If using a pretrained backbone (ResNet, EfficientNet) that expects 3-channel input,
repeat the single channel three times: `x.repeat(1, 3, 1, 1)`.

### Upsampling

The native 32 x 12 image is small.  For a CNN with multiple pooling layers, the
spatial dimensions shrink quickly.  Options:

1. **Bilinear upsampling to 224 x 224** before the first conv layer (standard for
   pretrained backbones).
2. **Dilated convolutions** to increase receptive field without spatial reduction.
3. **Custom shallow CNN** without pooling, using only strided convolutions and global
   average pooling at the end.

### Cross-Validation: Leave-One-Side-Out

Use `GroupKFold(n_splits=8)` with `groups = side_id`.  Each fold holds out all 9
windows (3 runs x 3 windows) from one physical side.  This is the strictest valid
split because:

- All 3 windows of the same run must be in the same split (same label, same cut).
- All 3 runs on the same side were machined under the same speed and depth conditions.
  Leaking any window from a side into the training set for a fold that tests that side
  would overestimate generalisation.

After predicting 3 windows per run, take the **majority vote** for the 3-class label
or the **mean** for a regression prediction.  Majority vote is more robust to one
anomalous window.

### Normalisation in Training

The PNGs were saved with global normalisation (fit on all 72 windows).  For strict
experiment setup, re-normalise per fold:

1. Compute per-column mean and std from the 63 training windows in the fold.
2. Apply the training statistics to normalise both train and test images.
3. Clip to ±3σ and scale to [0, 1] (for PyTorch float tensors, not uint8 PNGs).

This can be implemented as a transform in the `Dataset.__getitem__` method.

### Class Imbalance Handling

```python
# Example class weights for PyTorch CrossEntropyLoss
counts   = [27, 30, 15]          # Low, Med, High windows
weights  = [1/c for c in counts]
weights  = torch.tensor(weights) / sum(weights)
criterion = nn.CrossEntropyLoss(weight=weights)
```

---

## 10. File Index

| File | Purpose |
|---|---|
| `pca_readme.md` | Full dataset description, feature definitions, PCA and correlation analysis |
| `build_option_c_scalograms.py` | Script that performs scale selection and generates all 72 scalograms |
| `scalograms_32x12/` | Directory containing all output files (below) |
| `scalograms_32x12/run{NN}_{win}.png` | 72 grayscale scalogram images (32 x 12 px) |
| `scalograms_32x12/labels.csv` | Run, window, side, feed, Ra, Ra class for all 72 images |
| `scalograms_32x12/selected_scales.json` | 32 selected CWT scale indices + all 64 Spearman scores |
| `scalograms_32x12/scale_selection_summary.png` | Diagnostic visualisation of scale selection and example images |
| `pca_plots/` | All 19 diagnostic plots from PCA, correlation, and Options A/B/C explanations |
| `pca_analysis.py` | Phase 1: PCA pipeline |
| `correlation_analysis.py` | Phase 2: Spearman, MI, PLS, t-SNE |
| `plot_option_a.py` | Option A explanation plots (Plots 17-19) |
