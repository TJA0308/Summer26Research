# Targeted retraining: speed on speedopt dirs, doc on docopt dirs
# 128 commands extracted from run_everything_detailed.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
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
