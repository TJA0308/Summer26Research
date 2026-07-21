# Residual-corrected training sweep for the 32x3 / 32x12 pipelines.
# Condition-residual dirs only exist for roughness and feed_coarse (the two
# targets that share the DOC x speed nuisance covariate -- see
# build_residual_scalograms.py's docstring; speed/doc were excluded there
# because they already hit ~100% on raw features, nothing to rescue).
#
# All 4 backbones x 2 LRs x with/without SMOTE, across both layouts (32x3,
# 32x12) and both window variants (3win, 9win) = 128 plain-training runs,
# plus a ground-truth --conditioned cascade sweep for BOTH targets' 4
# residual dirs each (64 more runs -- roughness cascade support added
# alongside feed_coarse's, since both share the same nuisance covariate,
# see cnn_model/cnn_train_32x3.py's COND_PARENTS). --cascade_predicted is
# intentionally NOT included here: it would need speed/doc models trained ON
# the SAME residual-corrected images, but that correction specifically
# subtracts the speed x doc signal those models would need -- not a
# meaningful experiment, unlike the non-residual cascade sweep.
#
# These residual directories originally had no labels.csv/features_raw.npz/
# selected_scales.json (build_residual_scalograms.py only ever writes PNGs)
# -- smote_generate_32x3.py and predict_conditioning_32x3.py were both
# patched with a PNG-glob/pixel-space fallback so SMOTE and cascade
# conditioning work here too; plain training already worked (cnn_train.py's
# load_split() globs PNGs directly and never reads labels.csv).
#
# Usage:
#   powershell -File run_sweep_residual.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$LRs   = @("1e-3", "1e-4")

$RoughnessDirs = @(
    "scalograms_32x3_residual_roughness",
    "scalograms_32x3_9win_residual_roughness",
    "scalograms_32x12_residual_roughness",
    "scalograms_32x12_9win_residual_roughness"
)
$FeedCoarseDirs = @(
    "scalograms_32x3_feedopt_residual",
    "scalograms_32x3_feedopt_9win_residual",
    "scalograms_32x12_feedopt_residual",
    "scalograms_32x12_feedopt_9win_residual"
)

$done = 0
$total = ($RoughnessDirs.Count + $FeedCoarseDirs.Count) * $Archs.Count * $LRs.Count * 2

function Run-Plain($target, $imgDir) {
    foreach ($arch in $Archs) {
        foreach ($lr in $LRs) {
            foreach ($smoteMode in @("smote", "nosmote")) {
                $script:done++
                Write-Host "[$script:done/$total] $imgDir target=$target arch=$arch lr=$lr $smoteMode"
                $cmdArgs = @("--target", $target, "--img_dir", $imgDir, "--arch", $arch,
                             "--lr", $lr, "--run_tag", $smoteMode)
                if ($smoteMode -eq "nosmote") { $cmdArgs += "--no_smote" }
                python cnn_model/cnn_train_32x3.py @cmdArgs
            }
        }
    }
}

Write-Host "=== Plain training: roughness residual dirs ==="
foreach ($d in $RoughnessDirs) { Run-Plain "roughness" $d }

Write-Host "=== Plain training: feed_coarse residual dirs ==="
foreach ($d in $FeedCoarseDirs) { Run-Plain "feed_coarse" $d }

Write-Host "=== Ground-truth --conditioned cascade: feed_coarse residual dirs ==="
foreach ($d in $FeedCoarseDirs) {
    foreach ($arch in $Archs) {
        foreach ($lr in $LRs) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $d `
                --arch $arch --lr $lr --conditioned --run_tag conditioned
        }
    }
}

Write-Host "=== Ground-truth --conditioned cascade: roughness residual dirs ==="
foreach ($d in $RoughnessDirs) {
    foreach ($arch in $Archs) {
        foreach ($lr in $LRs) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $d `
                --arch $arch --lr $lr --conditioned --run_tag conditioned
        }
    }
}

Write-Host "Residual sweep complete: $done plain runs + 64 cascade runs."
