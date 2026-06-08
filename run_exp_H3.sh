#!/bin/bash
# H3: std_smote roughness (8 jobs)
set -e
cd "$(dirname "$0")"
mkdir -p exp_models_d

echo "[H3] std_smote roughness rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet18 --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_rn18_lr1e3.pt --history exp_models_d/std_smote_roughness_rn18_lr1e3_history.json
echo "[H3] std_smote roughness rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet18 --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_rn18_lr1e4.pt --history exp_models_d/std_smote_roughness_rn18_lr1e4_history.json
echo "[H3] std_smote roughness rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet50 --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_rn50_lr1e3.pt --history exp_models_d/std_smote_roughness_rn50_lr1e3_history.json
echo "[H3] std_smote roughness rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet50 --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_rn50_lr1e4.pt --history exp_models_d/std_smote_roughness_rn50_lr1e4_history.json
echo "[H3] std_smote roughness enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone efficientnet_b0 --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_enb0_lr1e3.pt --history exp_models_d/std_smote_roughness_enb0_lr1e3_history.json
echo "[H3] std_smote roughness enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone efficientnet_b0 --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_enb0_lr1e4.pt --history exp_models_d/std_smote_roughness_enb0_lr1e4_history.json
echo "[H3] std_smote roughness cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone convnext_tiny --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_cnxt_lr1e3.pt --history exp_models_d/std_smote_roughness_cnxt_lr1e3_history.json
echo "[H3] std_smote roughness cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone convnext_tiny --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_roughness_cnxt_lr1e4.pt --history exp_models_d/std_smote_roughness_cnxt_lr1e4_history.json
echo "[H3] DONE"
