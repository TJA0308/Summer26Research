#!/bin/bash
# H1: std_smote speed (8 jobs)
set -e
cd "$(dirname "$0")"
mkdir -p exp_models_d

echo "[H1] std_smote speed rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet18 --lr 1e-3 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_rn18_lr1e3.pt --history exp_models_d/std_smote_speed_rn18_lr1e3_history.json
echo "[H1] std_smote speed rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet18 --lr 1e-4 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_rn18_lr1e4.pt --history exp_models_d/std_smote_speed_rn18_lr1e4_history.json
echo "[H1] std_smote speed rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet50 --lr 1e-3 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_rn50_lr1e3.pt --history exp_models_d/std_smote_speed_rn50_lr1e3_history.json
echo "[H1] std_smote speed rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet50 --lr 1e-4 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_rn50_lr1e4.pt --history exp_models_d/std_smote_speed_rn50_lr1e4_history.json
echo "[H1] std_smote speed enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone efficientnet_b0 --lr 1e-3 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_enb0_lr1e3.pt --history exp_models_d/std_smote_speed_enb0_lr1e3_history.json
echo "[H1] std_smote speed enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone efficientnet_b0 --lr 1e-4 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_enb0_lr1e4.pt --history exp_models_d/std_smote_speed_enb0_lr1e4_history.json
echo "[H1] std_smote speed cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone convnext_tiny --lr 1e-3 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_cnxt_lr1e3.pt --history exp_models_d/std_smote_speed_cnxt_lr1e3_history.json
echo "[H1] std_smote speed cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone convnext_tiny --lr 1e-4 --epochs 30 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_speed_cnxt_lr1e4.pt --history exp_models_d/std_smote_speed_cnxt_lr1e4_history.json
echo "[H1] DONE"
