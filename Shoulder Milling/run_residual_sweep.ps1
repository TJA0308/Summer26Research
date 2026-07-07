# Full CNN sweep on residual scalogram directories.
# 2 dirs x 4 archs x 2 LRs x 2 SMOTE = 32 models per target.
# Only running feed (the target we're investigating).
#
# Run from the Shoulder Milling directory:
#   .\run_residual_sweep.ps1

$ErrorActionPreference = "Continue"
$img_dirs = @("scalograms_32x3_feedopt_residual", "scalograms_32x12_feedopt_residual")
$archs    = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs      = @("1e-3", "1e-4")
$target   = "feed"

$total = $img_dirs.Count * $archs.Count * $lrs.Count * 2
$i = 0

foreach ($img_dir in $img_dirs) {
    foreach ($smote_mode in @($false, $true)) {
        $smote_label = if ($smote_mode) { "smote" } else { "no_smote" }
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "[$i/$total] $img_dir | $smote_label | $arch | lr=$lr" -ForegroundColor Cyan
                if ($smote_mode) {
                    python cnn_train_param.py --target $target --img_dir $img_dir `
                        --arch $arch --lr $lr --epochs 50
                } else {
                    python cnn_train_param.py --target $target --img_dir $img_dir `
                        --arch $arch --lr $lr --epochs 50 --no_smote
                }
                if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }
    }
}

# ── Eval all trained models ──────────────────────────────────────────────────
Write-Host "`n=== EVAL ===" -ForegroundColor Green
$i = 0
foreach ($img_dir in $img_dirs) {
    $scalo_tag = $img_dir -replace "scalograms_", ""
    foreach ($smote_mode in @($false, $true)) {
        $run_tag = if ($smote_mode) { "" } else { "" }   # default run_tag (base split)
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                $lr_fmt     = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                $model_path = "models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}_best.pt"
                Write-Host "[$i/$total] eval $img_dir | $arch | lr=$lr" -ForegroundColor Cyan
                python eval_detailed_param.py --target $target --img_dir $img_dir `
                    --arch $arch --lr $lr --model $model_path
                if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }
    }
}

Write-Host "`nAll done. Results in exp_results_32x3_feedopt_residual/ and exp_results_32x12_feedopt_residual/." -ForegroundColor Green
Write-Host "Run 'python summarize_results.py' or check cv_summary.csv for aggregated numbers." -ForegroundColor Green
