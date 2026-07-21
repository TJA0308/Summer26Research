# Detailed (flat, non-loop) version of run_sweep_residual.ps1 -- every one
# of the 160 residual-corrected training commands spelled out explicitly:
# 128 plain-training runs (roughness x 4 dirs, feed_coarse x 4 dirs, 4
# backbones x 2 LRs x with/without SMOTE) + 32 ground-truth --conditioned
# cascade runs for feed_coarse's 4 residual dirs.
#
# --cascade_predicted is NOT included -- it would need speed/doc models
# trained on the SAME feed_coarse-residual-corrected images, but that
# correction specifically removes the speed x doc signal those models
# would need. See run_sweep_residual.ps1's header for the full rationale.
#
# Usage: powershell -File run_sweep_residual_detailed.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot


# ================= Plain training: roughness residual dirs =================

# --- 32x3 3win (scalograms_32x3_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 9win (scalograms_32x3_9win_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 3win (scalograms_32x12_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 9win (scalograms_32x12_9win_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# ================= Plain training: feed_coarse residual dirs =================

# --- 32x3 3win (scalograms_32x3_feedopt_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 9win (scalograms_32x3_feedopt_9win_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 3win (scalograms_32x12_feedopt_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 9win (scalograms_32x12_feedopt_9win_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# ================= Ground-truth --conditioned: feed_coarse residual dirs =================

# --- 32x3 3win (scalograms_32x3_feedopt_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_residual --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# --- 32x3 9win (scalograms_32x3_feedopt_9win_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win_residual --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# --- 32x12 3win (scalograms_32x12_feedopt_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_residual --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# --- 32x12 9win (scalograms_32x12_feedopt_9win_residual) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win_residual --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

Write-Host "Residual sweep complete: 160 runs."
