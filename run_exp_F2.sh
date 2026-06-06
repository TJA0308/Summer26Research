#!/bin/bash
# F2: std doc (8) + ses doc (8)
set -e
cd "$(dirname "$0")"

echo "[F2] std doc rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_rn18_lr1e3.pt
echo "[F2] std doc rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_rn18_lr1e4.pt
echo "[F2] std doc rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_rn50_lr1e3.pt
echo "[F2] std doc rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_rn50_lr1e4.pt
echo "[F2] std doc enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_enb0_lr1e3.pt
echo "[F2] std doc enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_enb0_lr1e4.pt
echo "[F2] std doc cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_cnxt_lr1e3.pt
echo "[F2] std doc cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/std_doc_cnxt_lr1e4.pt

echo "[F2] ses doc rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_rn18_lr1e3.pt
echo "[F2] ses doc rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_rn18_lr1e4.pt
echo "[F2] ses doc rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_rn50_lr1e3.pt
echo "[F2] ses doc rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_rn50_lr1e4.pt
echo "[F2] ses doc enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_enb0_lr1e3.pt
echo "[F2] ses doc enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_enb0_lr1e4.pt
echo "[F2] ses doc cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-3 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_cnxt_lr1e3.pt
echo "[F2] ses doc cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-4 --smote --label_smooth 0.05 --mixup 0.2 --save exp_models_v2/ses_doc_cnxt_lr1e4.pt

echo "[F2] DONE"
