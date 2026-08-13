$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# ═══════════════════════════════════════════════════════════
# Alt-split robustness training for the 32x3/32x12 feature set
# Note: --arch (not --backbone); no --save flag (auto-derived);
#       --no_smote to disable (SMOTE on by default); --run_tag for naming.
# ═══════════════════════════════════════════════════════════

# ── DOC alt3 / alt4 (SMOTE on by default, no --no_smote) ──────
Write-Host "=== DOC alt3 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target doc `
    --img_dir scalograms_32x3_docopt_raw3w `
    --split alt3 `
    --run_tag alt3 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

Write-Host "=== DOC alt4 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target doc `
    --img_dir scalograms_32x3_docopt_raw3w `
    --split alt4 `
    --run_tag alt4 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

# ── Feed Coarse alt3 / alt4 (retrain; SMOTE on by default) ──
Write-Host "=== Feed Coarse alt3 (feedopt_9win / convnext_tiny) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target feed_coarse `
    --img_dir scalograms_32x3_feedopt_9win `
    --split alt3 `
    --run_tag alt3 `
    --arch convnext_tiny `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

Write-Host "=== Feed Coarse alt3 (feedopt_raw9w_residual / resnet50) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target feed_coarse `
    --img_dir scalograms_32x3_feedopt_raw9w_residual `
    --split alt3 `
    --run_tag alt3 `
    --arch resnet50 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

Write-Host "=== Feed Coarse alt4 (feedopt_9win / convnext_tiny) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target feed_coarse `
    --img_dir scalograms_32x3_feedopt_9win `
    --split alt4 `
    --run_tag alt4 `
    --arch convnext_tiny `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

Write-Host "=== Feed Coarse alt4 (feedopt_raw9w_residual / resnet50) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target feed_coarse `
    --img_dir scalograms_32x3_feedopt_raw9w_residual `
    --split alt4 `
    --run_tag alt4 `
    --arch resnet50 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

# ── DOC alt5 / alt6 (low-RPM safe splits) ────────────────────────────────
Write-Host "=== DOC alt5 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target doc `
    --img_dir scalograms_32x3_docopt_raw3w `
    --split alt5 `
    --run_tag alt5 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

Write-Host "=== DOC alt6 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target doc `
    --img_dir scalograms_32x3_docopt_raw3w `
    --split alt6 `
    --run_tag alt6 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

# ── Roughness cascade alt7 (--no_smote; cascade uses predicted conditioning) ──
Write-Host "=== Roughness: Speed parent rough_alt7 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target speed `
    --img_dir scalograms_32x3_residual_roughness `
    --split rough_alt7 `
    --run_tag alt7 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --no_smote
Write-Host "---"

Write-Host "=== Roughness: DOC parent rough_alt7 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target doc `
    --img_dir scalograms_32x3_residual_roughness `
    --split rough_alt7 `
    --run_tag alt7 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
Write-Host "---"

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

# ── Roughness cascade alt8 ────────────────────────────────────
Write-Host "=== Roughness: Speed parent rough_alt8 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target speed `
    --img_dir scalograms_32x3_residual_roughness `
    --split rough_alt8 `
    --run_tag alt8 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --no_smote
Write-Host "---"

Write-Host "=== Roughness: DOC parent rough_alt8 ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target doc `
    --img_dir scalograms_32x3_residual_roughness `
    --split rough_alt8 `
    --run_tag alt8 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --dropout 0.15
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

# ── Speed alt7 / alt8 (--no_smote; ensemble: 32x12_9win + 32x3) ──
Write-Host "=== Speed alt7 (32x12_9win / resnet18) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target speed `
    --img_dir scalograms_32x12_9win `
    --split alt7 `
    --run_tag alt7 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --no_smote
Write-Host "---"

Write-Host "=== Speed alt7 (32x3 / resnet18) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target speed `
    --img_dir scalograms_32x3 `
    --split alt7 `
    --run_tag alt7 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --no_smote
Write-Host "---"

Write-Host "=== Speed alt8 (32x12_9win / resnet18) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target speed `
    --img_dir scalograms_32x12_9win `
    --split alt8 `
    --run_tag alt8 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --no_smote
Write-Host "---"

Write-Host "=== Speed alt8 (32x3 / resnet18) ===" -ForegroundColor Cyan
python cnn_model/cnn_train_32x3.py `
    --target speed `
    --img_dir scalograms_32x3 `
    --split alt8 `
    --run_tag alt8 `
    --arch resnet18 `
    --lr 1e-3 `
    --epochs 50 `
    --no_smote
Write-Host "---"

# ── Generate window_preds for all new models ─────────────────
Write-Host "=== Generating window_preds for all new alt models ===" -ForegroundColor Cyan
python generate_window_results.py --only_missing

Write-Host "Done." -ForegroundColor Green
