$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Re-run roughness alt7/alt8 cascade after fixing predict_conditioning_32x3.py
# (was failing because models_root defaulted to repo root, not cnn_model/)

# Speed + DOC parent models are already trained (in cnn_model/models_speed/doc_32x3_residual_roughness/)
# Just need to re-run predict_conditioning and retrain the cascade model.

Write-Host "=== Roughness: predict conditioning for alt7 ===" -ForegroundColor Cyan
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_residual_roughness --run_tag alt7
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_residual_roughness --run_tag alt7
Write-Host "---"

Write-Host "=== Roughness: cascade model alt7 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target roughness `
    --img_dir scalograms_32x3_residual_roughness `
    --split alt7 `
    --run_tag alt7 `
    --arch convnext_tiny `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15 `
    --no_smote `
    --cascade_predicted
Write-Host "---"

Write-Host "=== Roughness: predict conditioning for alt8 ===" -ForegroundColor Cyan
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_residual_roughness --run_tag alt8
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_residual_roughness --run_tag alt8
Write-Host "---"

Write-Host "=== Roughness: cascade model alt8 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target roughness `
    --img_dir scalograms_32x3_residual_roughness `
    --split alt8 `
    --run_tag alt8 `
    --arch convnext_tiny `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15 `
    --no_smote `
    --cascade_predicted
Write-Host "---"

Write-Host "=== Generating window_preds for roughness alt7/alt8 ===" -ForegroundColor Cyan
python generate_window_results.py --target roughness
Write-Host "Done." -ForegroundColor Green
