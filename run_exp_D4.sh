#!/bin/bash
# D4: Feed Coarse — std (8 jobs) + SES (8 jobs)
set -e
cd "$(dirname "$0")"

echo "[D4] std feed rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_rn18_lr1e3.pt

echo "[D4] std feed rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_rn18_lr1e4.pt

echo "[D4] std feed rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_rn50_lr1e3.pt

echo "[D4] std feed rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_rn50_lr1e4.pt

echo "[D4] std feed enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_enb0_lr1e3.pt

echo "[D4] std feed enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_enb0_lr1e4.pt

echo "[D4] std feed cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_cnxt_lr1e3.pt

echo "[D4] std feed cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-4 --augment light --optimizer adamw --scheduler cosine --split balanced --weighted_loss --save exp_models/std_feed_cnxt_lr1e4.pt

echo "[D4] ses feed rn18 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-3 --smote --weighted_loss --save exp_models/ses_feed_rn18_lr1e3.pt

echo "[D4] ses feed rn18 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet18 --epochs 33 --lr 1e-4 --smote --weighted_loss --save exp_models/ses_feed_rn18_lr1e4.pt

echo "[D4] ses feed rn50 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-3 --smote --weighted_loss --save exp_models/ses_feed_rn50_lr1e3.pt

echo "[D4] ses feed rn50 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone resnet50 --epochs 33 --lr 1e-4 --smote --weighted_loss --save exp_models/ses_feed_rn50_lr1e4.pt

echo "[D4] ses feed enb0 lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-3 --smote --weighted_loss --save exp_models/ses_feed_enb0_lr1e3.pt

echo "[D4] ses feed enb0 lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone efficientnet_b0 --epochs 33 --lr 1e-4 --smote --weighted_loss --save exp_models/ses_feed_enb0_lr1e4.pt

echo "[D4] ses feed cnxt lr1e-3"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-3 --smote --weighted_loss --save exp_models/ses_feed_cnxt_lr1e3.pt

echo "[D4] ses feed cnxt lr1e-4"
python cnn_model/cnn_train_hilbert.py --img_dir scalograms_ses_10w --target feed_coarse --backbone convnext_tiny --epochs 33 --lr 1e-4 --smote --weighted_loss --save exp_models/ses_feed_cnxt_lr1e4.pt

echo "[D4] DONE"
