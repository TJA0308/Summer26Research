# Batch D: re-run the README's best configs WITH per-window predictions saved, so precision /
# recall / F1 can be computed (compute_prf1.py). lr 1e-3, resnet18, 50 epochs, LOCO.
#   Block 1: best-of-16 per target (seed 42) + the two "best without residual" configs.
#   Block 2: plain 32x12 baseline (seeds 42-46) = the generalization counterpart.
# A GPU re-run may not reproduce the seed-42 accuracies in cv_summary.csv bit-for-bit; the README
# must quote the accuracy from THIS run next to its P/R/F1 and note any difference.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$batch = "D"
New-Item -ItemType Directory -Force "cv_runs/$batch", "cv_preds/cnn" | Out-Null

function Run-Job($t, $s, [int[]]$seeds) {
  $tag = ($seeds -join "-")
  $out = "cv_runs/$batch/${t}__${s}__lr1e-3__s$tag.csv"
  if ((Test-Path $out) -and (Get-Item $out).Length -gt 0) { "skip $out"; return }
  $extra = @(); if ($t -eq "roughness") { $extra = @("--roughness_group", "primary") }
  python cv_evaluate.py --img_dir "scalograms_$s" --target $t --split loco @extra `
    --models cnn --arch resnet18 --epochs 50 --lr 1e-3 --seeds @seeds `
    --save_preds cv_preds/cnn --out_csv $out
  if ($LASTEXITCODE) { throw "job failed: $t $s" }
}

# Block 1: best configs, seed 42
Run-Job speed     32x12_9win               @(42)
Run-Job doc       32x12_residual_doc       @(42)
Run-Job feed      32x3_residual_roughness  @(42)
Run-Job roughness 32x12_feedopt_9win       @(42)
Run-Job doc       32x3_feedopt_9win        @(42)   # best doc WITHOUT residual preprocessing
Run-Job feed      32x3_9win                @(42)   # best feed WITHOUT residual preprocessing

# Block 2: plain 32x12 baseline, 5 seeds (optional but needed for the generalization column)
foreach ($t in "speed", "doc", "feed", "roughness") { Run-Job $t 32x12 @(42, 43, 44, 45, 46) }

python compute_prf1.py "cv_preds/cnn/*.csv" --out_md cv_preds/cnn_prf1.md
"wrote cv_preds/cnn_prf1.md"
