#!/bin/bash
# D1: Speed — std (8 jobs) + SES (8 jobs)
set -e
cd "$(dirname "$0")"

echo "[D1] std speed rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_rn18_lr1e3.pt

echo "[D1] std speed rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_rn18_lr1e4.pt

echo "[D1] std speed rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_rn50_lr1e3.pt

echo "[D1] std speed rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_rn50_lr1e4.pt

echo "[D1] std speed enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_enb0_lr1e3.pt

echo "[D1] std speed enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_enb0_lr1e4.pt

echo "[D1] std speed cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_cnxt_lr1e3.pt

echo "[D1] std speed cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --save exp_models/std_speed_cnxt_lr1e4.pt

echo "[D1] ses speed rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --smote --save exp_models/ses_speed_rn18_lr1e3.pt

echo "[D1] ses speed rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-4 --smote --save exp_models/ses_speed_rn18_lr1e4.pt

echo "[D1] ses speed rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-3 --smote --save exp_models/ses_speed_rn50_lr1e3.pt

echo "[D1] ses speed rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-4 --smote --save exp_models/ses_speed_rn50_lr1e4.pt

echo "[D1] ses speed enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --smote --save exp_models/ses_speed_enb0_lr1e3.pt

echo "[D1] ses speed enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --smote --save exp_models/ses_speed_enb0_lr1e4.pt

echo "[D1] ses speed cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --smote --save exp_models/ses_speed_cnxt_lr1e3.pt

echo "[D1] ses speed cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-4 --smote --save exp_models/ses_speed_cnxt_lr1e4.pt

echo "[D1] DONE"
