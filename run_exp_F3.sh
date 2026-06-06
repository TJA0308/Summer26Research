#!/bin/bash
# F3: std roughness (8) + ses roughness (8)
set -e
cd "$(dirname "$0")"

echo "[F3] std roughness rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_rn18_lr1e3.pt
echo "[F3] std roughness rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_rn18_lr1e4.pt
echo "[F3] std roughness rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_rn50_lr1e3.pt
echo "[F3] std roughness rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_rn50_lr1e4.pt
echo "[F3] std roughness enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_enb0_lr1e3.pt
echo "[F3] std roughness enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_enb0_lr1e4.pt
echo "[F3] std roughness cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_cnxt_lr1e3.pt
echo "[F3] std roughness cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_roughness_cnxt_lr1e4.pt

echo "[F3] ses roughness rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_rn18_lr1e3.pt
echo "[F3] ses roughness rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_rn18_lr1e4.pt
echo "[F3] ses roughness rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_rn50_lr1e3.pt
echo "[F3] ses roughness rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_rn50_lr1e4.pt
echo "[F3] ses roughness enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_enb0_lr1e3.pt
echo "[F3] ses roughness enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_enb0_lr1e4.pt
echo "[F3] ses roughness cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_cnxt_lr1e3.pt
echo "[F3] ses roughness cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_roughness_cnxt_lr1e4.pt

echo "[F3] DONE"
