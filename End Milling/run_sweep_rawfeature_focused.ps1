$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Focused raw-window feature sweep:
# - Speed + DOC: baseline dirs (speedopt, docopt), 3win only, 4 archs x 2 LRs x +/-SMOTE
# - Feed_coarse + Roughness: baseline + residual dirs, 3win only, 4 archs x 2 LRs x +/-SMOTE

$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

# =============================================================================
# SPEED: baseline 32x3 + 32x12 speedopt, 3 windows
# =============================================================================
Write-Host "`n=== SPEED ===" -ForegroundColor Cyan
foreach ($dir in @("scalograms_32x3_speedopt_raw3w", "scalograms_32x12_speedopt_raw3w")) {
    foreach ($arch in $archs) { foreach ($lr in $lrs) {
        python cnn_model/cnn_train_32x3.py --target speed --img_dir $dir --arch $arch --lr $lr --run_tag smote
        python cnn_model/cnn_train_32x3.py --target speed --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
    }}
}

# =============================================================================
# DOC: baseline 32x3 + 32x12 docopt, 3 windows
# =============================================================================
Write-Host "`n=== DOC ===" -ForegroundColor Cyan
foreach ($dir in @("scalograms_32x3_docopt_raw3w", "scalograms_32x12_docopt_raw3w")) {
    foreach ($arch in $archs) { foreach ($lr in $lrs) {
        python cnn_model/cnn_train_32x3.py --target doc --img_dir $dir --arch $arch --lr $lr --run_tag smote
        python cnn_model/cnn_train_32x3.py --target doc --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
    }}
}

# =============================================================================
# FEED_COARSE: baseline + residual, 32x3 + 32x12 feedopt, 3 windows
# =============================================================================
Write-Host "`n=== FEED_COARSE ===" -ForegroundColor Cyan
foreach ($dir in @(
    "scalograms_32x3_feedopt_raw3w",
    "scalograms_32x3_feedopt_raw3w_residual",
    "scalograms_32x12_feedopt_raw3w",
    "scalograms_32x12_feedopt_raw3w_residual"
)) {
    foreach ($arch in $archs) { foreach ($lr in $lrs) {
        python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --run_tag smote
        python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
    }}
}

# =============================================================================
# ROUGHNESS: baseline + residual, 32x3 + 32x12, 3 windows
# =============================================================================
Write-Host "`n=== ROUGHNESS ===" -ForegroundColor Cyan
foreach ($dir in @(
    "scalograms_32x3_raw3w",
    "scalograms_32x3_raw3w_residual_roughness",
    "scalograms_32x12_raw3w",
    "scalograms_32x12_raw3w_residual_roughness"
)) {
    foreach ($arch in $archs) { foreach ($lr in $lrs) {
        python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --run_tag smote
        python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
    }}
}

Write-Host "`n=== All done ===" -ForegroundColor Green
