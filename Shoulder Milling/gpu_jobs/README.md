# gpu_jobs -- LOCO-CV follow-up runs (Windows GPU machine)

Scripts `cd` to `Shoulder Milling/` themselves. They need `cv_evaluate.py` with the `--out_csv` flag
(added by another workstream) and the `scalograms_*` folders. Each job skips if its output CSV already exists, so reruns resume.
Bash (Git Bash/WSL) and PowerShell versions are equivalent (`.sh` / `.ps1`).

## Run order
1. `00_repro_check` -- doc, 32x12_residual_doc, seed 42, lr 1e-3. Must give run_acc_soft 0.9583 (95.8%); exits nonzero otherwise. STOP if it fails.
2. `A_missing_lr1e-4` -- unmatched cells from `python find_missing_runs.py`. Finding: all 48 section-4 cells already match
   (lr=1e-4 rows exist in cv_summary.csv, some with blank lr, some explicit), so no lr=1e-4 reruns are needed.
   The one gap found: roughness/secondary/32x12_feedopt_9win has no lr=1e-3 row, so batch A runs that single cell.
3. `B_multiseed` -- seeds 43 44 45 46, lr 1e-3, resnet18, 50 epochs:
   speed 32x12_9win; doc 32x12_residual_doc; feed 32x3_residual_roughness; roughness 32x12_feedopt_9win (`--roughness_group primary`).
4. `C_nested_preproc` -- fold-nested preprocessing (`--preproc`), resnet18, 50 epochs, lr 1e-3, seeds 42 43 44 45 46
   (new variants, so seed 42 is not a selection seed). Needs `fullscale_cwt/` (feedopt_nested). Uses the 72-window dirs
   (`*_9win` dirs have ragged image widths, unsupported by nested preprocessing). Jobs:
   - `feedopt_nested`: feed on `scalograms_32x3_feedopt`; roughness (primary) on `scalograms_32x12_feedopt`
     (feedopt scale selection is against feed, as in the legacy feedopt dirs; not run for speed/doc, whose configs are not feedopt).
   - `residual_inductive`: speed, doc, roughness (primary) on `scalograms_32x12`; feed on `scalograms_32x3`.
5. `run_all` runs 1-4 in sequence.

**Reading batch C:** `residual_inductive` does NOT remove the held-out factor's group effect (by design: a nuisance level
absent from the training fold, e.g. the whole held-out doc level for the doc/speed folds, gets effect 0 and is left in). The
legacy residual variants instead centre each test group on its own mean (transductive), which is why they score higher.
Expect lower numbers from `residual_inductive`; that lower figure is the honest, leak-free one. Report it as a different
method, never as the legacy residual number. Smoke test (CPU, hgb, seed 42, LOCO): doc/32x3 none 0.583 vs residual_inductive 0.333.

## Expected output
| Batch | CSV files | cnn rows |
|---|---|---|
| repro | 1 | 1 |
| A | 1 | 1 |
| B | 4 (`cv_runs/B/<target>__<scalogram>__lr1e-3__s43-44-45-46.csv`) | 4 each = 16 |
| C | 6 (`cv_runs/C/<target>__<scalogram>__<preproc>__lr1e-3__s42-46.csv`) | 5 each = 30 |

Total 48 rows. Naming: `cv_runs/<batch>/<target>__<scalogram>__lr<lr>__s<seeds>.csv`.

## Runtime estimate
Based on run_loco_32x12.sh (~1 h on a T4 for ~15 target-seed LOCO sweeps): about 4-6 min per (config, seed) on a T4.
Repro ~5 min, A ~5 min, B 16 seed-runs ~65-100 min. C: 30 seed-runs ~2-3 h (per-fold fit adds seconds). Roughly 4-5 h total on a T4.

## Merge
Copy `cv_runs/` back to `Shoulder Milling/` and run:

    python merge_cv_runs.py

(script from another workstream, not yet present at time of writing). Then re-check with `python find_missing_runs.py`.


