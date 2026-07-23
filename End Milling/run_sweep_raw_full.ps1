$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# =============================================================================
# Full sweep: raw_10w + 32x12 feature dirs
# plain + residual + conditioned + cascade_predicted, all archs/LRs/±SMOTE
#
# Run AFTER run_sweep_raw_10w.ps1 completes (cascade_predicted needs trained
# speed/doc models before predict_conditioning can run).
#
# Steps:
#   1.  Build residual dirs for scalograms_raw_10w
#   2.  Conditioned sweeps: 32x12 + raw_10w + their residual dirs
#   3.  predict_conditioning for speed + doc on raw_10w and 32x12 dirs
#   4.  Cascade_predicted sweeps: same dirs
#   5.  Residual plain sweeps: feed_coarse + roughness only, ±SMOTE
# =============================================================================

# =============================================================================
# 1. Build residual dirs for scalograms_raw_10w
#    (32x12 residual dirs already exist from previous runs)
# =============================================================================
Write-Host "`n=== Building residual dirs for scalograms_raw_10w ===" -ForegroundColor Cyan
python build_residual_scalograms.py --target feed_coarse --src_dirs scalograms_raw_10w
python build_residual_scalograms.py --target roughness   --src_dirs scalograms_raw_10w

# =============================================================================
# 2. Conditioned sweeps (ground-truth speed+doc, feed_coarse + roughness only)
#
# raw_10w dirs:
#   scalograms_raw_10w
#   scalograms_raw_10w_residual          (feed_coarse residual)
#   scalograms_raw_10w_residual_roughness
#
# 32x12 feature dirs (target-specific opt):
#   feed_coarse -> scalograms_32x12_feedopt, scalograms_32x12_feedopt_residual,
#                  scalograms_32x12_feedopt_9win, scalograms_32x12_feedopt_9win_residual
#   roughness   -> scalograms_32x12, scalograms_32x12_residual_roughness,
#                  scalograms_32x12_9win, scalograms_32x12_9win_residual_roughness
# =============================================================================
Write-Host "`n=== Conditioned sweeps (ground-truth) ===" -ForegroundColor Cyan

# feed_coarse: raw_10w dirs
foreach ($dir in @(
    "scalograms_raw_10w",
    "scalograms_raw_10w_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# feed_coarse: 32x12 feature dirs
foreach ($dir in @(
    "scalograms_32x12_feedopt",
    "scalograms_32x12_feedopt_residual",
    "scalograms_32x12_feedopt_9win",
    "scalograms_32x12_feedopt_9win_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# roughness: raw_10w dirs
foreach ($dir in @(
    "scalograms_raw_10w",
    "scalograms_raw_10w_residual_roughness"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# roughness: 32x12 feature dirs
foreach ($dir in @(
    "scalograms_32x12",
    "scalograms_32x12_residual_roughness",
    "scalograms_32x12_9win",
    "scalograms_32x12_9win_residual_roughness"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# =============================================================================
# 3. predict_conditioning: speed + doc on raw_10w and 32x12 dirs
#    (needs trained speed/doc models from run_sweep_raw_10w.ps1 and the
#     existing 32x12 plain sweeps)
# =============================================================================
Write-Host "`n=== Predict conditioning ===" -ForegroundColor Cyan

# raw_10w
python predict_conditioning_32x3.py --target speed --img_dir scalograms_raw_10w
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_raw_10w

# 32x12 (speed uses speedopt dir, doc uses docopt dir)
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_speedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_docopt

# 32x12 feedopt (the dir used for feed_coarse/roughness cascade)
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_feedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_feedopt
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_feedopt_9win
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_9win

# =============================================================================
# 4. Cascade_predicted sweeps (feed_coarse + roughness only)
# =============================================================================
Write-Host "`n=== Cascade_predicted sweeps ===" -ForegroundColor Cyan

# feed_coarse: raw_10w dirs
foreach ($dir in @(
    "scalograms_raw_10w",
    "scalograms_raw_10w_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --cascade_predicted
        }
    }
}

# feed_coarse: 32x12 feature dirs
foreach ($dir in @(
    "scalograms_32x12_feedopt",
    "scalograms_32x12_feedopt_residual",
    "scalograms_32x12_feedopt_9win",
    "scalograms_32x12_feedopt_9win_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --cascade_predicted
        }
    }
}

# roughness: raw_10w dirs
foreach ($dir in @(
    "scalograms_raw_10w",
    "scalograms_raw_10w_residual_roughness"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --cascade_predicted
        }
    }
}

# roughness: 32x12 feature dirs
foreach ($dir in @(
    "scalograms_32x12",
    "scalograms_32x12_residual_roughness",
    "scalograms_32x12_9win",
    "scalograms_32x12_9win_residual_roughness"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --cascade_predicted
        }
    }
}

# =============================================================================
# 5. Residual plain sweeps (feed_coarse + roughness only, ±SMOTE)
# =============================================================================
Write-Host "`n=== Residual plain sweeps ===" -ForegroundColor Cyan

foreach ($entry in @(
    @{target="feed_coarse"; dir="scalograms_raw_10w_residual"},
    @{target="feed_coarse"; dir="scalograms_32x12_feedopt_residual"},
    @{target="feed_coarse"; dir="scalograms_32x12_feedopt_9win_residual"},
    @{target="roughness";   dir="scalograms_raw_10w_residual_roughness"},
    @{target="roughness";   dir="scalograms_32x12_residual_roughness"},
    @{target="roughness";   dir="scalograms_32x12_9win_residual_roughness"}
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target $entry.target --img_dir $entry.dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target $entry.target --img_dir $entry.dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

Write-Host "`n=== All done ===" -ForegroundColor Green
