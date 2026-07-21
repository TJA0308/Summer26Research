# Detailed (flat, non-loop) version of run_sweep_cascade.ps1 -- every one
# of the cascade commands spelled out explicitly: ground-truth --conditioned,
# the speed/doc dependency training, the predict_conditioning_32x3.py step,
# and --cascade_predicted, for BOTH cascade-eligible targets (feed_coarse on
# its _feedopt dirs, roughness on its base dirs) across 32x3/32x12 x 3win/9win.
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
