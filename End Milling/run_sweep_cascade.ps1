# feed_coarse cascade sweep for the 32x3 / 32x12 precomputed-feature
# pipelines -- ground-truth --conditioned (upper-bound shortcut) AND the
# leakage-honest --cascade_predicted (needs speed+doc trained first, then
# predict_conditioning_32x3.py to generate the prediction CSVs it reads).
# Separate from run_sweep_32xN.ps1 because cascade only applies to
# feed_coarse and needs its own speed/doc dependency step first.
#
# Usage:
#   powershell -File run_sweep_cascade.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$LRs   = @("1e-3", "1e-4")

$Layouts = @(
    @{ Name = "32x3";  Feedopt = "scalograms_32x3_feedopt" },
    @{ Name = "32x12"; Feedopt = "scalograms_32x12_feedopt" }
)
$WinVariants = @("", "_9win")

foreach ($layout in $Layouts) {
    foreach ($winSuffix in $WinVariants) {
        $feedoptDir = "$($layout.Feedopt)$winSuffix"

        Write-Host "=== $feedoptDir : ground-truth --conditioned (all archs/lrs) ==="
        foreach ($arch in $Archs) {
            foreach ($lr in $LRs) {
                python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $feedoptDir `
                    --arch $arch --lr $lr --conditioned --run_tag conditioned
            }
        }

        Write-Host "=== $feedoptDir : speed/doc (dependency for --cascade_predicted) ==="
        foreach ($arch in $Archs) {
            foreach ($lr in $LRs) {
                python cnn_model/cnn_train_32x3.py --target speed --img_dir $feedoptDir --arch $arch --lr $lr
                python cnn_model/cnn_train_32x3.py --target doc   --img_dir $feedoptDir --arch $arch --lr $lr
            }
        }
        python predict_conditioning_32x3.py --target speed --img_dir $feedoptDir
        python predict_conditioning_32x3.py --target doc   --img_dir $feedoptDir

        Write-Host "=== $feedoptDir : --cascade_predicted (all archs/lrs) ==="
        foreach ($arch in $Archs) {
            foreach ($lr in $LRs) {
                python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $feedoptDir `
                    --arch $arch --lr $lr --cascade_predicted --run_tag cascade_pred
            }
        }
    }
}
Write-Host "Cascade sweep complete."
