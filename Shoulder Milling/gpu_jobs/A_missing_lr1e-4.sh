#!/usr/bin/env bash
# Batch A: only cells that find_missing_runs.py reports as MISSING/MISMATCH.
# As of writing, all 48 section-4 cells match (lr=1e-4 already in cv_summary.csv).
# Re-run `python find_missing_runs.py` and add "<target>|<group>|<scalogram>|<lr>" lines below.
# Currently listed: roughness/secondary/32x12_feedopt_9win has NO lr=1e-3 row (only lr=1e-4 exists).
set -euo pipefail
cd "$(dirname "$0")/.."
BATCH=A
mkdir -p "cv_runs/$BATCH"
JOBS=(
  "roughness|secondary|32x12_feedopt_9win|1e-3"
)
for j in "${JOBS[@]}"; do
  IFS='|' read -r T G S LR <<<"$j"
  OUT="cv_runs/$BATCH/${T}__${S}__lr${LR}__s42.csv"
  [ -s "$OUT" ] && { echo "skip $OUT"; continue; }
  EXTRA=(); [ "$T" = roughness ] && EXTRA=(--roughness_group "$G")
  python cv_evaluate.py --img_dir "scalograms_$S" --target "$T" --split loco "${EXTRA[@]}" \
    --models cnn --arch resnet18 --epochs 50 --lr "$LR" --seeds 42 --out_csv "$OUT"
done
