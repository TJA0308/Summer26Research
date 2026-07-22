# End Milling — Raw-Window Engineered Feature Set (`scalograms_*_raw{n}w/`)

A fourth feature pipeline for End Milling. Combines the engineered 32x3/32x12
column layout from `build_32x3_features.py`/`build_32x12_features.py` (see
`README_32x3.md`) with genuinely independent time windows from the raw
waveform (see `README_RAWSIGNAL.md`), instead of either:
- reading one precomputed Excel measurement and row-splitting it into
  artificial "windows" (`scalograms_32x3*`/`scalograms_32x12*`), or
- building a plain CWT-image scalogram with no engineered feature columns
  (`scalograms_raw_10w`).

Every window here is a real, non-overlapping slice of `data/run{N}.csv`,
freshly put through the same FFT/CWT/DWT computation Shoulder Milling and
the Excel-based pipeline use — see `rawwindow_feature_common.py` for the
column semantics and caveats (coiflet-CWT approximation, db4 DWT choice).

## Pipeline

1. **`build_rawwindow_features.py --target {roughness,feed_coarse,speed,doc}
   --layout {32x3,32x12} --n_windows {3,9}`** — computes per-window
   FFT/mexican/coif/DWT/time-domain features from `data/run{N}.csv`, selects
   the top-32-of-64 CWT scale rows for the given target (same Spearman-|rho|
   method as `em_feature_common.select_cwt_rows`, but run-level-averaged
   across each run's real windows first), and writes
   `scalograms_<layout>[_feedopt|_speedopt|_docopt]_raw<n>w/` with the same
   file schema as the Excel-based pipeline (`labels.csv`,
   `selected_scales.json`, `features_raw.npz`, `run_features_raw.npz`,
   `run{N}_w{K}.png`) — a drop-in replacement, no downstream code changes.
2. **`build_residual_scalograms.py --target {feed_coarse,roughness} --src_dirs
   ...`** — unmodified, existing script; condition-residual correction for
   feed_coarse/roughness only (speed/doc already near-100% on raw features).
3. **`smote_generate_32x3.py --img_dir ...`** / **`pca_analysis_32x3.py
   --img_dir ... --target ...`** — unmodified, existing scripts; both are
   column-count- and schema-agnostic, so they run directly against the new
   directories.

All 16 `--target`x`--layout`x`--n_windows` combinations were generated, then
residual variants for `feed_coarse` (on the 4 `_feedopt_raw{n}w` dirs) and
`roughness` (on the 4 base `_raw{n}w` dirs), then SMOTE (all 24 resulting
dirs) and PCA (the 16 base dirs, one target each matching the dir's
`TARGET_DIR_SUFFIX`).

## Usage

```bash
cd "End Milling"
python convert_stml_to_csv.py    # data/stlml_*.txt -> data/run*.csv (if not already done)

# 16 combinations:
for target in roughness feed_coarse speed doc; do
  for layout in 32x3 32x12; do
    for n in 3 9; do
      python build_rawwindow_features.py --target $target --layout $layout --n_windows $n
    done
  done
done

# residuals
python build_residual_scalograms.py --target feed_coarse --src_dirs scalograms_32x3_feedopt_raw3w scalograms_32x3_feedopt_raw9w scalograms_32x12_feedopt_raw3w scalograms_32x12_feedopt_raw9w
python build_residual_scalograms.py --target roughness   --src_dirs scalograms_32x3_raw3w scalograms_32x3_raw9w scalograms_32x12_raw3w scalograms_32x12_raw9w

# SMOTE (all 24 dirs) + PCA (the 16 base dirs)
python smote_generate_32x3.py --img_dir <dir>
python pca_analysis_32x3.py --img_dir <base_dir> --target <roughness|feed_coarse|speed|doc>
```

`data/run*.csv` are not committed (regeneratable from `stlml_*.txt` in
seconds — same reasoning `data/` itself is excluded elsewhere in this repo).

## Not yet done

No training has been run against these directories. `cnn_train_32x3.py`
should work unmodified once pointed at a `scalograms_*_raw{n}w[_residual...]`
directory, since the file schema is identical to the Excel-based pipeline's
— not yet verified end-to-end.
