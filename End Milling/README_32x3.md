# End Milling — 32x3 / 32x12 Feature-Image Pipelines

Two feature representations for End Milling, built to mirror Shoulder
Milling's Option D (`scalograms_32x3/`) and Option C (`scalograms_32x12/`)
scalograms, and every downstream procedure that was run on top of them
there: SMOTE, condition-residual preprocessing, 9-window majority voting,
cascade conditioning, and PCA diagnostics.

Source data: `data/STLMILAE_DOC{015,03,06}.xlsx` -- confirmed by direct
inspection to have the identical 12-column precomputed feature schema
Shoulder Milling uses (`32FFT, 5statistics, 64mexican, 64coif, KA, SA, KD,
SD, rmsA, rmsD, crestfactA, crestfactD`), one workbook per DOC level, 15
sheets each (`s{speed}f{feed}`), 45 sheets total = all 45 runs. So the FFT/
CWT numbers are **read directly** in both pipelines, exactly like Options
C/D, not recomputed from the raw waveform.

## The two layouts

- **32x3** (`build_32x3_features.py`, Option D analog): col 0 = 32FFT
  (native, complete), col 1 = top-32-of-64 selected `64mexican` rows, col 2
  = the same selected `64coif` rows.
- **32x12** (`build_32x12_features.py`, Option C analog): all 12 columns.
  The two CWT columns use the same selected rows as 32x3; every other
  column is naturally truncated to its first 32 rows (already zero beyond
  its real length -- 32FFT has 32 real values, `5statistics` has 6, the 8
  DWT-stat columns have 10 each, confirmed by inspection, not assumed).

Both share loading/scale-selection/windowing code in `em_feature_common.py`
so they never disagree about run->sheet mapping or which 32 scales were
selected for a given target.

## Why "windows" here are a row-split, not a real re-window

Shoulder Milling's 3 windows/run (a/b/c) were 3 separate real measurement
sheets that existed before any row-splitting; only its `_9win` variant
(`split_scalogram_windows.py`) is a post-hoc split, done because by that
point there was no raw waveform left to re-derive real windows from.

End Milling's precomputed sheets are **one block per run** -- there's no
separate real per-run window granularity to start from here either. So both
the 3-window baseline and the 9-window variant are produced the same way:
split the final 32-row image's row axis into `--n_windows` row-blocks
(`np.array_split` -- deterministic sizes, e.g. 3 -> `[11,11,10]` rows, 9 ->
`[4,4,4,4,4,3,3,3,3]` rows), zero-padded to a uniform size, each block saved
as one training sample. This replicates Shoulder Milling's sample-count
structure (3x/9x more windows than runs) -- it is not a claim that these are
independent real measurements the way Shoulder Milling's a/b/c windows were.

## Files

| File | Purpose |
|---|---|
| `em_feature_common.py` | Shared Excel loading, run/label wiring, CWT scale selection, normalize+window+write logic used by both builders |
| `build_32x3_features.py` | Option D analog (3 columns) |
| `build_32x12_features.py` | Option C analog (12 columns) |
| `smote_generate_32x3.py` | Persisted whole-run SMOTE synthesis (k-NN interpolation). Column-count-agnostic, and falls back to SMOTE-ing directly on pixel values when `features_raw.npz`/`selected_scales.json` don't exist (residual dirs) -- serves all three (base, feedopt, residual) x both pipelines with no flag needed |
| `build_residual_scalograms.py` | **Reused unmodified** -- already generic over any `run{N}_w{K}.png` directory; subtracts the per-(DOC,speed)-condition mean. Only ever writes PNGs (no `labels.csv`/`features_raw.npz`/`selected_scales.json`) |
| `predict_conditioning_32x3.py` | Runs a trained speed/doc model over all windows (globs PNGs directly, no `labels.csv` dependency -- works on residual dirs too), writes `<target>_pred_<scalo_tag>....csv` for the leakage-honest cascade |
| `cnn_model/cnn_train_32x3.py` | Training entry point: 4 targets, SMOTE auto-load, `--conditioned` (ground-truth cascade), `--cascade_predicted` (predicted-parent cascade). Its plain-training path (`load_split`) globs PNGs directly too -- always worked on residual dirs even before the SMOTE/predict fixes above |
| `pca_analysis_32x3.py` | 7-plot PCA diagnostic suite. Reads column names/count from `selected_scales.json`, so it works unmodified on either pipeline (not run on residual dirs -- those have no `run_features_raw.npz` either, and residual-correcting is a training-time concern, not a feature-space one) |
| `run_sweep_32xN.ps1` | Trains all 4 targets x 4 backbones x 2 LRs x with/without SMOTE, across both layouts and both window variants (256 runs) |
| `run_sweep_cascade.ps1` | feed_coarse cascade sweep: ground-truth `--conditioned` + the full speed/doc -> predict -> `--cascade_predicted` chain |
| `run_sweep_residual.ps1` | Same grid as `run_sweep_32xN.ps1` but for the 8 residual-corrected dirs (roughness x 4 dirs, feed_coarse x 4 dirs) + ground-truth `--conditioned` on the feed_coarse residual dirs (160 runs total) |
| `residual_all_commands.txt` | The same 160 commands `run_sweep_residual.ps1` runs, as a flat, human-readable list |

