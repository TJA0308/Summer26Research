#!/bin/bash
# Fix eval for feed_coarse models (filename uses 'feed', target arg uses 'feed_coarse')
set -e
cd "$(dirname "$0")"

for pip_short in std ses; do
  case $pip_short in
    std) pipeline=a ;;
    ses) pipeline=b ;;
  esac
  for bb_short in rn18 rn50 enb0 cnxt; do
    case $bb_short in
      rn18) bb=resnet18 ;;
      rn50) bb=resnet50 ;;
      enb0) bb=efficientnet_b0 ;;
      cnxt) bb=convnext_tiny ;;
    esac
    for lr in lr1e3 lr1e4; do
      model="exp_models_v2/${pip_short}_feed_${bb_short}_${lr}.pt"
      out="exp_results_v2/${pip_short}_feed_coarse_${bb_short}_${lr}.md"
      echo "[eval-feed-fix] $model"
      python cnn_model/eval_detailed.py --model "$model" --target feed_coarse --backbone "$bb" --pipeline "$pipeline" --save_md "$out"
    done
  done
done
echo "[eval-feed-fix] DONE"
