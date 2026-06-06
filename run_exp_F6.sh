#!/bin/bash
# F6: sesrgb roughness (8) + sesrgb feed (8)
set -e
cd "$(dirname "$0")"

echo "[F6] sesrgb roughness rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_rn18_lr1e3.pt
echo "[F6] sesrgb roughness rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_rn18_lr1e4.pt
echo "[F6] sesrgb roughness rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_rn50_lr1e3.pt
echo "[F6] sesrgb roughness rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_rn50_lr1e4.pt
echo "[F6] sesrgb roughness enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_enb0_lr1e3.pt
echo "[F6] sesrgb roughness enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_enb0_lr1e4.pt
echo "[F6] sesrgb roughness cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_cnxt_lr1e3.pt
echo "[F6] sesrgb roughness cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_roughness_cnxt_lr1e4.pt

echo "[F6] sesrgb feed rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_rn18_lr1e3.pt
echo "[F6] sesrgb feed rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_rn18_lr1e4.pt
echo "[F6] sesrgb feed rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_rn50_lr1e3.pt
echo "[F6] sesrgb feed rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_rn50_lr1e4.pt
echo "[F6] sesrgb feed enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_enb0_lr1e3.pt
echo "[F6] sesrgb feed enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_enb0_lr1e4.pt
echo "[F6] sesrgb feed cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_cnxt_lr1e3.pt
echo "[F6] sesrgb feed cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_ses_rgb_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/sesrgb_feed_cnxt_lr1e4.pt

echo "[F6] DONE"
