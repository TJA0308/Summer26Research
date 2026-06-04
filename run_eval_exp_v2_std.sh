#!/bin/bash
# Eval all 32 std CWT v2 models (pipeline a) -> exp_results_v2/
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
      model="exp_models_v2/std_${target}_${bb_short}_${lr}.pt"
      out="exp_results_v2/std_${target}_${bb_short}_${lr}.md"
      echo "[eval-std-v2] $model"
      python cnn_model/eval_detailed.py --model "$model" --target "$target" --backbone "$bb" --pipeline a --save_md "$out"
    done
  done
done
echo "[eval-std-v2] DONE"
