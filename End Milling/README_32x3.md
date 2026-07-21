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

## Every target gets its own scale selection

Originally only `roughness` (default) and `feed_coarse` (`_feedopt`) had
dedicated top-32-of-64 scale selections; `speed` and `doc` just trained on
whichever of those two was passed as `--img_dir`. `compare_scale_selection.py`
tested whether that was actually fine, by computing each target's OWN true
top-32 ranking and checking how well roughness's/feed_coarse's selections
would have scored if repurposed:

| Existing selection | vs speed | vs doc |
|---|---|---|
| roughness's top-32   | 10/32 rows overlap, **86.7%** efficiency | 13/32 rows overlap, **93.2%** efficiency |
| feed_coarse's top-32 | 26/32 rows overlap, **98.7%** efficiency | 21/32 rows overlap, **94.9%** efficiency |

("Efficiency" = mean |Spearman rho| of that target's own score function over
the existing 32 rows, divided by the mean over that target's true best 32
rows -- 100% would mean the existing selection is already optimal.)

Roughness's selection left real signal on the table for both speed and doc
(worst case: only 86.7% as good as a dedicated selection, barely more than
half the rows even overlapping). Feed_coarse's selection happened to be
decent for speed but not doc. Conclusion: dedicated `_speedopt`/`_docopt`
selections are worth having, not just tidiness -- `scalograms_32x{3,12}_
speedopt/` and `_docopt/` (plus their `_9win` variants) now exist and
`run_sweep_32xN.ps1`/`run_sweep_32xN_detailed.ps1` route speed/doc training
to them instead of the base or feedopt dirs.

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
| `compare_scale_selection.py` | Test: quantifies overlap/efficiency between each target's own top-32 scale selection and every other target's -- see "Every target gets its own scale selection" above |
| `build_32x3_features.py` | Option D analog (3 columns). `--target` in `{roughness, feed_coarse, speed, doc}` |
| `build_32x12_features.py` | Option C analog (12 columns). Same 4 `--target` values |
| `smote_generate_32x3.py` | Persisted whole-run SMOTE synthesis (k-NN interpolation). Column-count-agnostic, and falls back to SMOTE-ing directly on pixel values when `features_raw.npz`/`selected_scales.json` don't exist (residual dirs) -- serves all three (base, feedopt, residual) x both pipelines with no flag needed |
| `build_residual_scalograms.py` | **Reused unmodified** -- already generic over any `run{N}_w{K}.png` directory; subtracts the per-(DOC,speed)-condition mean. Only ever writes PNGs (no `labels.csv`/`features_raw.npz`/`selected_scales.json`) |
| `predict_conditioning_32x3.py` | Runs a trained speed/doc model over all windows (globs PNGs directly, no `labels.csv` dependency -- works on residual dirs too), writes `<target>_pred_<scalo_tag>....csv` for the leakage-honest cascade |
| `cnn_model/cnn_train_32x3.py` | Training entry point: 4 targets, SMOTE auto-load, `--conditioned`/`--cascade_predicted` (feed_coarse **or roughness** cascade), `--kfold N` (stratified CV instead of one fixed split). Reports run-level accuracy two ways: hard majority vote and soft probability-averaging |
| `pca_analysis_32x3.py` | 7-plot PCA diagnostic suite. Reads column names/count from `selected_scales.json`, so it works unmodified on either pipeline (not run on residual dirs -- those have no `run_features_raw.npz` either, and residual-correcting is a training-time concern, not a feature-space one) |
| `run_sweep_32xN.ps1` | Trains all 4 targets x 4 backbones x 2 LRs x with/without SMOTE, across both layouts and both window variants (256 runs) -- loop-based |
| `run_sweep_cascade.ps1` | Cascade sweep for feed_coarse (on `_feedopt` dirs) AND roughness (on base dirs): ground-truth `--conditioned` + the full speed/doc -> predict -> `--cascade_predicted` chain (272 runs) -- loop-based |
| `run_sweep_residual.ps1` | Same grid as `run_sweep_32xN.ps1` but for the 8 residual-corrected dirs (roughness x 4 dirs, feed_coarse x 4 dirs) + ground-truth `--conditioned` for BOTH targets' residual dirs (192 runs) -- loop-based |
| `run_sweep_32xN_detailed.ps1` | The same 256 commands as `run_sweep_32xN.ps1`, spelled out one line each (no loops) -- for reading/auditing/copy-pasting individual lines |
| `run_sweep_cascade_detailed.ps1` | The same 272 commands as `run_sweep_cascade.ps1`, spelled out flat |
| `run_sweep_residual_detailed.ps1` | The same 192 commands as `run_sweep_residual.ps1`, spelled out flat |
| `run_everything_detailed.ps1` | All 720 commands from the three `_detailed.ps1` files above, concatenated into one file/one run |

The `_detailed.ps1` files and the loop-based files run the identical grid --
pick whichever you'd rather work with. The detailed ones are plain
`python ...` lines with a 2-line PowerShell header, so they're just as
copy-paste-able into a plain shell as a `.txt` would be.

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
scalograms_32x3_speedopt/            -- speed-tuned, 3 windows/run
scalograms_32x3_docopt/              -- doc-tuned, 3 windows/run
scalograms_32x3_9win/                -- roughness-tuned, 9 windows/run (405 samples)
scalograms_32x3_feedopt_9win/        -- feed_coarse-tuned, 9 windows/run
scalograms_32x3_speedopt_9win/       -- speed-tuned, 9 windows/run
scalograms_32x3_docopt_9win/         -- doc-tuned, 9 windows/run
scalograms_32x3_residual_roughness/  -- residual-corrected roughness variant
scalograms_32x3_9win_residual_roughness/
scalograms_32x3_feedopt_residual/    -- residual-corrected feed_coarse variant
scalograms_32x3_feedopt_9win_residual/

