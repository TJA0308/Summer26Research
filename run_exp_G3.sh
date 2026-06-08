#!/bin/bash
# G3: ses4ch roughness (8 no-smote + 8 smote = 16 jobs)
set -e
cd "$(dirname "$0")"
mkdir -p exp_models_d

echo "[G3] ses4ch roughness rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_rn18_lr1e3.pt --history exp_models_d/ses4ch_roughness_rn18_lr1e3_history.json
echo "[G3] ses4ch roughness rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_rn18_lr1e4.pt --history exp_models_d/ses4ch_roughness_rn18_lr1e4_history.json
echo "[G3] ses4ch roughness rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_rn50_lr1e3.pt --history exp_models_d/ses4ch_roughness_rn50_lr1e3_history.json
echo "[G3] ses4ch roughness rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_rn50_lr1e4.pt --history exp_models_d/ses4ch_roughness_rn50_lr1e4_history.json
echo "[G3] ses4ch roughness enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_enb0_lr1e3.pt --history exp_models_d/ses4ch_roughness_enb0_lr1e3_history.json
echo "[G3] ses4ch roughness enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_enb0_lr1e4.pt --history exp_models_d/ses4ch_roughness_enb0_lr1e4_history.json
echo "[G3] ses4ch roughness cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_cnxt_lr1e3.pt --history exp_models_d/ses4ch_roughness_cnxt_lr1e3_history.json
echo "[G3] ses4ch roughness cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_roughness_cnxt_lr1e4.pt --history exp_models_d/ses4ch_roughness_cnxt_lr1e4_history.json

echo "[G3] ses4ch smote roughness rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_rn18_lr1e3.pt --history exp_models_d/ses4ch_smote_roughness_rn18_lr1e3_history.json
echo "[G3] ses4ch smote roughness rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet18 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_rn18_lr1e4.pt --history exp_models_d/ses4ch_smote_roughness_rn18_lr1e4_history.json
echo "[G3] ses4ch smote roughness rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_rn50_lr1e3.pt --history exp_models_d/ses4ch_smote_roughness_rn50_lr1e3_history.json
echo "[G3] ses4ch smote roughness rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone resnet50 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_rn50_lr1e4.pt --history exp_models_d/ses4ch_smote_roughness_rn50_lr1e4_history.json
echo "[G3] ses4ch smote roughness enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_enb0_lr1e3.pt --history exp_models_d/ses4ch_smote_roughness_enb0_lr1e3_history.json
echo "[G3] ses4ch smote roughness enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_enb0_lr1e4.pt --history exp_models_d/ses4ch_smote_roughness_enb0_lr1e4_history.json
echo "[G3] ses4ch smote roughness cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_cnxt_lr1e3.pt --history exp_models_d/ses4ch_smote_roughness_cnxt_lr1e3_history.json
echo "[G3] ses4ch smote roughness cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target roughness --backbone convnext_tiny --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_roughness_cnxt_lr1e4.pt --history exp_models_d/ses4ch_smote_roughness_cnxt_lr1e4_history.json

echo "[G3] DONE"
