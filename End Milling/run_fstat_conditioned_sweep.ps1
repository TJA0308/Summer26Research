$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# ============================================================
# 1. Build F-stat scale-selected dirs for speed
# ============================================================
Write-Host "`n=== BUILD F-STAT SPEED DIRS ===" -ForegroundColor Cyan

python build_32x3_features.py  --target speed --scale_method fstat
python build_32x12_features.py --target speed --scale_method fstat

# Generate SMOTE for the new fstat dirs
python smote_generate_32x3.py --img_dir scalograms_32x3_speedopt_fstat  --target speed
python smote_generate_32x3.py --img_dir scalograms_32x12_speedopt_fstat --target speed

# ============================================================
# 2. Train speed on F-stat dirs
# ============================================================
Write-Host "`n=== SPEED FSTAT SWEEP ===" -ForegroundColor Cyan

$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

foreach ($dir in @("scalograms_32x3_speedopt_fstat", "scalograms_32x12_speedopt_fstat")) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            python cnn_model/cnn_train_32x3.py --target speed --img_dir $dir `
                --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target speed --img_dir $dir `
                --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

# ============================================================
# 3. Feed_coarse -- conditioned on ground-truth speed+doc
#    (upper bound: tells us if conditioning would ever help)
# ============================================================
Write-Host "`n=== FEED_COARSE CONDITIONED (ground-truth) ===" -ForegroundColor Cyan

foreach ($dir in @(
    "scalograms_32x3_feedopt_residual",
    "scalograms_32x3_feedopt",
    "scalograms_32x12_feedopt",
    "scalograms_32x12_feedopt_residual"
)) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir `
                --arch $arch --lr $lr --run_tag cond_gt --conditioned
        }
    }
}

Write-Host "`n=== All done ===" -ForegroundColor Green
