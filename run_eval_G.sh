#!/bin/bash
# Eval all 64 ses4ch G-pipeline models -> exp_results_d/
set -e
cd "$(dirname "$0")"
mkdir -p exp_results_d

for variant in "" "smote_"; do
  tag="${variant:+smote_}"
  for target in speed doc roughness feed_coarse; do
    for bb_short in rn18 rn50 enb0 cnxt; do
      case $bb_short in
        rn18) bb=resnet18 ;;
        rn50) bb=resnet50 ;;
        enb0) bb=efficientnet_b0 ;;
        cnxt) bb=convnext_tiny ;;
      esac
      for lr in lr1e3 lr1e4; do
        # feed_coarse models saved as ses4ch_feed_* not ses4ch_feed_coarse_*
        if [ "$target" = "feed_coarse" ]; then
          model="exp_models_d/ses4ch_${tag}feed_${bb_short}_${lr}.pt"
        else
          model="exp_models_d/ses4ch_${tag}${target}_${bb_short}_${lr}.pt"
        fi
        out="exp_results_d/ses4ch_${tag}${target}_${bb_short}_${lr}.md"
        echo "[eval-G] $model"
        python cnn_model/eval_detailed.py \
          --model "$model" \
          --target "$target" \
          --backbone "$bb" \
          --pipeline b \
          --img_dir scalograms_ses_4ch_10w \
          --save_md "$out"
      done
    done
  done
done
echo "[eval-G] DONE"
