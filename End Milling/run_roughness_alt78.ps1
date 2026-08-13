$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$modelsDir = "cnn_model\models_roughness_raw_10w"

# Train alt7 x6 (zero sub-cluster-A in Medium test)
for ($i = 1; $i -le 6; $i++) {
    Write-Host "=== ALT7 run $i ===" -ForegroundColor Cyan
    python cnn_model/cnn_train.py `
        --target roughness `
        --img_dir scalograms_10w `
        --split alt7 `
        --backbone resnet18 `
        --lr 1e-3 `
        --epochs 30 `
        --dropout 0.15 `
        --augment light `
        --save "$modelsDir\resnet18_lr1e3_alt7_run${i}_best.pt"
    Write-Host "---"
}

# Train alt8 x6 (zero sub-cluster-A in Medium test, fresh Smooth/Rough)
for ($i = 1; $i -le 6; $i++) {
    Write-Host "=== ALT8 run $i ===" -ForegroundColor Cyan
    python cnn_model/cnn_train.py `
        --target roughness `
        --img_dir scalograms_10w `
        --split alt8 `
        --backbone resnet18 `
        --lr 1e-3 `
        --epochs 30 `
        --dropout 0.15 `
        --augment light `
        --save "$modelsDir\resnet18_lr1e3_alt8_run${i}_best.pt"
    Write-Host "---"
}

Write-Host "Done." -ForegroundColor Green
