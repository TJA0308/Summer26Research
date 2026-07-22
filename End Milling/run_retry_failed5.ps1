# Retry the 5 runs that failed with error code 32 (Windows file-lock on torch.save)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# 1. speed / scalograms_32x3 / resnet18 / lr=1e-4 / nosmote
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x3 --arch resnet18 --lr 1e-4 --run_tag nosmote --no_smote

# 2. doc / scalograms_32x3 / resnet18 / lr=1e-3 / nosmote
python cnn_model/cnn_train_32x3.py --target doc --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3 --run_tag nosmote --no_smote

# 3. feed_coarse / scalograms_32x3_feedopt / convnext_tiny / lr=1e-4 / smote
python cnn_model/cnn_train_32x3.py --target feed_coarse --img_dir scalograms_32x3_feedopt --arch convnext_tiny --lr 1e-4 --run_tag smote

# 4. roughness / scalograms_32x3 / resnet18 / lr=1e-3 / smote
python cnn_model/cnn_train_32x3.py --target roughness --img_dir scalograms_32x3 --arch resnet18 --lr 1e-3 --run_tag smote

# 5. speed / scalograms_32x12_feedopt / resnet18 / lr=1e-3 (cascade dep, no smote flag)
python cnn_model/cnn_train_32x3.py --target speed --img_dir scalograms_32x12_feedopt --arch resnet18 --lr 1e-3
