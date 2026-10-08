#!/usr/bin/env bash
# Batch C: fold-nested preprocessing variants (NEW variants, so seed 42 is NOT a selection seed).
# resnet18, 50 epochs, lr 1e-3, seeds 42 43 44 45 46.  Needs fullscale_cwt/ cache for feedopt_nested.
# Base dirs must be the 72-window dirs (the *_9win dirs have ragged image widths and are not supported).
set -euo pipefail
cd "$(dirname "$0")/.."
BATCH=C
mkdir -p "cv_runs/$BATCH"
JOBS=(
  "feedopt_nested|feed|32x3_feedopt"
  "feedopt_nested|roughness|32x12_feedopt"
  "residual_inductive|speed|32x12"
  "residual_inductive|doc|32x12"
  "residual_inductive|feed|32x3"
  "residual_inductive|roughness|32x12"
)
for j in "${JOBS[@]}"; do
  IFS='|' read -r P T S <<<"$j"
  OUT="cv_runs/$BATCH/${T}__${S}__${P}__lr1e-3__s42-46.csv"
  [ -s "$OUT" ] && { echo "skip $OUT"; continue; }
  EXTRA=(); [ "$T" = roughness ] && EXTRA=(--roughness_group primary)
  python cv_evaluate.py --img_dir "scalograms_$S" --target "$T" --split loco "${EXTRA[@]}" \
    --preproc "$P" --models cnn --arch resnet18 --epochs 50 --lr 1e-3 \
    --seeds 42 43 44 45 46 --out_csv "$OUT"
done
