$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

# ============================================================
# 1. Build harmonic feature dirs (options 1 + 2)
#    - scalograms_harmonic_speedopt/      speed, global norm
#    - scalograms_harmonic_feedopt/       feed_coarse, global norm
#    - scalograms_harmonic_feedopt_perdoc/ feed_coarse, per-DOC norm
# ============================================================
Write-Host "`n=== BUILD HARMONIC FEATURE DIRS ===" -ForegroundColor Cyan
python build_harmonic_features.py --target speed
python build_harmonic_features.py --target feed_coarse
python build_harmonic_features.py --target feed_coarse --norm_mode per_doc

# ============================================================
# 2. Build per-DOC-normalised dirs (option 3) from Excel features
#    - scalograms_32x3_feedopt_perdoc/
#    - scalograms_32x12_feedopt_perdoc/
#    - scalograms_32x3_speedopt_perdoc/
#    - scalograms_32x12_speedopt_perdoc/
# ============================================================
Write-Host "`n=== BUILD PER-DOC NORM DIRS ===" -ForegroundColor Cyan
python build_32x3_features.py  --target feed_coarse --norm_mode per_doc
python build_32x12_features.py --target feed_coarse --norm_mode per_doc
python build_32x3_features.py  --target speed       --norm_mode per_doc
python build_32x12_features.py --target speed       --norm_mode per_doc

# ============================================================
# 3. Generate SMOTE for new dirs
# ============================================================
Write-Host "`n=== SMOTE ===" -ForegroundColor Cyan
python smote_generate_32x3.py --img_dir scalograms_harmonic_speedopt      --target speed
python smote_generate_32x3.py --img_dir scalograms_harmonic_feedopt       --target feed_coarse
python smote_generate_32x3.py --img_dir scalograms_32x3_feedopt_perdoc    --target feed_coarse
python smote_generate_32x3.py --img_dir scalograms_32x12_feedopt_perdoc   --target feed_coarse
python smote_generate_32x3.py --img_dir scalograms_32x3_speedopt_perdoc   --target speed
python smote_generate_32x3.py --img_dir scalograms_32x12_speedopt_perdoc  --target speed

# ============================================================
# 4. Train: Harmonic features for speed (options 1+2)
# ============================================================
Write-Host "`n=== TRAIN: HARMONIC SPEED ===" -ForegroundColor Cyan
foreach ($arch in $archs) {
    foreach ($lr in $lrs) {
        python cnn_model/cnn_train_32x3.py --target speed `
            --img_dir scalograms_harmonic_speedopt --arch $arch --lr $lr --run_tag smote
        python cnn_model/cnn_train_32x3.py --target speed `
            --img_dir scalograms_harmonic_speedopt --arch $arch --lr $lr --run_tag nosmote --no_smote
    }
}

# ============================================================
# 5. Train: Harmonic features for feed_coarse (options 1+2)
# ============================================================
Write-Host "`n=== TRAIN: HARMONIC FEED_COARSE ===" -ForegroundColor Cyan
foreach ($dir in @("scalograms_harmonic_feedopt", "scalograms_harmonic_feedopt_perdoc")) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse `
                --img_dir $dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target feed_coarse `
                --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

# ============================================================
# 6. Train: Per-DOC-normalised Excel features (option 3)
# ============================================================
Write-Host "`n=== TRAIN: PER-DOC NORM EXCEL FEATURES ===" -ForegroundColor Cyan
foreach ($dir in @(
    "scalograms_32x3_feedopt_perdoc",
    "scalograms_32x12_feedopt_perdoc",
    "scalograms_32x3_speedopt_perdoc",
    "scalograms_32x12_speedopt_perdoc"
)) {
    $tgt = if ($dir -match "feedopt") { "feed_coarse" } else { "speed" }
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            python cnn_model/cnn_train_32x3.py --target $tgt `
                --img_dir $dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target $tgt `
                --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

Write-Host "`n=== All done ===" -ForegroundColor Green
