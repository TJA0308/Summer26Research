# Cascade sweep for the 32x3 / 32x12 precomputed-feature pipelines --
# ground-truth --conditioned (upper-bound shortcut) AND the leakage-honest
# --cascade_predicted (needs speed+doc trained first, then
# predict_conditioning_32x3.py to generate the prediction CSVs it reads).
#
# Covers BOTH cascade-eligible targets: feed_coarse (on its _feedopt dirs)
# and roughness (on its base dirs) -- both share the DOC x speed nuisance
# covariate that motivates cascading in the first place (see
# cnn_model/cnn_train_32x3.py's COND_PARENTS / module docstring). Separate
# from run_sweep_32xN.ps1 because cascade needs its own speed/doc dependency
# step first, per target's own img_dir.
#
# Usage:
#   powershell -File run_sweep_cascade.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$LRs   = @("1e-3", "1e-4")

# (cascade target, per-layout img_dir key)
$Layouts = @(
    @{ Name = "32x3";  Base = "scalograms_32x3";  Feedopt = "scalograms_32x3_feedopt" },
    @{ Name = "32x12"; Base = "scalograms_32x12"; Feedopt = "scalograms_32x12_feedopt" }
)
$WinVariants = @("", "_9win")
$CascadeTargets = @(
    @{ Target = "feed_coarse"; DirKey = "Feedopt" },
    @{ Target = "roughness";   DirKey = "Base" }
)

foreach ($layout in $Layouts) {
    foreach ($winSuffix in $WinVariants) {
        foreach ($ct in $CascadeTargets) {
            $target = $ct.Target
            $imgDir = "$($layout[$ct.DirKey])$winSuffix"

            Write-Host "=== $imgDir : $target ground-truth --conditioned (all archs/lrs) ==="
            foreach ($arch in $Archs) {
                foreach ($lr in $LRs) {
                    python cnn_model/cnn_train_32x3.py --target $target --img_dir $imgDir `
                        --arch $arch --lr $lr --conditioned --run_tag conditioned
                }
            }

            Write-Host "=== $imgDir : speed/doc (dependency for --cascade_predicted) ==="
            foreach ($arch in $Archs) {
                foreach ($lr in $LRs) {
                    python cnn_model/cnn_train_32x3.py --target speed --img_dir $imgDir --arch $arch --lr $lr
                    python cnn_model/cnn_train_32x3.py --target doc   --img_dir $imgDir --arch $arch --lr $lr
                }
            }
            python predict_conditioning_32x3.py --target speed --img_dir $imgDir
            python predict_conditioning_32x3.py --target doc   --img_dir $imgDir

            Write-Host "=== $imgDir : $target --cascade_predicted (all archs/lrs) ==="
            foreach ($arch in $Archs) {
                foreach ($lr in $LRs) {
                    python cnn_model/cnn_train_32x3.py --target $target --img_dir $imgDir `
                        --arch $arch --lr $lr --cascade_predicted --run_tag cascade_pred
                }
            }
        }
    }
}
Write-Host "Cascade sweep complete."
