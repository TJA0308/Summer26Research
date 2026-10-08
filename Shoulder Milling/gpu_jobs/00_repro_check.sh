#!/usr/bin/env bash
# Repro check: doc / 32x12_residual_doc / seed 42 / lr 1e-3 must reproduce 95.8% (run_acc_soft 0.9583).
# Run FIRST. If it does not reproduce, STOP and do not run batches A/B.
set -euo pipefail
cd "$(dirname "$0")/.."
BATCH=repro
mkdir -p "cv_runs/$BATCH"
OUT="cv_runs/$BATCH/doc__32x12_residual_doc__lr1e-3__s42.csv"
python cv_evaluate.py --selftest
python cv_evaluate.py --img_dir scalograms_32x12_residual_doc --target doc --split loco \
  --models cnn --arch resnet18 --epochs 50 --lr 1e-3 --seeds 42 --out_csv "$OUT"
python - "$OUT" <<'PY'
import sys, pandas as pd
v = float(pd.read_csv(sys.argv[1]).run_acc_soft.iloc[-1])
print(f"run_acc_soft={v:.4f} (expected 0.9583)")
sys.exit(0 if abs(v - 0.9583) < 0.0006 else 1)
PY
echo "REPRO OK"
