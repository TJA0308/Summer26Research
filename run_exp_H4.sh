#!/bin/bash
# H4: std_smote feed_coarse (8 jobs)
set -e
cd "$(dirname "$0")"
mkdir -p exp_models_d

echo "[H4] std_smote feed_coarse rn18 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet18 --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_rn18_lr1e3.pt --history exp_models_d/std_smote_feed_coarse_rn18_lr1e3_history.json
echo "[H4] std_smote feed_coarse rn18 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet18 --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_rn18_lr1e4.pt --history exp_models_d/std_smote_feed_coarse_rn18_lr1e4_history.json
echo "[H4] std_smote feed_coarse rn50 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet50 --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_rn50_lr1e3.pt --history exp_models_d/std_smote_feed_coarse_rn50_lr1e3_history.json
echo "[H4] std_smote feed_coarse rn50 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone resnet50 --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_rn50_lr1e4.pt --history exp_models_d/std_smote_feed_coarse_rn50_lr1e4_history.json
echo "[H4] std_smote feed_coarse enb0 lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone efficientnet_b0 --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_enb0_lr1e3.pt --history exp_models_d/std_smote_feed_coarse_enb0_lr1e3_history.json
echo "[H4] std_smote feed_coarse enb0 lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone efficientnet_b0 --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_enb0_lr1e4.pt --history exp_models_d/std_smote_feed_coarse_enb0_lr1e4_history.json
echo "[H4] std_smote feed_coarse cnxt lr1e-3"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone convnext_tiny --lr 1e-3 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_cnxt_lr1e3.pt --history exp_models_d/std_smote_feed_coarse_cnxt_lr1e3_history.json
echo "[H4] std_smote feed_coarse cnxt lr1e-4"
python cnn_model/cnn_train.py --img_dir scalograms_10w --target feed_coarse --backbone convnext_tiny --lr 1e-4 --epochs 33 --label_smooth 0.05 --mixup 0.2 --save exp_models_d/std_smote_feed_coarse_cnxt_lr1e4.pt --history exp_models_d/std_smote_feed_coarse_cnxt_lr1e4_history.json
echo "[H4] DONE"
