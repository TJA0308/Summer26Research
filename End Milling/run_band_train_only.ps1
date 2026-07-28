$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

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
