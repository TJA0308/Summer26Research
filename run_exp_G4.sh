#!/bin/bash
# G4: ses4ch feed_coarse (8 no-smote + 8 smote = 16 jobs)
set -e
cd "$(dirname "$0")"
mkdir -p exp_models_d

echo "[G4] ses4ch feed rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_rn18_lr1e3.pt --history exp_models_d/ses4ch_feed_rn18_lr1e3_history.json
echo "[G4] ses4ch feed rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_rn18_lr1e4.pt --history exp_models_d/ses4ch_feed_rn18_lr1e4_history.json
echo "[G4] ses4ch feed rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_rn50_lr1e3.pt --history exp_models_d/ses4ch_feed_rn50_lr1e3_history.json
echo "[G4] ses4ch feed rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_rn50_lr1e4.pt --history exp_models_d/ses4ch_feed_rn50_lr1e4_history.json
echo "[G4] ses4ch feed enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_enb0_lr1e3.pt --history exp_models_d/ses4ch_feed_enb0_lr1e3_history.json
echo "[G4] ses4ch feed enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_enb0_lr1e4.pt --history exp_models_d/ses4ch_feed_enb0_lr1e4_history.json
echo "[G4] ses4ch feed cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_cnxt_lr1e3.pt --history exp_models_d/ses4ch_feed_cnxt_lr1e3_history.json
echo "[G4] ses4ch feed cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --save exp_models_d/ses4ch_feed_cnxt_lr1e4.pt --history exp_models_d/ses4ch_feed_cnxt_lr1e4_history.json

echo "[G4] ses4ch smote feed rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_rn18_lr1e3.pt --history exp_models_d/ses4ch_smote_feed_rn18_lr1e3_history.json
echo "[G4] ses4ch smote feed rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_rn18_lr1e4.pt --history exp_models_d/ses4ch_smote_feed_rn18_lr1e4_history.json
echo "[G4] ses4ch smote feed rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_rn50_lr1e3.pt --history exp_models_d/ses4ch_smote_feed_rn50_lr1e3_history.json
echo "[G4] ses4ch smote feed rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_rn50_lr1e4.pt --history exp_models_d/ses4ch_smote_feed_rn50_lr1e4_history.json
echo "[G4] ses4ch smote feed enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_enb0_lr1e3.pt --history exp_models_d/ses4ch_smote_feed_enb0_lr1e3_history.json
echo "[G4] ses4ch smote feed enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_enb0_lr1e4.pt --history exp_models_d/ses4ch_smote_feed_enb0_lr1e4_history.json
echo "[G4] ses4ch smote feed cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_cnxt_lr1e3.pt --history exp_models_d/ses4ch_smote_feed_cnxt_lr1e3_history.json
echo "[G4] ses4ch smote feed cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_4ch_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-4 --optimizer adamw --scheduler cosine --label_smooth 0.05 --mixup 0.2 --weighted_loss --smote --save exp_models_d/ses4ch_smote_feed_cnxt_lr1e4.pt --history exp_models_d/ses4ch_smote_feed_cnxt_lr1e4_history.json

echo "[G4] DONE"
