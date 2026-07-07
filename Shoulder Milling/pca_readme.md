# Shoulder Milling — Surface Roughness Prediction

This document tracks the full workflow for predicting surface roughness (Ra) from
pre-extracted vibration features in shoulder milling.  Every decision is explained
alongside the evidence that motivated it so the thought process is fully traceable.

---

## Table of Contents

1. [Project Context](#1-project-context)
2. [Dataset Description](#2-dataset-description)
3. [Feature Definitions](#3-feature-definitions)
4. [Data Structure and Label Mapping](#4-data-structure-and-label-mapping)
5. [Why Use a CNN at All?](#5-why-use-a-cnn-at-all)
6. [Phase 1 — PCA Analysis](#6-phase-1--pca-analysis)
7. [Phase 2 — Extended Correlation Analysis](#7-phase-2--extended-correlation-analysis)
8. [Consolidated Findings and What They Mean](#8-consolidated-findings-and-what-they-mean)
9. [Model Plan](#9-model-plan)
10. [File Index](#10-file-index)

---

## 1. Project Context

### Background

The broader project trains CNNs to predict milling process parameters from
vibration sensor data.  The prior work (in `End Milling/`) used **raw time-series**
accelerometer signals (channels `ai4` and `ai6`) and converted them to
**Continuous Wavelet Transform (CWT) scalograms** — 2D images where the axes are
frequency scale and time.  A CNN trained on those images classified spindle speed,
depth of cut, feed rate, and surface roughness.

### What Is Different Here

The shoulder milling dataset does **not** contain raw time-series.  Instead, it
contains features that were already extracted from the vibration signal before the
data was provided.  The extraction process produced 12 feature types per
measurement window, including FFT spectrum coefficients, wavelet scale coefficients,
and statistical descriptors.  These are stored in Excel spreadsheets.

This creates a fundamental architectural question: the end-milling pipeline applied
CWT to raw signals to produce images.  Here, the CWT has already been applied.
**We cannot re-apply CWT** to already-extracted features — it has no physical
meaning (CWT requires a time-domain input signal, not a frequency-domain spectrum
or a set of statistics).

The question is therefore: what is the right way to represent these feature vectors
as model inputs, and what model architecture is appropriate given the dataset size?

### Target Variable

Average surface roughness **Ra (µm)** measured at 5 positions per run.  Provided in
`data/Surface Roughness_Data.xlsx`.

---

## 2. Dataset Description

### Experimental Setup

- Material: Steel
- Tool: Carbide inserts, 3-tooth end mill
- Controlled parameters:
  - Spindle speed: 2500 RPM or 3500 RPM
  - Feed rate: 3, 5, or 7 in/min (varied within each side)
  - Y-depth: 0.5 in or 0.25 in
  - Z-depth: 0.25 in or 0.125 in
- 8 physical workpiece sides, each machined at one combination of speed + depth
- 3 feed rates applied to each side = **24 experimental runs total**

### File Layout

```
data/
  Side1.xlsx  ...  Side8.xlsx    — feature matrices (8 files)
  Surface Roughness_Data.xlsx   — Ra labels
```

Each `SideN.xlsx` contains **9 sheets**, one per (feed rate × time window):

```
Sheet name format:  s{rpm}f{feed}y{ydepth}z{zdepth}_{window}
  s25 / s35   = 2500 / 3500 RPM
  f3 / f5 / f7 = feed 3, 5, 7 in/min
  y5 / y25    = Y-depth 0.5 / 0.25 in
  z25 / z125  = Z-depth 0.25 / 0.125 in
  _a / _b / _c = time windows a, b, c
```

Each sheet is a **65 × 12 matrix**: row 0 is a header, rows 1–64 are feature values.

### Dataset Size

| Level | Count |
|---|---|
| Physical sides | 8 |
| Experimental runs | 24 (8 sides × 3 feed rates) |
| Time windows per run | 3 (a, b, c) |
| **Total feature matrices** | **72** |
| Features per matrix | 64 rows × 12 columns = 768 values |

The 3 windows of the same run all share the **same Ra label**.  This is equivalent
to the 10-window approach in the end-milling pipeline — multiple overlapping time
slices of the same cut.  Window-level predictions will later be aggregated by
majority vote (classification) or averaging (regression) to give one prediction
per run.

### Ra Distribution

| Class | Threshold | Runs | Windows |
|---|---|---|---|
| Low | Ra ≤ 0.30 µm | 9 | 27 |
| Med | 0.31 – 0.50 µm | 10 | 30 |
| High | Ra > 0.50 µm | 5 | 15 |

Ra range: 0.18 – 0.92 µm.  The value Ra = 0.92 (run 3) is a notable outlier —
more than 0.3 µm above the next-highest value (0.60).  This is worth monitoring
in model evaluation.

---

## 3. Feature Definitions

Each sheet contains 12 feature columns.  Each column is a vector of different
length; shorter vectors have `NaN` values in the remaining rows (treated as zeros
when building the feature image).

| Column | Valid rows | Description |
|---|---|---|
| `32FFT` | 0–31 | 32 FFT frequency-bin amplitudes, normalised so bin 0 = 1.0 (DC reference). Captures the spectral energy distribution of the vibration signal. |
| `5statistics` | 0–5 | 6 time-domain statistics: likely mean, variance, skewness, kurtosis, RMS, and one additional descriptor. |
| `64mexican` | 0–63 | 64 scale coefficients from a CWT using the Mexican hat (Ricker) wavelet. Each entry is the energy at one frequency scale. This IS a scalogram column — it spans fine to coarse scales across all 64 entries. |
| `64coif` | 0–63 | 64 scale coefficients from a CWT using the Coiflet wavelet. Same structure as `64mexican` but different wavelet basis. |
| `KA` | 0–9 | Kurtosis of the DWT **Approximation** coefficients at each of 10 decomposition levels. Level 0 = finest scale (highest frequency). |
| `SA` | 0–9 | Skewness of the DWT **Approximation** coefficients (10 levels). |
| `KD` | 0–9 | Kurtosis of the DWT **Detail** coefficients (10 levels). |
| `SD` | 0–9 | Skewness of the DWT **Detail** coefficients (10 levels). |
| `rmsA` | 0–9 | RMS of the DWT **Approximation** coefficients (10 levels). |
| `rmsD` | 0–9 | RMS of the DWT **Detail** coefficients (10 levels). |
| `crestfactA` | 0–9 | Crest factor of DWT **Approximation** coefficients (10 levels). |
| `crestfactD` | 0–9 | Crest factor of DWT **Detail** coefficients (10 levels). |

**Total valid values per matrix:** 32 + 6 + 64 + 64 + 10×8 = **246 values**  
(the remaining 768 − 246 = 522 positions are zero-padded)

---

## 4. Data Structure and Label Mapping

### Side → Run Mapping

| Side file | Runs | Speed | Y-depth | Z-depth |
|---|---|---|---|---|
| Side1.xlsx | 1, 2, 3 | 2500 RPM | 0.5 in | 0.25 in |
| Side2.xlsx | 13, 14, 15 | 3500 RPM | 0.5 in | 0.25 in |
| Side3.xlsx | 4, 5, 6 | 2500 RPM | 0.25 in | 0.25 in |
| Side4.xlsx | 16, 17, 18 | 3500 RPM | 0.25 in | 0.25 in |
| Side5.xlsx | 7, 8, 9 | 2500 RPM | 0.5 in | 0.125 in |
| Side6.xlsx | 19, 20, 21 | 3500 RPM | 0.5 in | 0.125 in |
| Side7.xlsx | 10, 11, 12 | 2500 RPM | 0.25 in | 0.125 in |
| Side8.xlsx | 22, 23, 24 | 3500 RPM | 0.25 in | 0.125 in |

Within each side: feed f3 → first run, f5 → second run, f7 → third run.

### Feature Image Construction

To feed the features into a CNN or any image-based model, we stack all 12 columns
into a **64 × 12 matrix**.  Shorter feature vectors are zero-padded to length 64.
This creates one image per measurement window.

```
Row   0–5:   All 12 columns have valid data (5stats, KA/SA/.., FFT, wavelet)
Row   6–9:   10 columns valid (5stats gone; FFT, wavelet, DWT stats)
Row  10–31:  3 columns valid  (only 32FFT, 64mexican, 64coif)
Row  32–63:  2 columns valid  (only 64mexican, 64coif; FFT ends at row 31)
```

The dense upper rows (0–9) carry the most simultaneous information.

---

## 5. Why Use a CNN at All?

### Motivation

The end-milling work showed that CNNs trained on 2D image representations of
vibration signals can classify milling process parameters with high accuracy.
The natural question is whether the same paradigm applies here.

### The Challenge: Pre-Extracted Features

Unlike raw time-series, the shoulder milling data is already in feature space.
The literature review (see below) found:

- **No published paper feeds a pre-extracted statistical feature matrix directly
  into a 2D CNN as an image.**  The field splits cleanly into: raw signal → CWT
  scalogram → CNN, or extracted features → classical ML (SVM, Random Forest, GPR).
- The closest structural analog is the **MFCC spectrogram** from speech/audio ML —
  a matrix where rows are frequency coefficients and columns are time frames.
  One 2025 paper (Sun et al., Scientific Reports) stacked signal segments into a
  2D matrix and fed it to a CNN for Ra classification, achieving 99.45% accuracy.
- A 2022 milling paper (Sensors, PMC8706467) compared CNN vs. Transformer on
  160 runs × 10 windows (1600 samples total).  A lightweight Transformer (34K
  parameters) achieved 92.7% vs. CNN 82.2%.  At small dataset scales, Transformers
  consistently outperform CNNs.
- A 2024 turning paper (Sensors, PMC11014149) used 50 workpieces with GPR on
  6 selected features (from 7 initial), achieving R² = 0.94.  Feature selection
  before modelling consistently improves generalisation on small datasets.

### The Fundamental Constraint

With 24 runs and a 768-dimensional feature vector, this is a **p >> n** problem
(features >> samples).  Any model that uses the full 768-dim vector will severely
overfit.  The PLS analysis (Phase 2) confirmed this empirically — cross-validated
R² was negative for all component counts, meaning the model performed worse than
a constant mean prediction.

The solution is **aggressive feature selection** informed by the correlation
analyses.

---

## 6. Phase 1 — PCA Analysis

**Script:** `pca_analysis.py`  
**Plots:** `pca_plots/1_explained_variance.png` through `pca_plots/7_row_importance.png`

### Why PCA First

PCA is the standard starting point for high-dimensional small-sample problems.  It
tells us:
1. How many independent dimensions of variation exist in the data
2. Which features drive that variation (loadings)
3. Whether Ra separates naturally in the principal component space

PCA is **unsupervised** — it does not know about the Ra label.  This is both a
strength (no overfitting to label noise) and a weakness (it cannot preferentially
surface Ra-related variation).
  
### Results

**Dimensionality (Plot 1):**  
10 PCs explain 90% of the total variance in a 768-dim space.  The data is
effectively 10-dimensional.  This is the maximum number of model parameters that
can be reliably estimated from 24 samples.

**PC–Ra correlation (Plot 5):**

| PC | Variance explained | Correlation with Ra |
|---|---|---|
| PC1 | 46.6% | r = 0.26 |
| PC2 | 20.9% | **r = 0.44** |
| PC3 | 6.1% | r = 0.10 |
| PC4 | 4.7% | r = −0.32 |
| PC5 | 3.4% | **r = 0.43** |
| PC6 | 2.9% | r = 0.13 |

The most variance-explaining PC (PC1) is only weakly correlated with Ra.  The
Ra-predictive signal is concentrated in PC2 and PC5, which together explain only
24% of variance.  This tells us that **machining parameter combinations (RPM ×
feed × depth) drive the dominant variance in the data, not roughness**.  Ra is a
secondary effect.

**Feature importance (Plot 6):**  
`64mexican` and `64coif` dominate — the CWT wavelet columns carry the most
structural variation.  `32FFT` is third.  The statistical features (SA, SD,
5statistics) contribute least under PCA.

**Row importance (Plot 7):**  
Rows 0–9 are the most important.  This is partly because those are the only rows
where all 12 columns have valid data simultaneously (the dense region of the
feature matrix).  After row 9, the DWT statistics go to zero; after row 31, the
FFT also goes to zero.

### Why PCA Is Not Sufficient

PCA confirmed that Ra-relevant variation exists in the data, but only in secondary
components.  To understand which specific features and positions correlate with Ra,
we need supervised or rank-based methods.  PCA also cannot tell us about
non-linear relationships between features and Ra.

---

## 7. Phase 2 — Extended Correlation Analysis

**Script:** `correlation_analysis.py`  
**Plots:** `pca_plots/8_spearman.png` through `pca_plots/13_tsne.png`

We ran four additional analyses, each addressing a limitation of PCA.

### 7.1 Spearman Rank Correlation

**Why:** Spearman rho measures monotonic (not just linear) relationships and is
robust to outliers.  The Ra = 0.92 outlier (run 3) could heavily distort Pearson
correlation, but Spearman is rank-based so outliers have bounded influence.

**Results — max |rho| per feature column:**

| Feature | Max |rho| | Interpretation |
|---|---|---|
| `64coif` | **0.623** | Strongest Ra correlation — specific coiflet scale coefficients strongly predict roughness |
| `SA` | **0.619** | DWT approximation skewness at a specific level is nearly as predictive |
| `64mexican` | 0.598 | Mexican hat CWT also strongly correlated |
| `rmsD` | 0.571 | RMS of DWT detail coefficients |
| `crestfactA` | 0.559 | Crest factor of DWT approximation |
| `SD` | 0.483 | DWT detail skewness |
| `KD` | 0.483 | DWT detail kurtosis |
| `KA` | 0.417 | DWT approximation kurtosis |
| `crestfactD` | 0.415 | DWT detail crest factor |
| `5statistics` | 0.393 | Time-domain statistics |
| `rmsA` | 0.376 | DWT approximation RMS |
| `32FFT` | 0.353 | FFT spectrum |

**Top individual positions:**
- `64coif` at rows 31 and 32 (rho = 0.623, 0.599) — coiflet energy at mid-scales
- `SA` at row 4 (rho = −0.619) — DWT approximation skewness at level 4 (negative: higher skewness → lower Ra)
- `64mexican` at rows 3, 4, 6 (rho ≈ 0.58–0.60) — Mexican hat energy at fine-to-mid scales

The **CWT wavelet columns dominate**, consistent with PCA.  Notably, `SA` (skewness
of DWT approximation at level 4) is the most Ra-correlated single statistical
feature, suggesting the amplitude distribution shape of the approximation signal at
a specific DWT level is highly informative.

**Key implication:** The sign of the `SA` correlation (negative) means that as the
vibration signal becomes more asymmetric (higher skewness), the surface is smoother.
This is physically plausible — higher feed rates produce more symmetric, periodic
vibration patterns and rougher surfaces.

### 7.2 Mutual Information

**Why:** Mutual information (MI) is non-parametric and captures any statistical
dependency, including U-shaped, threshold, or other non-linear relationships that
Spearman rho (which only measures monotonic trends) would miss.

**Results — max MI per feature column:**

| Feature | Max MI | Note |
|---|---|---|
| `32FFT` | **0.506** | Highest non-linear information about Ra |
| `64mexican` | 0.468 | |
| `SD` | 0.425 | DWT detail skewness — higher than Spearman suggested |
| `KA` | 0.389 | DWT approximation kurtosis |
| `rmsA` | 0.373 | |
| `rmsD` | 0.355 | |
| `SA` | 0.287 | Lower MI than Spearman rho — SA's relationship with Ra is mostly linear |
| `64coif` | 0.281 | Lower MI than Spearman — coiflet relationship is mostly monotonic |

**Key divergence from Spearman:** `32FFT` ranks last in Spearman (max|rho| = 0.353)
but **first in MI (0.506)**.  This means the FFT spectrum has a *non-linear*
relationship with Ra — the FFT captures information that a linear or monotonic
correlation metric cannot detect.  Any model that uses only linear relationships
(Ridge Regression, Linear SVM) will underutilise the FFT features.

`64coif` and `SA` rank high in Spearman but lower in MI, meaning their Ra
relationships are mostly monotonic — a good sign for model interpretability.

### 7.3 Partial Least Squares Regression

**Why:** PLS is a supervised version of PCA — its components explicitly maximise
the covariance with Ra rather than total variance in X.  If PLS produces a good
cross-validated R², it means the feature matrix can predict Ra with a linear model
once the right projection is found.

**Results — 8-fold CV R²:**

| Components | CV R² |
|---|---|
| 1 | −13.7 |
| 2 | **−3.5** (best) |
| 3 | −7.5 |
| ... | all negative |

All R² values are **negative**.  A negative R² means the model performs worse than
simply predicting the mean Ra for every sample — it is less useful than no model
at all.

**Why this happened:** With 768 features and 24 samples, even PLS (which is
specifically designed for p >> n problems) cannot generalise.  Each CV fold trains
on 21 runs and tests on 3.  The model memorises the 21 training points but cannot
transfer to unseen conditions.  This is the strongest possible signal that **the
full 768-dim feature vector cannot be used as-is.**

**PLS loadings (Plot 11):** Despite the poor CV performance, the loadings confirm
that `64coif` and `64mexican` are the primary drivers (consistent with PCA and
Spearman), and that `32FFT` is third.

### 7.4 t-SNE

**Why:** t-SNE is a non-linear dimensionality reduction method that preserves
local neighbourhood structure.  If Ra classes form separable clusters in t-SNE
space but not in PCA space, it confirms that non-linear separation exists and a
non-linear model (kernel SVM, neural network) can exploit it.

**Results (Plot 13):** At both perplexity values (5 and 15), there is partial but
incomplete separation of Ra classes.  Low-Ra samples tend to cluster together in
one region.  High-Ra samples are more dispersed.  This is consistent with the
moderate Spearman correlations (max|rho| = 0.62): the signal is real but not
overwhelmingly strong.

The partial separation confirms a non-linear model is worth trying, but also that
the problem is genuinely hard with this sample size.

---

## 8. Consolidated Findings and What They Mean

### Feature Importance Summary

All four analyses agree on the hierarchy:

1. **`64coif` and `64mexican`** — the CWT wavelet columns are the most Ra-predictive
   features by every metric.  Specific scales (rows 3–6, 11–12, 30–32) are
   particularly important.
2. **`SA` (DWT approximation skewness)** — the highest-ranked statistical feature by
   Spearman.  Row 4 specifically.  Relationship is mostly monotonic.
3. **`32FFT`** — most informative by MI but weakest by Spearman, indicating a
   non-linear relationship between spectral content and Ra.
4. **Remaining DWT stats** (`rmsD`, `crestfactA`, `SD`, `KD`, `KA`, `crestfactD`)
   — moderate correlations, useful but redundant with each other.
5. **`5statistics`** — least informative across all metrics.

### Critical Dataset Constraint

With 24 runs and a 768-dim feature vector, any model using all features will
overfit.  The PLS negative R² demonstrates this conclusively.

**Maximum viable feature vector size:** Given 24 samples and 8-fold CV (3 test runs
per fold), a rule of thumb is to use at most n/5 to n/10 features.  That means
**2–5 features** for classical ML, or at most **20–30 features** with careful
regularisation for a neural network.

### The "First Few Rows" Finding (Confirmed)

The PCA row-importance analysis confirmed that rows 0–9 carry the most signal.
However, Spearman shows that for the wavelet columns, rows 30–32 also have very
high Ra correlation (coiflet energy at mid-to-coarse scales).  The answer is:
- For **DWT statistics** (KA, SA, etc.): rows 0–9, with rows 3–6 being most important
- For **CWT wavelet columns**: both fine scales (rows 3–6) and mid-to-coarse scales (rows 30–32) matter
- For **FFT**: the relationship is non-linear, so it is hard to identify specific rows
  without a non-linear analysis

---

## 9. Model Plan

### Rationale

Based on all analyses, the modelling strategy is:

1. **Reduce features aggressively** before fitting any model
2. **Use the top features identified by Spearman and MI** rather than all 246 valid
   positions or all 768 positions
3. **Validate with leave-one-side-out** (8 folds, one physical side held out per fold)
   to prevent data leakage — windows of the same run must not appear in both train
   and test
4. **Start with classical ML** (Ridge, SVM) as a baseline; add neural networks only
   if baseline performance is promising

### Phase A — Feature-Reduced Classical ML (Next Step)

Select the top K positions by combined Spearman |rho| + MI score.  Fit:
- Ridge Regression (continuous Ra) with 8-fold CV
- SVM-RBF (3-class: Low/Med/High) with 8-fold CV + majority vote across 3 windows

Start with K = 10, 20, 30 and compare.

### Phase B — Feature Image CNN

If Phase A results are promising (R² > 0.3 or accuracy > 60%):
- Build the 64×12 feature image
- Crop to the rows where valid data exists for the top-ranked columns (skip rows 10–29
  where only FFT and wavelet have values, if FFT is not in top-K features)
- Train a shallow CNN (2 conv layers, GlobalAveragePooling, <100K parameters)
- Same 8-fold CV + majority vote

### Phase C — Lightweight Transformer

Based on the literature finding that Transformers outperform CNNs at small scale:
- Treat the 12 feature columns as tokens, each with a fixed-length embedding
- 2-layer Transformer encoder → pooling → output
- Compare directly against Phase B CNN

### Evaluation Metrics

- **Classification:** 3-class accuracy (Low/Med/High) and per-class F1, run-level
  after majority vote across 3 windows
- **Regression:** R² and RMSE on run-level average predictions
- **Baseline to beat:** constant mean prediction (R² = 0 by definition)

---

## 10. File Index

| File | Purpose |
|---|---|
| `data/Side1.xlsx` – `Side8.xlsx` | Pre-extracted feature matrices (9 sheets each) |
| `data/Surface Roughness_Data.xlsx` | Average Ra (µm) for all 24 runs |
| `pca_analysis.py` | Phase 1: PCA dimensionality reduction and feature importance |
| `correlation_analysis.py` | Phase 2: Spearman, Mutual Information, PLS, t-SNE |
| `pca_plots/1_explained_variance.png` | Scree plot — 10 PCs explain 90% variance |
| `pca_plots/2_pc1_pc2_windows.png` | PCA scatter coloured by Ra class (72 windows) |
| `pca_plots/3_pc1_pc2_runs.png` | PCA scatter coloured by continuous Ra (24 runs) |
| `pca_plots/4_loading_heatmaps.png` | PC1–4 loadings reshaped as (64, 12) heatmaps |
| `pca_plots/5_pc_vs_ra.png` | PC score vs Ra scatter for PC1–6 |
| `pca_plots/6_column_importance.png` | Feature column importance via PCA |
| `pca_plots/7_row_importance.png` | Row-index importance via PCA |
| `pca_plots/8_spearman.png` | Spearman rho heatmap and per-column max |rho| |
| `pca_plots/9_mutual_info.png` | Mutual information heatmap and per-column max |
| `pca_plots/10_pls_scores.png` | PLS component scores vs Ra |
| `pca_plots/11_pls_loadings.png` | PLS loadings heatmap (PLS1–4) |
| `pca_plots/12_pls_loo_r2.png` | PLS CV R² vs number of components |
| `pca_plots/13_tsne.png` | t-SNE embedding at perplexity 5 and 15 |

---

## References

- Sun et al. (2025). *Surface roughness classification using stacked signal segment
  images and CNN.* Scientific Reports. PMC11871040.
- Liu et al. (2022). *Milling surface quality prediction: CNN vs Transformer.*
  Sensors. PMC8706467.
- Wang & Oates (2015). *Encoding time series as images.* IJCAI. arXiv:1506.00327.
- Zhao et al. (2024). *Vibration feature extraction + GPR for Ra prediction.*
  Sensors. PMC11014149.
- Qin et al. (2023). *CWT scalogram + multi-scale CNN for tool wear.*
  Sensors. PMC10221429.
