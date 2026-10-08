#!/usr/bin/env bash
# Batch B: seeds 43 44 45 46 for the four pre-registered configs (lr 1e-3, resnet18, 50 epochs).
# Seed 42 already exists in cv_summary.csv. One CSV per config (4 rows each).
set -euo pipefail
cd "$(dirname "$0")/.."
BATCH=B
mkdir -p "cv_runs/$BATCH"
JOBS=(
  "speed|32x12_9win"
  "doc|32x12_residual_doc"
  "feed|32x3_residual_roughness"
  "roughness|32x12_feedopt_9win"
)
for j in "${JOBS[@]}"; do
  IFS='|' read -r T S <<<"$j"
  OUT="cv_runs/$BATCH/${T}__${S}__lr1e-3__s43-44-45-46.csv"
  [ -s "$OUT" ] && { echo "skip $OUT"; continue; }
  EXTRA=(); [ "$T" = roughness ] && EXTRA=(--roughness_group primary)
  python cv_evaluate.py --img_dir "scalograms_$S" --target "$T" --split loco "${EXTRA[@]}" \
    --models cnn --arch resnet18 --epochs 50 --lr 1e-3 --seeds 43 44 45 46 --out_csv "$OUT"
done
