#!/bin/bash
# F1: std speed (8) + ses speed (8)
set -e
cd "$(dirname "$0")"

echo "[F1] std speed rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_rn18_lr1e3.pt
echo "[F1] std speed rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_rn18_lr1e4.pt
echo "[F1] std speed rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_rn50_lr1e3.pt
echo "[F1] std speed rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_rn50_lr1e4.pt
echo "[F1] std speed enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_enb0_lr1e3.pt
echo "[F1] std speed enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_enb0_lr1e4.pt
echo "[F1] std speed cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_cnxt_lr1e3.pt
echo "[F1] std speed cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_speed_cnxt_lr1e4.pt

echo "[F1] ses speed rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_rn18_lr1e3.pt
echo "[F1] ses speed rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_rn18_lr1e4.pt
echo "[F1] ses speed rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_rn50_lr1e3.pt
echo "[F1] ses speed rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_rn50_lr1e4.pt
echo "[F1] ses speed enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_enb0_lr1e3.pt
echo "[F1] ses speed enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_enb0_lr1e4.pt
echo "[F1] ses speed cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_cnxt_lr1e3.pt
echo "[F1] ses speed cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_speed_cnxt_lr1e4.pt

echo "[F1] DONE"
