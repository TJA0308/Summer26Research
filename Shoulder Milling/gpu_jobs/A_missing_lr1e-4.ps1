# Batch A: only cells find_missing_runs.py reports as MISSING/MISMATCH (currently just the one below).
# Add "target|group|scalogram|lr" entries after re-running: python find_missing_runs.py
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$batch = "A"; New-Item -ItemType Directory -Force "cv_runs/$batch" | Out-Null
$jobs = @(
  "roughness|secondary|32x12_feedopt_9win|1e-3"   # no lr=1e-3 row exists for this cell
)
foreach ($j in $jobs) {
  $t, $g, $s, $lr = $j -split '\|'
  $out = "cv_runs/$batch/${t}__${s}__lr${lr}__s42.csv"
  if ((Test-Path $out) -and (Get-Item $out).Length -gt 0) { "skip $out"; continue }
  $extra = @(); if ($t -eq "roughness") { $extra = @("--roughness_group", $g) }
  python cv_evaluate.py --img_dir "scalograms_$s" --target $t --split loco @extra `
    --models cnn --arch resnet18 --epochs 50 --lr $lr --seeds 42 --out_csv $out
  if ($LASTEXITCODE) { throw "job failed: $j" }
}