## Is it running all four backbones with/without SMOTE?

**Not automatically per single command** -- each `cnn_train_32x3.py`
invocation trains exactly one (target, arch, lr, SMOTE-setting) combination;
arch and lr are already baked into the output filename
(`models_<target>_<scalo_tag>/<arch>_lr<lr>[_<run_tag>]_best.pt`), and
`--no_smote` toggles SMOTE off (on by default when a `smote_*.csv` exists).
**`run_sweep_32xN.ps1` is what makes "yes" true** -- run that one script and
it loops over all 4 backbones x 2 LRs x with/without SMOTE x 4 targets x
both layouts x both window variants (256 total training runs). Narrow the
`$Layouts` / `$WinVariants` arrays at the top of the script if you want a
smaller slice first.

## Generated scalograms (already committed)

```
scalograms_32x3/                     -- roughness-tuned, 3 windows/run (135 samples)
scalograms_32x3_feedopt/             -- feed_coarse-tuned, 3 windows/run
scalograms_32x3_9win/                -- roughness-tuned, 9 windows/run (405 samples)
scalograms_32x3_feedopt_9win/        -- feed_coarse-tuned, 9 windows/run
scalograms_32x3_residual_roughness/  -- residual-corrected roughness variant
scalograms_32x3_9win_residual_roughness/
scalograms_32x3_feedopt_residual/    -- residual-corrected feed_coarse variant
scalograms_32x3_feedopt_9win_residual/

scalograms_32x12/                    -- same 4 base variants, 12-column layout
scalograms_32x12_feedopt/
scalograms_32x12_9win/
scalograms_32x12_feedopt_9win/
scalograms_32x12_residual_roughness/
scalograms_32x12_9win_residual_roughness/
scalograms_32x12_feedopt_residual/
scalograms_32x12_feedopt_9win_residual/
```

Each `scalograms_32x{3,12}*` directory (non-residual) contains:
`run{N}_w{K}.png`, `labels.csv`, `selected_scales.json`, `features_raw.npz`,
`run_features_raw.npz`, and (after the SMOTE step) `smote_*_labels.csv` +
synthetic `smote<target><i>_w{K}.png` files. PCA charts are in
`pca_plots_scalograms_32x3/`, `pca_plots_scalograms_32x3_feedopt/`,
`pca_plots_scalograms_32x12/`, `pca_plots_scalograms_32x12_feedopt/`.

Each `scalograms_32x{3,12}*_residual*` directory contains only
`run{N}_w{K}.png` (from `build_residual_scalograms.py`) plus, after the
SMOTE step, `smote_<target>_labels.csv` + synthetic PNGs (`target` is
`roughness` or `feed_coarse`, whichever that residual dir was built for) --
no `labels.csv`/`features_raw.npz`/`selected_scales.json`; every script that
touches these dirs was written or patched to not need them (see Files
table above).

## Run everything at once

```bash
cd "End Milling"

# Plain training sweep: all 4 targets x 4 backbones x 2 LRs x with/without
# SMOTE, across 32x3/32x12 and 3win/9win (256 runs)
powershell -File run_sweep_32xN.ps1

# feed_coarse cascade sweep: ground-truth --conditioned + the leakage-honest
# speed/doc -> predict_conditioning_32x3.py -> --cascade_predicted chain
powershell -File run_sweep_cascade.ps1

# Residual-corrected training: same grid, on the 8 residual dirs, plus
# ground-truth --conditioned for feed_coarse's 4 residual dirs (160 runs)
powershell -File run_sweep_residual.ps1
```

`residual_all_commands.txt` has the same 160 commands `run_sweep_residual.ps1`
runs, spelled out one per line, if you'd rather run them individually or in
parallel batches instead of through the script.

## Open questions to check once trained

- Does condition-residual preprocessing recover feed_coarse/roughness here
  the way it did for Shoulder Milling (see `Shoulder Milling/writeup.md`),
  or does it behave differently given End Milling's feature source is a
  single measurement per run rather than 3 independent windows?
- Does the leakage-honest `--cascade_predicted` cascade hold up as well as
  the ground-truth `--conditioned` shortcut, or does it reveal the same kind
  of inflation Shoulder Milling found when it moved from ad-hoc validation
  to leave-one-side-out CV?
- Does the 9-window (row-split-into-9) variant actually help majority-vote
  accuracy, or does splitting an already-narrow 32-row image into
  3-4-row fragments destroy too much per-window signal to be useful?
- Does 32x12 (all features) outperform 32x3 (FFT/mexican/coif only), or do
  the extra 9 columns (mostly zero beyond row 5-9, per the PCA column-
  importance plots) just add noise for the CNN to ignore?
