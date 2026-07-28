$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

# ============================================================
# 1. Speed ensemble (immediate, no training needed)
# ============================================================
Write-Host "`n=== SPEED ENSEMBLE ===" -ForegroundColor Cyan
python ensemble_speed.py

# ============================================================
# 2. Build band-stat feature dirs
# ============================================================
Write-Host "`n=== BUILD BAND FEATURE DIRS ===" -ForegroundColor Cyan
python build_band_features.py --target feed_coarse
python build_band_features.py --target feed_coarse --norm_mode per_doc
python build_band_features.py --target roughness
python build_band_features.py --target speed

# ============================================================
# 3. SMOTE for band dirs
# ============================================================
Write-Host "`n=== SMOTE ===" -ForegroundColor Cyan
python smote_generate_32x3.py --img_dir scalograms_band_feedopt    --target feed_coarse
python smote_generate_32x3.py --img_dir scalograms_band_feedopt_perdoc --target feed_coarse
python smote_generate_32x3.py --img_dir scalograms_band_roughness  --target roughness
python smote_generate_32x3.py --img_dir scalograms_band_speedopt   --target speed

# ============================================================
# 4. Train band features
# ============================================================
Write-Host "`n=== TRAIN BAND: FEED_COARSE ===" -ForegroundColor Cyan
foreach ($dir in @("scalograms_band_feedopt", "scalograms_band_feedopt_perdoc")) {
    foreach ($arch in $archs) { foreach ($lr in $lrs) {
        python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir `
            --arch $arch --lr $lr --run_tag smote
        python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir `
            --arch $arch --lr $lr --run_tag nosmote --no_smote
    }}
}

Write-Host "`n=== TRAIN BAND: ROUGHNESS ===" -ForegroundColor Cyan
foreach ($arch in $archs) { foreach ($lr in $lrs) {
    python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_band_roughness `
        --arch $arch --lr $lr --run_tag smote
    python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_band_roughness `
        --arch $arch --lr $lr --run_tag nosmote --no_smote
}}

Write-Host "`n=== TRAIN BAND: SPEED ===" -ForegroundColor Cyan
foreach ($arch in $archs) { foreach ($lr in $lrs) {
    python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_band_speedopt `
        --arch $arch --lr $lr --run_tag smote
    python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_band_speedopt `
        --arch $arch --lr $lr --run_tag nosmote --no_smote
}}

Write-Host "`n=== All done ===" -ForegroundColor Green
