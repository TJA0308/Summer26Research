$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Full sweep over raw-window feature dirs (scalograms_32x[3|12]_*_raw[3|9]w)
# plain + conditioned + cascade_predicted + residual plain
# 4 archs x 2 LRs x +/-SMOTE x all applicable dirs

# =============================================================================
# SECTION 1: Plain sweeps (all 4 targets, all dirs, +/-SMOTE)
# =============================================================================
Write-Host "`n=== PLAIN SWEEPS ===" -ForegroundColor Cyan

# --- speed ---
foreach ($dir in @(
    "scalograms_32x3_speedopt_raw3w",  "scalograms_32x3_speedopt_raw9w",
    "scalograms_32x12_speedopt_raw3w", "scalograms_32x12_speedopt_raw9w"
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
    "scalograms_32x3_docopt_raw3w",  "scalograms_32x3_docopt_raw9w",
    "scalograms_32x12_docopt_raw3w", "scalograms_32x12_docopt_raw9w"
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
    "scalograms_32x3_feedopt_raw3w",  "scalograms_32x3_feedopt_raw9w",
    "scalograms_32x12_feedopt_raw3w", "scalograms_32x12_feedopt_raw9w"
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
    "scalograms_32x3_raw3w",  "scalograms_32x3_raw9w",
    "scalograms_32x12_raw3w", "scalograms_32x12_raw9w"
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
# feed_coarse and roughness only
# =============================================================================
Write-Host "`n=== CONDITIONED SWEEPS ===" -ForegroundColor Cyan

# feed_coarse: plain + residual dirs
foreach ($dir in @(
    "scalograms_32x3_feedopt_raw3w",          "scalograms_32x3_feedopt_raw9w",
    "scalograms_32x3_feedopt_raw3w_residual", "scalograms_32x3_feedopt_raw9w_residual",
    "scalograms_32x12_feedopt_raw3w",         "scalograms_32x12_feedopt_raw9w",
    "scalograms_32x12_feedopt_raw3w_residual","scalograms_32x12_feedopt_raw9w_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# roughness: plain + residual dirs
foreach ($dir in @(
    "scalograms_32x3_raw3w",                      "scalograms_32x3_raw9w",
    "scalograms_32x3_raw3w_residual_roughness",   "scalograms_32x3_raw9w_residual_roughness",
    "scalograms_32x12_raw3w",                     "scalograms_32x12_raw9w",
    "scalograms_32x12_raw3w_residual_roughness",  "scalograms_32x12_raw9w_residual_roughness"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target roughness --img_dir $dir --arch $arch --lr $lr --conditioned
        }
    }
}

# =============================================================================
# SECTION 3: predict_conditioning (speed + doc on all relevant dirs)
# =============================================================================
Write-Host "`n=== PREDICT CONDITIONING ===" -ForegroundColor Cyan

foreach ($dir in @(
    "scalograms_32x3_speedopt_raw3w", "scalograms_32x3_speedopt_raw9w",
    "scalograms_32x12_speedopt_raw3w","scalograms_32x12_speedopt_raw9w",
    "scalograms_32x3_feedopt_raw3w",  "scalograms_32x3_feedopt_raw9w",
    "scalograms_32x12_feedopt_raw3w", "scalograms_32x12_feedopt_raw9w",
    "scalograms_32x3_raw3w",          "scalograms_32x3_raw9w",
    "scalograms_32x12_raw3w",         "scalograms_32x12_raw9w"
)) {
    python predict_conditioning_32x3.py --target speed --img_dir $dir
    python predict_conditioning_32x3.py --target doc   --img_dir $dir
}

# =============================================================================
# SECTION 4: Cascade_predicted sweeps (feed_coarse + roughness only)
# =============================================================================
Write-Host "`n=== CASCADE_PREDICTED SWEEPS ===" -ForegroundColor Cyan

# feed_coarse: plain + residual dirs
foreach ($dir in @(
    "scalograms_32x3_feedopt_raw3w",          "scalograms_32x3_feedopt_raw9w",
    "scalograms_32x3_feedopt_raw3w_residual", "scalograms_32x3_feedopt_raw9w_residual",
    "scalograms_32x12_feedopt_raw3w",         "scalograms_32x12_feedopt_raw9w",
    "scalograms_32x12_feedopt_raw3w_residual","scalograms_32x12_feedopt_raw9w_residual"
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir $dir --arch $arch --lr $lr --cascade_predicted
        }
    }
}

# roughness: plain + residual dirs
foreach ($dir in @(
    "scalograms_32x3_raw3w",                      "scalograms_32x3_raw9w",
    "scalograms_32x3_raw3w_residual_roughness",   "scalograms_32x3_raw9w_residual_roughness",
    "scalograms_32x12_raw3w",                     "scalograms_32x12_raw9w",
    "scalograms_32x12_raw3w_residual_roughness",  "scalograms_32x12_raw9w_residual_roughness"
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
    @{target="feed_coarse"; dir="scalograms_32x3_feedopt_raw3w_residual"},
    @{target="feed_coarse"; dir="scalograms_32x3_feedopt_raw9w_residual"},
    @{target="feed_coarse"; dir="scalograms_32x12_feedopt_raw3w_residual"},
    @{target="feed_coarse"; dir="scalograms_32x12_feedopt_raw9w_residual"},
    @{target="roughness";   dir="scalograms_32x3_raw3w_residual_roughness"},
    @{target="roughness";   dir="scalograms_32x3_raw9w_residual_roughness"},
    @{target="roughness";   dir="scalograms_32x12_raw3w_residual_roughness"},
    @{target="roughness";   dir="scalograms_32x12_raw9w_residual_roughness"}
)) {
    foreach ($arch in @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")) {
        foreach ($lr in @("1e-3", "1e-4")) {
            python cnn_model/cnn_train_32x3.py --target $entry.target --img_dir $entry.dir --arch $arch --lr $lr --run_tag smote
            python cnn_model/cnn_train_32x3.py --target $entry.target --img_dir $entry.dir --arch $arch --lr $lr --run_tag nosmote --no_smote
        }
    }
}

Write-Host "`n=== All done ===" -ForegroundColor Green
