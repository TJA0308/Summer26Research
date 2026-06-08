#!/bin/bash
# Eval all 32 std_smote (H-pipeline) models -> exp_results_a/
set -e
cd "$(dirname "$0")"
mkdir -p exp_results_a

for target in speed doc roughness feed_coarse; do
  for bb_short in rn18 rn50 enb0 cnxt; do
    case $bb_short in
      rn18) bb=resnet18 ;;
      rn50) bb=resnet50 ;;
      enb0) bb=efficientnet_b0 ;;
      cnxt) bb=convnext_tiny ;;
    esac
    for lr in lr1e3 lr1e4; do
      if [ "$target" = "feed_coarse" ]; then
        model="exp_models_d/std_smote_feed_coarse_${bb_short}_${lr}.pt"
      else
        model="exp_models_d/std_smote_${target}_${bb_short}_${lr}.pt"
      fi
      out="exp_results_a/std_smote_${target}_${bb_short}_${lr}.md"
      echo "[eval-H] $model"
      python cnn_model/eval_detailed.py \
        --model "$model" \
        --target "$target" \
        --backbone "$bb" \
        --pipeline a \
        --save_md "$out"
    done
  done
done
echo "[eval-H] DONE"
