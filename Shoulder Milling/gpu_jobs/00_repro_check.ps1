# Repro check: doc / 32x12_residual_doc / seed 42 / lr 1e-3 must reproduce 95.8% (run_acc_soft 0.9583).
# Run FIRST. If it fails, STOP and do not run batches A/B.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)
$out = "cv_runs/repro/doc__32x12_residual_doc__lr1e-3__s42.csv"
New-Item -ItemType Directory -Force "cv_runs/repro" | Out-Null
python cv_evaluate.py --selftest
if ($LASTEXITCODE) { throw "selftest failed" }
python cv_evaluate.py --img_dir scalograms_32x12_residual_doc --target doc --split loco `
  --models cnn --arch resnet18 --epochs 50 --lr 1e-3 --seeds 42 --out_csv $out
if ($LASTEXITCODE) { throw "cv_evaluate failed" }
$v = [double](Import-Csv $out | Select-Object -Last 1).run_acc_soft
"run_acc_soft=$v (expected 0.9583)"
if ([math]::Abs($v - 0.9583) -ge 0.0006) { throw "REPRO FAILED" }
"REPRO OK"
