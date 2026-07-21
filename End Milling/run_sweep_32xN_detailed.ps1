# Detailed (flat, non-loop) version of run_sweep_32xN.ps1 -- every one of
# the 256 plain-training commands spelled out explicitly, so you can see
# exactly what runs before/while running it, or copy individual lines out.
# Same grid: 4 targets x 4 backbones x 2 LRs x with/without SMOTE, across
# both layouts (32x3/32x12) and both window variants (3win/9win). Each
# target trains on its OWN scale-selection-tuned directory (roughness ->
# base dir, feed_coarse -> _feedopt, speed -> _speedopt, doc -> _docopt --
# see compare_scale_selection.py / build_32x3_features.py's docstring for
# why speed/doc get dedicated selections instead of reusing roughness's).
#
# Usage: powershell -File run_sweep_32xN_detailed.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot


# --- 32x3 3win: speed (scalograms_32x3_speedopt) ---
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 3win: doc (scalograms_32x3_docopt) ---
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 3win: feed_coarse (scalograms_32x3_feedopt) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 3win: roughness (scalograms_32x3) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 9win: speed (scalograms_32x3_speedopt_9win) ---
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_speedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 9win: doc (scalograms_32x3_docopt_9win) ---
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_docopt_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 9win: feed_coarse (scalograms_32x3_feedopt_9win) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x3 9win: roughness (scalograms_32x3_9win) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 3win: speed (scalograms_32x12_speedopt) ---
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 3win: doc (scalograms_32x12_docopt) ---
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 3win: feed_coarse (scalograms_32x12_feedopt) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 3win: roughness (scalograms_32x12) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 9win: speed (scalograms_32x12_speedopt_9win) ---
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_speedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 9win: doc (scalograms_32x12_docopt_9win) ---
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_docopt_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 9win: feed_coarse (scalograms_32x12_feedopt_9win) ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- 32x12 9win: roughness (scalograms_32x12_9win) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

Write-Host "Sweep complete: 256 runs."
