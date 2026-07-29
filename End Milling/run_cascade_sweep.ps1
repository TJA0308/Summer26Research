$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot

$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

# (target, img_dir) pairs: base + residual, 32x3 + 32x12, feed_coarse + roughness
$jobs = @(
    @{ target = "feed_coarse"; dir = "scalograms_32x3_feedopt" },
    @{ target = "feed_coarse"; dir = "scalograms_32x12_feedopt" },
    @{ target = "feed_coarse"; dir = "scalograms_32x3_feedopt_residual" },
    @{ target = "feed_coarse"; dir = "scalograms_32x12_feedopt_residual" },
    @{ target = "roughness";   dir = "scalograms_32x3" },
    @{ target = "roughness";   dir = "scalograms_32x12" },
    @{ target = "roughness";   dir = "scalograms_32x3_residual_roughness" },
    @{ target = "roughness";   dir = "scalograms_32x12_residual_roughness" }
)

foreach ($j in $jobs) {
    Write-Host "`n=== CASCADE: $($j.target) / $($j.dir) ===" -ForegroundColor Cyan
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            python cnn_model/cnn_train_32x3.py --target $j.target --img_dir $j.dir `
                --arch $arch --lr $lr --cascade_predicted --run_tag cascade_smote
            python cnn_model/cnn_train_32x3.py --target $j.target --img_dir $j.dir `
                --arch $arch --lr $lr --cascade_predicted --no_smote --run_tag cascade_nosmote
        }
    }
}

Write-Host "`n=== Cascade sweep done ===" -ForegroundColor Green
