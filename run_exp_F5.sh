#!/bin/bash
# F5: sesrgb speed (8) + sesrgb doc (8)
set -e
cd "$(dirname "$0")"

echo "[F5] sesrgb speed rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_rn18_lr1e3.pt
echo "[F5] sesrgb speed rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_rn18_lr1e4.pt
echo "[F5] sesrgb speed rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_rn50_lr1e3.pt
echo "[F5] sesrgb speed rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_rn50_lr1e4.pt
echo "[F5] sesrgb speed enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_enb0_lr1e3.pt
echo "[F5] sesrgb speed enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_enb0_lr1e4.pt
echo "[F5] sesrgb speed cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_cnxt_lr1e3.pt
echo "[F5] sesrgb speed cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_speed_cnxt_lr1e4.pt

echo "[F5] sesrgb doc rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_rn18_lr1e3.pt
echo "[F5] sesrgb doc rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_rn18_lr1e4.pt
echo "[F5] sesrgb doc rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_rn50_lr1e3.pt
echo "[F5] sesrgb doc rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_rn50_lr1e4.pt
echo "[F5] sesrgb doc enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_enb0_lr1e3.pt
echo "[F5] sesrgb doc enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_enb0_lr1e4.pt
echo "[F5] sesrgb doc cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_cnxt_lr1e3.pt
echo "[F5] sesrgb doc cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_doc_cnxt_lr1e4.pt

echo "[F5] DONE"
