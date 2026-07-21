# Master detailed (flat, non-loop) run file -- literally every command
# across all three sweeps in one file: main plain-training sweep (256),
# cascade sweep (272, feed_coarse + roughness), residual-corrected
# sweep (192, includes roughness cascade) = 720 training runs
# total. Generated from run_sweep_32xN_detailed.ps1,
# run_sweep_cascade_detailed.ps1, and run_sweep_residual_detailed.ps1 --
# edit those individually and regenerate this file if the grids change,
# don't hand-edit this one.
#
# Usage: powershell -File run_everything_detailed.ps1
# (This will take a long time -- 720 full training runs. Comment out
# sections you don't want before running, or run the three individual
# _detailed.ps1 files instead if you want to run phases separately.)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# ======================================================================
# PHASE 1: Main plain-training sweep (256 runs)
# ======================================================================
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

# ======================================================================
# PHASE 2: Cascade sweep -- feed_coarse + roughness (272 runs)
# ======================================================================
#
# Usage: powershell -File run_sweep_cascade_detailed.ps1

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot


# === 32x3 3win (scalograms_32x3_feedopt): feed_coarse ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x3 3win (scalograms_32x3_feedopt): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4

# === 32x3 3win (scalograms_32x3_feedopt): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_feedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_feedopt

# === 32x3 3win (scalograms_32x3_feedopt): feed_coarse --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

# === 32x3 3win (scalograms_32x3): roughness ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x3 3win (scalograms_32x3): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4

# === 32x3 3win (scalograms_32x3): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3

# === 32x3 3win (scalograms_32x3): roughness --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

# === 32x3 9win (scalograms_32x3_feedopt_9win): feed_coarse ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x3 9win (scalograms_32x3_feedopt_9win): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-4

# === 32x3 9win (scalograms_32x3_feedopt_9win): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_feedopt_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_feedopt_9win

# === 32x3 9win (scalograms_32x3_feedopt_9win): feed_coarse --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt_9win --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

# === 32x3 9win (scalograms_32x3_9win): roughness ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x3 9win (scalograms_32x3_9win): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-4

# === 32x3 9win (scalograms_32x3_9win): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x3_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x3_9win

# === 32x3 9win (scalograms_32x3_9win): roughness --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

# === 32x12 3win (scalograms_32x12_feedopt): feed_coarse ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x12 3win (scalograms_32x12_feedopt): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-4

# === 32x12 3win (scalograms_32x12_feedopt): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_feedopt
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_feedopt

# === 32x12 3win (scalograms_32x12_feedopt): feed_coarse --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

# === 32x12 3win (scalograms_32x12): roughness ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x12 3win (scalograms_32x12): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-4

# === 32x12 3win (scalograms_32x12): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12

# === 32x12 3win (scalograms_32x12): roughness --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12 --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

# === 32x12 9win (scalograms_32x12_feedopt_9win): feed_coarse ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x12 9win (scalograms_32x12_feedopt_9win): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-4

# === 32x12 9win (scalograms_32x12_feedopt_9win): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_feedopt_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_feedopt_9win

# === 32x12 9win (scalograms_32x12_feedopt_9win): feed_coarse --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x12_feedopt_9win --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

# === 32x12 9win (scalograms_32x12_9win): roughness ground-truth --conditioned ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# === 32x12 9win (scalograms_32x12_9win): speed/doc (dependency for --cascade_predicted) ===
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-4
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-3
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-4

# === 32x12 9win (scalograms_32x12_9win): predict_conditioning ===
python predict_conditioning_32x3.py --target speed --img_dir scalograms_32x12_9win
python predict_conditioning_32x3.py --target doc   --img_dir scalograms_32x12_9win

# === 32x12 9win (scalograms_32x12_9win): roughness --cascade_predicted ===
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet18 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch resnet50 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch efficientnet_b0 --lr 1e-4 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-3 --cascade_predicted --run_tag cascade_pred
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win --arch convnext_tiny --lr 1e-4 --cascade_predicted --run_tag cascade_pred

Write-Host "Cascade sweep complete: 272 runs."

# ======================================================================
# PHASE 3: Residual-corrected sweep (192 runs)
# ======================================================================
# both cascade-eligible, see cnn_model/cnn_train_32x3.py's COND_PARENTS).
#
# --cascade_predicted is NOT included -- it would need speed/doc models
# trained on the SAME residual-corrected images, but that correction
# specifically removes the speed x doc signal those models would need. See
# run_sweep_residual.ps1's header for the full rationale.
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

# ================= Ground-truth --conditioned: roughness residual dirs =================

# --- 32x3 3win (scalograms_32x3_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_residual_roughness --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# --- 32x3 9win (scalograms_32x3_9win_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3_9win_residual_roughness --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# --- 32x12 3win (scalograms_32x12_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_residual_roughness --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

# --- 32x12 9win (scalograms_32x12_9win_residual_roughness) ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet18 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet18 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet50 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch resnet50 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch efficientnet_b0 --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch efficientnet_b0 --lr 1e-4 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch convnext_tiny --lr 1e-3 --conditioned --run_tag conditioned
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x12_9win_residual_roughness --arch convnext_tiny --lr 1e-4 --conditioned --run_tag conditioned

Write-Host "Residual sweep complete: 192 runs."
