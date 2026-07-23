$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# =============================================================================
# Full sweep over 32x3 and 32x12 precomputed-feature scalogram dirs:
# plain + conditioned + cascade_predicted + residual plain, all 9win variants
# 4 archs x 2 LRs x +/-SMOTE x all applicable dirs
#
# predict_conditioning must be run before the cascade_predicted section.
# The script handles this by running plain first, then predict, then cascade.
# =============================================================================

# Target -> its base plain dirs (3win and 9win)
# Target -> residual dirs (feed_coarse and roughness only)

# =============================================================================
# SECTION 1: Plain sweeps (all targets, all dirs, +/-SMOTE)
# =============================================================================
Write-Host "`n=== PLAIN SWEEPS ===" -ForegroundColor Cyan

# --- speed ---
foreach ($dir in @(
    "scalograms_32x3_speedopt", "scalograms_32x3_speedopt_9win",
    "scalograms_32x12_speedopt", "scalograms_32x12_speedopt_9win"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target speed --img_dir $dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target speed --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

# --- doc ---
foreach ($dir in @(
    "scalograms_32x3_docopt", "scalograms_32x3_docopt_9win",
    "scalograms_32x12_docopt", "scalograms_32x12_docopt_9win"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target doc --img_dir $dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target doc --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

# --- feed_coarse ---
foreach ($dir in @(
    "scalograms_32x3_feedopt",     "scalograms_32x3_feedopt_9win",
    "scalograms_32x12_feedopt",    "scalograms_32x12_feedopt_9win"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

# --- roughness ---
foreach ($dir in @(
    "scalograms_32x3",     "scalograms_32x3_9win",
    "scalograms_32x12",    "scalograms_32x12_9win"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

# =============================================================================
# SECTION 2: Conditioned sweeps (ground-truth speed+doc)
# feed_coarse and roughness only, no SMOTE in conditioned mode
# =============================================================================
Write-Host "`n=== CONDITIONED SWEEPS (ground-truth) ===" -ForegroundColor Cyan

# feed_coarse: plain dirs + residual dirs
foreach ($dir in @(
    "scalograms_32x3_feedopt",          "scalograms_32x3_feedopt_9win",
    "scalograms_32x3_feedopt_residual", "scalograms_32x3_feedopt_9win_residual",
    "scalograms_32x12_feedopt",         "scalograms_32x12_feedopt_9win",
    "scalograms_32x12_feedopt_residual","scalograms_32x12_feedopt_9win_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# roughness: plain dirs + residual dirs
foreach ($dir in @(
    "scalograms_32x3",                       "scalograms_32x3_9win",
    "scalograms_32x3_residual_roughness",    "scalograms_32x3_9win_residual_roughness",
    "scalograms_32x12",                      "scalograms_32x12_9win",
    "scalograms_32x12_residual_roughness",   "scalograms_32x12_9win_residual_roughness"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# =============================================================================
# SECTION 3: predict_conditioning for speed + doc
# Must run before cascade_predicted section
# =============================================================================
Write-Host "`n=== PREDICT CONDITIONING ===" -ForegroundColor Cyan

# 32x3 dirs
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_speedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_docopt
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_feedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_feedopt
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_feedopt_9win
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_9win

# 32x12 dirs
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_speedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_docopt
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_feedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_feedopt
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_feedopt_9win
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_9win

# =============================================================================
# SECTION 4: Cascade_predicted sweeps (feed_coarse + roughness only)
# =============================================================================
Write-Host "`n=== CASCADE_PREDICTED SWEEPS ===" -ForegroundColor Cyan

# feed_coarse: plain dirs + residual dirs
foreach ($dir in @(
    "scalograms_32x3_feedopt",          "scalograms_32x3_feedopt_9win",
    "scalograms_32x3_feedopt_residual", "scalograms_32x3_feedopt_9win_residual",
    "scalograms_32x12_feedopt",         "scalograms_32x12_feedopt_9win",
    "scalograms_32x12_feedopt_residual","scalograms_32x12_feedopt_9win_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --cascade_predicted
        }
    }
}

# roughness: plain dirs + residual dirs
foreach ($dir in @(
    "scalograms_32x3",                       "scalograms_32x3_9win",
    "scalograms_32x3_residual_roughness",    "scalograms_32x3_9win_residual_roughness",
    "scalograms_32x12",                      "scalograms_32x12_9win",
    "scalograms_32x12_residual_roughness",   "scalograms_32x12_9win_residual_roughness"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --cascade_predicted
        }
    }
}

# =============================================================================
# SECTION 5: Residual plain sweeps (feed_coarse + roughness only, +/-SMOTE)
# =============================================================================
Write-Host "`n=== RESIDUAL PLAIN SWEEPS ===" -ForegroundColor Cyan

foreach ($entry in @(
    @{target="feed_coarse"; dir="scalograms_32x3_feedopt_residual"},
    @{target="feed_coarse"; dir="scalograms_32x3_feedopt_9win_residual"},
    @{target="feed_coarse"; dir="scalograms_32x12_feedopt_residual"},
    @{target="feed_coarse"; dir="scalograms_32x12_feedopt_9win_residual"},
    @{target="roughness";   dir="scalograms_32x3_residual_roughness"},
    @{target="roughness";   dir="scalograms_32x3_9win_residual_roughness"},
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
