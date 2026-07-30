$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")
foreach ($arch in $archs) {
    foreach ($lr in $lrs) {
        python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch $arch --lr $lr --cascade_predicted --run_tag cascade_smote
        python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch $arch --lr $lr --cascade_predicted --no_smote --run_tag cascade_nosmote
    }
}
Write-Host "Done" -ForegroundColor Green
