$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# ============================================================
# Ordinal loss for feed_coarse (ordered: low < medium < high)
# Best dirs from prior sweep: 32x3_feedopt_residual (resnet18,
# resnet50) and 32x12_feedopt (convnext_tiny).
# Run both with and without SMOTE, two LRs.
# ============================================================
Write-Host "`n=== ORDINAL LOSS: feed_coarse ===" -ForegroundColor Cyan

$feedDirs = @(
    "scalograms_32x3_feedopt_residual",
    "scalograms_32x3_feedopt",
    "scalograms_32x12_feedopt",
    "scalograms_32x12_feedopt_residual"
)
$archs = @("resnet18", "resnet50", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

foreach ($dir in $feedDirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir `
                --arch $arch --lr $lr --run_tag ordinal_smote --ordinal_loss
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir `
                --arch $arch --lr $lr --run_tag ordinal_nosmote --ordinal_loss --no_smote
        }
    }
}

# ============================================================
# DOC-conditioned roughness (ground-truth upper bound)
# Residual dirs: removes DOC x speed mean so the model sees
# residual texture; conditioning then provides DOC explicitly.
# ============================================================
Write-Host "`n=== CONDITIONED ROUGHNESS ===" -ForegroundColor Cyan

$roughDirs = @(
    "scalograms_32x12_residual_roughness",
    "scalograms_32x3",
    "scalograms_32x12",
    "scalograms_32x3_residual_roughness"
)
$roughArchs = @("resnet18", "resnet50", "convnext_tiny")

foreach ($dir in $roughDirs) {
    foreach ($arch in $roughArchs) {
        foreach ($lr in $lrs) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir `
                --arch $arch --lr $lr --run_tag cond_gt --conditioned
        }
    }
}

Write-Host "`n=== All done ===" -ForegroundColor Green
