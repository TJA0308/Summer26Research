#!/bin/bash
# G1: ses4ch speed (8 no-smote + 8 smote = 16 jobs)
set -e
cd "$(dirname "$0")"
mkdir -p exp_models_d

echo "[G1] ses4ch speed rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_rn18_lr1e3.pt --history exp_models_d/ses4ch_speed_rn18_lr1e3_history.json
echo "[G1] ses4ch speed rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_rn18_lr1e4.pt --history exp_models_d/ses4ch_speed_rn18_lr1e4_history.json
echo "[G1] ses4ch speed rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_rn50_lr1e3.pt --history exp_models_d/ses4ch_speed_rn50_lr1e3_history.json
echo "[G1] ses4ch speed rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_rn50_lr1e4.pt --history exp_models_d/ses4ch_speed_rn50_lr1e4_history.json
echo "[G1] ses4ch speed enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_enb0_lr1e3.pt --history exp_models_d/ses4ch_speed_enb0_lr1e3_history.json
echo "[G1] ses4ch speed enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_enb0_lr1e4.pt --history exp_models_d/ses4ch_speed_enb0_lr1e4_history.json
echo "[G1] ses4ch speed cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_cnxt_lr1e3.pt --history exp_models_d/ses4ch_speed_cnxt_lr1e3_history.json
echo "[G1] ses4ch speed cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_speed_cnxt_lr1e4.pt --history exp_models_d/ses4ch_speed_cnxt_lr1e4_history.json

echo "[G1] ses4ch smote speed rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_rn18_lr1e3.pt --history exp_models_d/ses4ch_smote_speed_rn18_lr1e3_history.json
echo "[G1] ses4ch smote speed rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet18 --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_rn18_lr1e4.pt --history exp_models_d/ses4ch_smote_speed_rn18_lr1e4_history.json
echo "[G1] ses4ch smote speed rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_rn50_lr1e3.pt --history exp_models_d/ses4ch_smote_speed_rn50_lr1e3_history.json
echo "[G1] ses4ch smote speed rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone resnet50 --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_rn50_lr1e4.pt --history exp_models_d/ses4ch_smote_speed_rn50_lr1e4_history.json
echo "[G1] ses4ch smote speed enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_enb0_lr1e3.pt --history exp_models_d/ses4ch_smote_speed_enb0_lr1e3_history.json
echo "[G1] ses4ch smote speed enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone efficientnet_b0 --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_enb0_lr1e4.pt --history exp_models_d/ses4ch_smote_speed_enb0_lr1e4_history.json
echo "[G1] ses4ch smote speed cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_cnxt_lr1e3.pt --history exp_models_d/ses4ch_smote_speed_cnxt_lr1e3_history.json
echo "[G1] ses4ch smote speed cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target speed --backbone convnext_tiny --epochs 30 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_speed_cnxt_lr1e4.pt --history exp_models_d/ses4ch_smote_speed_cnxt_lr1e4_history.json

echo "[G1] DONE"
