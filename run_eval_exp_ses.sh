#!/bin/bash
# Eval all 32 SES models (pipeline b) -> exp_results/
set -e
cd "$(dirname "$0")"

for target in speed doc roughness feed_coarse; do
  for bb_short in rn18 rn50 enb0 cnxt; do
    case $bb_short in
      rn18) bb=resnet18 ;;
      rn50) bb=resnet50 ;;
      enb0) bb=efficientnet_b0 ;;
      cnxt) bb=convnext_tiny ;;
    esac
    for lr in lr1e3 lr1e4; do
      model="exp_models/ses_${target}_${bb_short}_${lr}.pt"
      out="exp_results/ses_${target}_${bb_short}_${lr}.md"
      echo "[eval-ses] $model"
      python cnn_model/eval_detailed.py --model "$model" --target "$target" --backbone "$bb" --pipeline b --save_md "$out"
    done
  done
done
echo "[eval-ses] DONE"
