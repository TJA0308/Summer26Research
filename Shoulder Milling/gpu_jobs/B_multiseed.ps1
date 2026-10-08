# Batch B: seeds 43 44 45 46 for the four pre-registered configs (lr 1e-3, resnet18, 50 epochs).
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$batch = "B"; New-Item -ItemType Directory -Force "cv_runs/$batch" | Out-Null
$jobs = @(
  @{t="speed";     s="32x12_9win"},
  @{t="doc";       s="32x12_residual_doc"},
  @{t="feed";      s="32x3_residual_roughness"},
  @{t="roughness"; s="32x12_feedopt_9win"}
)
foreach ($j in $jobs) {
  $out = "cv_runs/$batch/$($j.t)__$($j.s)__lr1e-3__s43-44-45-46.csv"
  if ((Test-Path $out) -and (Get-Item $out).Length -gt 0) { "skip $out"; continue }
  $extra = @(); if ($j.t -eq "roughness") { $extra = @("--roughness_group", "primary") }
  python cv_evaluate.py --img_dir "scalograms_$($j.s)" --target $j.t --split loco @extra `
    --models cnn --arch resnet18 --epochs 50 --lr 1e-3 --seeds 43 44 45 46 --out_csv $out
  if ($LASTEXITCODE) { throw "job failed: $($j.t) $($j.s)" }
}
