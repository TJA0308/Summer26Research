# End Milling — Raw-Signal CWT Scalograms (`scalograms_raw_10w/`)

A third feature pipeline for End Milling, structurally different from
`scalograms_32x3*`/`scalograms_32x12*` (see `README_32x3.md`): those are
built from precomputed Excel features with only **one real measurement per
run** (their "windows" are row-splits of that single measurement -- see
`build_32x3_features.py`'s docstring). This pipeline goes back to the raw
waveform and derives **real, independent time windows** per run instead --
the single biggest structural gap identified after the first round of
32x3/32x12 results (see the "what can we do to improve accuracy" discussion
in this project's history: recommendation #5).

## Pipeline

1. **`convert_stml_to_csv.py`** -- converts `data/stlml_1.txt`-`stlml_45.txt`
   (LabVIEW STML export) to `data/run1.csv`-`run45.csv` (`time,ai4,ai5,ai6`).
   Originally only handled `stlml_10`-`stlml_45` -> `run1`-`run36`; fixed to
   also cover `stlml_1`-`stlml_9` -> `run37`-`run45`, per README.md's
   run/stlml mapping table.
2. **`build_rawsignal_scalograms.py`** -- reads `data/run{N}.csv`, splits
   each run's ~65,000-sample signal into `--n_windows` real, non-overlapping
   time segments (default 10), and computes a fresh continuous wavelet
   transform (complex/analytic Morlet, `cmor1.5-1.0`) for each window from
   both `ai4` and `ai6` channels, producing a 224x224 RGB PNG per window:
   R = |CWT(ai4)|, G = |CWT(ai6)|, B = 0.

## Honest caveat: `cnn_model/scalogram.py` doesn't exist in this repo

README.md's Pipeline section describes `cnn_model/scalogram.py` as the
script that built the existing `scalograms_ai4_ai6/` -- but that file was
never committed to this checkout (the same situation as `scalogram_hilbert.py`,
already noted missing in `build_residual_scalograms.py`'s docstring). So
`build_rawsignal_scalograms.py` cannot literally reproduce its CWT scale
range -- there is nothing to read.

What WAS verified directly (not assumed) before writing this script, by
inspecting the real `scalograms_ai4_ai6/run1.png`:
- Image size: 224x224 RGB.
- Channel layout: R and G have real, varying pixel content; B is
  **identically zero** across the whole image (checked via numpy min/max).
  This matches Shoulder Milling's own documented Option A analogy table for
  End Milling (`Shoulder Milling/plot_option_a.py`'s comparison table):
  R = CWT(ai4), G = CWT(ai6), B = unused. Reproduced exactly.

What was NOT recoverable and is a fresh, documented choice instead of a
silent guess:
- **Wavelet**: complex ("analytic") Morlet, `cmor1.5-1.0` -- matches
  README's "analytic Morlet CWT" wording; PyWavelets' plain `'morl'` is
  real-valued, not analytic.
- **Frequency range**: 20-4000 Hz, `--n_scales` log-spaced scales (default
  128). Lower bound excludes near-DC drift; upper bound is half the
  ~8196 Hz Nyquist, covering spindle rotation frequencies (25-83 Hz for
  1500-5000 rpm), tooth-passing frequencies and harmonics, and into the
  low-kHz chatter/tool-wear range, without the noisiest top octave near
  Nyquist.
- **Normalisation**: `|CWT|` magnitude, `log1p`-compressed, min-max scaled
  to `[0, 255]` independently per window per channel.

These are reasonable, physically-motivated defaults, not a verified
reproduction -- flagged here per this repo's existing convention of not
silently assuming an unrecoverable original was matched.

## Usage

```bash
cd "End Milling"
python convert_stml_to_csv.py              # data/stlml_*.txt -> data/run*.csv
python build_rawsignal_scalograms.py        # -> scalograms_raw_10w/ (450 PNGs)

# Variants:
python build_rawsignal_scalograms.py --n_windows 5
python build_rawsignal_scalograms.py --n_scales 64 --f_min 10 --f_max 2000
```

`data/run*.csv` are NOT committed (regeneratable from `stlml_*.txt` in
~seconds; same reasoning `data/` itself was excluded from earlier commits --
size, not sensitivity).

## Not yet done

This script only builds the base scalogram images. It does not yet have:
- A training script (would need the same `--target` label wiring as
  `cnn_model/cnn_train.py`/`cnn_train_32x3.py`, but images are already
  224x224 so no Resize-focused rewrite is needed -- `cnn_model/cnn_train.py`
  itself, already built for `scalograms_10w`-style directories, should work
  directly against `scalograms_raw_10w/` once labels are confirmed to line
  up, since it already keys everything off `run{N}_w{K}.png` filenames).
- SMOTE, residual correction, or PCA analogs for this pipeline.
- Any comparison against the existing `scalograms_10w`/`scalograms_ai4_ai6`
  outputs to check whether this specific CWT parameterisation (vs whatever
  the original, now-missing `scalogram.py` used) changes results.

Nothing here has been trained.
