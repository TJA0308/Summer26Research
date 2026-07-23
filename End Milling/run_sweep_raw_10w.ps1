$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Full sweep: 4 targets x 4 archs x 2 LRs x +/-SMOTE = 64 runs
# All on scalograms_raw_10w (genuine temporal windowing from raw signals)

# --- speed ---
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- doc ---
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- feed_coarse ---
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote

# --- roughness ---
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch resnet50 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch efficientnet_b0 --lr 1e-4 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-3 --run_tag nosmote --no_smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_raw_10w --arch convnext_tiny --lr 1e-4 --run_tag nosmote --no_smote
