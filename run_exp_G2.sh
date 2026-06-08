#!/bin/bash
# G2: ses4ch doc (8 no-smote + 8 smote = 16 jobs)
set -e
cd "$(dirname "$0")"
mkdir -p exp_models_d

echo "[G2] ses4ch doc rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_rn18_lr1e3.pt --history exp_models_d/ses4ch_doc_rn18_lr1e3_history.json
echo "[G2] ses4ch doc rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_rn18_lr1e4.pt --history exp_models_d/ses4ch_doc_rn18_lr1e4_history.json
echo "[G2] ses4ch doc rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_rn50_lr1e3.pt --history exp_models_d/ses4ch_doc_rn50_lr1e3_history.json
echo "[G2] ses4ch doc rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_rn50_lr1e4.pt --history exp_models_d/ses4ch_doc_rn50_lr1e4_history.json
echo "[G2] ses4ch doc enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_enb0_lr1e3.pt --history exp_models_d/ses4ch_doc_enb0_lr1e3_history.json
echo "[G2] ses4ch doc enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_enb0_lr1e4.pt --history exp_models_d/ses4ch_doc_enb0_lr1e4_history.json
echo "[G2] ses4ch doc cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_cnxt_lr1e3.pt --history exp_models_d/ses4ch_doc_cnxt_lr1e3_history.json
echo "[G2] ses4ch doc cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --save exp_models_d/ses4ch_doc_cnxt_lr1e4.pt --history exp_models_d/ses4ch_doc_cnxt_lr1e4_history.json

echo "[G2] ses4ch smote doc rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_rn18_lr1e3.pt --history exp_models_d/ses4ch_smote_doc_rn18_lr1e3_history.json
echo "[G2] ses4ch smote doc rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet18 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_rn18_lr1e4.pt --history exp_models_d/ses4ch_smote_doc_rn18_lr1e4_history.json
echo "[G2] ses4ch smote doc rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_rn50_lr1e3.pt --history exp_models_d/ses4ch_smote_doc_rn50_lr1e3_history.json
echo "[G2] ses4ch smote doc rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone resnet50 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_rn50_lr1e4.pt --history exp_models_d/ses4ch_smote_doc_rn50_lr1e4_history.json
echo "[G2] ses4ch smote doc enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_enb0_lr1e3.pt --history exp_models_d/ses4ch_smote_doc_enb0_lr1e3_history.json
echo "[G2] ses4ch smote doc enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_enb0_lr1e4.pt --history exp_models_d/ses4ch_smote_doc_enb0_lr1e4_history.json
echo "[G2] ses4ch smote doc cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_cnxt_lr1e3.pt --history exp_models_d/ses4ch_smote_doc_cnxt_lr1e3_history.json
echo "[G2] ses4ch smote doc cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target doc --backbone convnext_tiny --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --smote --save exp_models_d/ses4ch_smote_doc_cnxt_lr1e4.pt --history exp_models_d/ses4ch_smote_doc_cnxt_lr1e4_history.json

echo "[G2] DONE"
