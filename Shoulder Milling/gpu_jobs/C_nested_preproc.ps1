# Batch C: fold-nested preprocessing variants (new variants; seed 42 is NOT a selection seed).
# resnet18, 50 epochs, lr 1e-3, seeds 42-46. Base dirs are the 72-window dirs (*_9win unsupported).
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$batch = "C"; New-Item -ItemType Directory -Force "cv_runs/$batch" | Out-Null
$jobs = @(
  @{p="feedopt_nested";     t="feed";      s="32x3_feedopt"},
  @{p="feedopt_nested";     t="roughness"; s="32x12_feedopt"},
  @{p="residual_inductive"; t="speed";     s="32x12"},
  @{p="residual_inductive"; t="doc";       s="32x12"},
  @{p="residual_inductive"; t="feed";      s="32x3"},
  @{p="residual_inductive"; t="roughness"; s="32x12"}
)
foreach ($j in $jobs) {
  $out = "cv_runs/$batch/$($j.t)__$($j.s)__$($j.p)__lr1e-3__s42-46.csv"
  if ((Test-Path $out) -and (Get-Item $out).Length -gt 0) { "skip $out"; continue }
  $extra = @(); if ($j.t -eq "roughness") { $extra = @("--roughness_group", "primary") }
  python cv_evaluate.py --img_dir "scalograms_$($j.s)" --target $j.t --split loco @extra `
    --preproc $j.p --models cnn --arch resnet18 --epochs 50 --lr 1e-3 `
    --seeds 42 43 44 45 46 --out_csv $out
  if ($LASTEXITCODE) { throw "job failed: $($j.t) $($j.s) $($j.p)" }
}
