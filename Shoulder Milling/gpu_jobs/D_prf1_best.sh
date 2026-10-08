#!/usr/bin/env bash
# Batch D: re-run the README's best configs WITH per-window predictions saved, so precision /
# recall / F1 can be computed (compute_prf1.py). lr 1e-3, resnet18, 50 epochs, LOCO.
#   Block 1: best-of-16 per target (seed 42) + the two "best without residual" configs.
#   Block 2: plain 32x12 baseline (seeds 42-46) = the generalization counterpart.
# A GPU re-run may not reproduce the seed-42 accuracies in cv_summary.csv bit-for-bit; the README
# must quote the accuracy from THIS run next to its P/R/F1 and note any difference.
set -euo pipefail
cd "$(dirname "$0")/.."
BATCH=D
mkdir -p "cv_runs/$BATCH" cv_preds/cnn

run() {  # target scalogram seeds...
  local T="$1" S="$2"; shift 2
  local TAG; TAG=$(echo "$*" | tr ' ' '-')
  local OUT="cv_runs/$BATCH/${T}__${S}__lr1e-3__s${TAG}.csv"
  [ -s "$OUT" ] && { echo "skip $OUT"; return; }
  local EXTRA=(); [ "$T" = roughness ] && EXTRA=(--roughness_group primary)
  python cv_evaluate.py --img_dir "scalograms_$S" --target "$T" --split loco "${EXTRA[@]}" \
    --models cnn --arch resnet18 --epochs 50 --lr 1e-3 --seeds "$@" \
    --save_preds cv_preds/cnn --out_csv "$OUT"
}

# Block 1: best configs, seed 42
run speed     32x12_9win               42
run doc       32x12_residual_doc       42
run feed      32x3_residual_roughness  42
run roughness 32x12_feedopt_9win       42
run doc       32x3_feedopt_9win        42   # best doc WITHOUT residual preprocessing
run feed      32x3_9win                42   # best feed WITHOUT residual preprocessing

# Block 2: plain 32x12 baseline, 5 seeds (optional but needed for the generalization column)
for T in speed doc feed roughness; do
  run "$T" 32x12 42 43 44 45 46
done

python compute_prf1.py "cv_preds/cnn/*.csv" --out_md cv_preds/cnn_prf1.md
echo "wrote cv_preds/cnn_prf1.md"
