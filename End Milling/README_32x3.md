# End Milling — 32x3 Feature-Image Pipeline

A second feature representation for End Milling, built to mirror Shoulder
Milling's Option D scalograms (`Shoulder Milling/build_option_d_scalograms.py`
-> `scalograms_32x3/`) and every downstream procedure that was run on top of
it there: SMOTE, condition-residual preprocessing, 9-window majority voting,
cascade conditioning, and PCA diagnostics.

Source data: `data/STLMILAE_DOC{015,03,06}.xlsx` -- confirmed by direct
inspection to have the identical 12-column precomputed feature schema
Shoulder Milling uses (`32FFT, 5statistics, 64mexican, 64coif, KA, SA, KD,
SD, rmsA, rmsD, crestfactA, crestfactD`), one workbook per DOC level, 15
sheets each (`s{speed}f{feed}`), 45 sheets total = all 45 runs. So the FFT/
CWT numbers are **read directly**, exactly like Option D, not recomputed
from the raw waveform.

## Why "windows" here are a row-split, not a real re-window

Shoulder Milling's 3 windows/run (a/b/c) were 3 separate real measurement
sheets that existed before any row-splitting; only its `_9win` variant
(`split_scalogram_windows.py`) is a post-hoc split, done because by that
point there was no raw waveform left to re-derive real windows from.

End Milling's precomputed sheets are **one block per run** -- there's no
separate real per-run window granularity to start from here either. So both
the 3-window baseline and the 9-window variant are produced the same way:
split the final (32, 3) image's 32-row axis into `--n_windows` row-blocks
(`np.array_split` -- deterministic sizes, e.g. 3 -> `[11,11,10]` rows, 9 ->
`[4,4,4,4,4,3,3,3,3]` rows), each block saved as one training sample. This
replicates Shoulder Milling's sample-count structure (3x/9x more windows
than runs) -- it is not a claim that these are independent real
measurements the way Shoulder Milling's a/b/c windows were.

## Files

| File | Purpose |
|---|---|
| `build_32x3_features.py` | Reads the precomputed Excel columns, selects top-32-of-64 CWT scales by Spearman \|rho\|, writes the 32x3 PNGs (row-split into `--n_windows` blocks) + `labels.csv` + `selected_scales.json` + `features_raw.npz` (per-window blocks) + `run_features_raw.npz` (full per-run 32x3 arrays) |
| `smote_generate_32x3.py` | Persisted whole-run SMOTE synthesis (k-NN interpolation), one CSV+PNGs per target |
| `build_residual_scalograms.py` | **Reused unmodified** -- already generic over any `run{N}_w{K}.png` directory; subtracts the per-(DOC,speed)-condition mean |
| `predict_conditioning_32x3.py` | Runs a trained speed/doc model over all windows, writes `<target>_pred_32x3....csv` for the leakage-honest cascade |
| `cnn_model/cnn_train_32x3.py` | Training entry point: 4 targets, SMOTE auto-load, `--conditioned` (ground-truth cascade) and `--cascade_predicted` (predicted-parent cascade) |
| `pca_analysis_32x3.py` | 7-plot PCA diagnostic suite on the final (post-selection) 32x3 feature space, one sample per run |

## Generated scalograms (already committed)

The 3-window baseline and 9-window variants for both scale-selection targets
have been generated and committed:

```
scalograms_32x3/                    -- roughness-tuned, 3 windows/run (135 samples)
scalograms_32x3_feedopt/            -- feed_coarse-tuned, 3 windows/run
scalograms_32x3_9win/               -- roughness-tuned, 9 windows/run (405 samples)
scalograms_32x3_feedopt_9win/       -- feed_coarse-tuned, 9 windows/run
```

Each contains: `run{N}_w{K}.png`, `labels.csv`, `selected_scales.json`,
`features_raw.npz`, `run_features_raw.npz`.

## Full command list (run these next, in order)

Order matters between residual and SMOTE: `build_residual_scalograms.py`
skips any file whose run id isn't a real run, so it silently ignores SMOTE
synthetic images already sitting in the same folder -- a `_residual*`
directory never inherits synthetic images generated afterward. Build
residual first if you want both.

```bash
cd "End Milling"

# 1. Condition-residual preprocessing (subtract per DOC x speed group mean)
python build_residual_scalograms.py --target roughness   --src_dirs scalograms_32x3 scalograms_32x3_9win
python build_residual_scalograms.py --target feed_coarse --src_dirs scalograms_32x3_feedopt scalograms_32x3_feedopt_9win

# 2. Persisted SMOTE (per variant, all targets)
python smote_generate_32x3.py --img_dir scalograms_32x3
python smote_generate_32x3.py --img_dir scalograms_32x3_feedopt
python smote_generate_32x3.py --img_dir scalograms_32x3_9win
python smote_generate_32x3.py --img_dir scalograms_32x3_feedopt_9win

# 3. PCA charts
python pca_analysis_32x3.py --img_dir scalograms_32x3         --target roughness
python pca_analysis_32x3.py --img_dir scalograms_32x3_feedopt --target feed_coarse

# 4. Train (plain, per target/arch/lr -- repeat over archs as desired:
#    resnet18, resnet50, efficientnet_b0, convnext_tiny, mobilenet_v3_large)
python cnn_model/cnn_train_32x3.py --target speed       --img_dir scalograms_32x3          --arch resnet18
python cnn_model/cnn_train_32x3.py --target doc         --img_dir scalograms_32x3          --arch resnet18
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt  --arch resnet18
python cnn_model/cnn_train_32x3.py --target roughness   --img_dir scalograms_32x3_residual_roughness --arch resnet18

# 5a. Cascade (ground-truth shortcut, upper bound)
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --conditioned

# 5b. Cascade (leakage-honest, predicted parents)
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch resnet18
python cnn_model/cnn_train_32x3.py --target doc   --img_dir scalograms_32x3_feedopt --arch resnet18
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_feedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_feedopt
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --cascade_predicted

# 6. Repeat steps 4/5 with --img_dir pointed at the _9win variants
#    (scalograms_32x3_9win / scalograms_32x3_feedopt_9win) for the
#    9-window majority-vote comparison -- voting across windows happens
#    automatically inside cnn_train_32x3.py.
```

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
  3-4-row fragments destroy too much per-window signal to be useful --
  compare against the 3-window baseline once both are trained.