scalograms_32x12/                    -- same 8 non-residual variants, 12-column layout
scalograms_32x12_feedopt/
scalograms_32x12_speedopt/
scalograms_32x12_docopt/
scalograms_32x12_9win/
scalograms_32x12_feedopt_9win/
scalograms_32x12_speedopt_9win/
scalograms_32x12_docopt_9win/
scalograms_32x12_residual_roughness/
scalograms_32x12_9win_residual_roughness/
scalograms_32x12_feedopt_residual/
scalograms_32x12_feedopt_9win_residual/
```

(No residual variants for `_speedopt`/`_docopt`: speed/doc were excluded from
condition-residual correction from the start -- see
`build_residual_scalograms.py`'s docstring -- they already hit ~100% on raw
features, so there's nothing for residual correction to rescue.)

Each `scalograms_32x{3,12}*` directory (non-residual) contains:
`run{N}_w{K}.png`, `labels.csv`, `selected_scales.json`, `features_raw.npz`,
`run_features_raw.npz`, and (after the SMOTE step) `smote_*_labels.csv` +
synthetic `smote<target><i>_w{K}.png` files. PCA charts (`--target` matching
each dir's own scale-selection target) are in `pca_plots_scalograms_32x3/`,
`pca_plots_scalograms_32x3_feedopt/`, `pca_plots_scalograms_32x3_speedopt/`,
`pca_plots_scalograms_32x3_docopt/`, and the same four for `32x12`.

Each `scalograms_32x{3,12}*_residual*` directory contains only
`run{N}_w{K}.png` (from `build_residual_scalograms.py`) plus, after the
SMOTE step, `smote_<target>_labels.csv` + synthetic PNGs (`target` is
`roughness` or `feed_coarse`, whichever that residual dir was built for) --
no `labels.csv`/`features_raw.npz`/`selected_scales.json`; every script that
touches these dirs was written or patched to not need them (see Files
table above).

## Run everything at once

Loop-based (compact, same grid):

```bash
cd "End Milling"

powershell -File run_sweep_32xN.ps1       # plain training: 256 runs
powershell -File run_sweep_cascade.ps1    # feed_coarse + roughness cascade: 272 runs
powershell -File run_sweep_residual.ps1   # residual-corrected: 192 runs
```

Or the flat, fully-spelled-out equivalents (every one of the 720 commands
visible, nothing hidden behind a loop) -- either run each phase separately
or run all 720 in one shot:

```bash
cd "End Milling"

powershell -File run_sweep_32xN_detailed.ps1
powershell -File run_sweep_cascade_detailed.ps1
powershell -File run_sweep_residual_detailed.ps1

# -- or, all three phases in one file --
powershell -File run_everything_detailed.ps1
```

Every `_detailed.ps1` file is plain `python ...` lines (with just a 2-line
PowerShell header), grouped under `#` section comments per target/layout/
window-variant -- open any of them if you just want to read or copy-paste
the commands rather than run the file.

`--kfold` is deliberately NOT part of any sweep script -- running full CV
across every arch/lr/smote/target/layout combo (5x the already-large grid)
isn't worth it as a blanket default. Run it standalone per target/config you
actually want to trust, e.g.:

```bash
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet50 --kfold 5
python cnn_model/cnn_train_32x3.py --target speed     --img_dir scalograms_32x3_speedopt           --arch resnet18 --kfold 5
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet50 --kfold 5
python cnn_model/cnn_train_32x3.py --target doc       --img_dir scalograms_32x3_docopt             --arch resnet18 --kfold 5
```

## Three additions from the first results round

The first full sweep's results (256+136+160 runs) prompted three follow-ups,
all now implemented in `cnn_model/cnn_train_32x3.py`:

1. **Soft (probability-averaging) run-level accuracy**, reported alongside
   the existing hard majority vote for every training run, no flag needed.
   Saved in each run's history JSON as `run_level_soft_acc` (majority vote
   stays `run_level_acc`, unchanged, so `predict_conditioning_32x3.py`'s
   best-model selection is unaffected).
2. **Cascade conditioning extended to roughness**, not just feed_coarse
   (`COND_PARENTS` now covers both). Roughness shares feed_coarse's exact
   DOC x speed nuisance covariate -- it's the reason residual correction
   helps both -- so it was always a legitimate cascade candidate; it just
   hadn't been tried. `run_sweep_cascade.ps1`/`run_sweep_residual.ps1` (and
   their detailed counterparts) now cover it.
3. **`--kfold N`**: stratified N-fold CV instead of one fixed split, reusing
   cnn_train.py's own `stratified_kfold`/`load_smote_full`/`smote_for_fold`.
   Plain training only (not compatible with cascade flags). This is the
   check for whether any given number is trustworthy or just a lucky/
   unlucky split -- see Shoulder Milling's own feed-rate story in the module
   docstring for why this matters.

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
