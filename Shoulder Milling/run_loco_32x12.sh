#!/usr/bin/env bash
# LOCO cross-validation sweep — scalograms_32x12, resnet18, 5 seeds
# Run from the "Shoulder Milling" directory on a GPU instance (T4 recommended).
# Total wall time: ~1 hr on a T4.

set -e
cd "$(dirname "$0")"

# ------------------------------------------------------------------
# 1. Sanity check (seconds, no training)
# ------------------------------------------------------------------
python cv_evaluate.py --selftest

# ------------------------------------------------------------------
# 2. Pre-flight: reproduce standard-split number for each target
#    (~15-30 sec/target on T4)
# ------------------------------------------------------------------
for t in speed feed doc roughness; do
    python cv_evaluate.py \
        --img_dir scalograms_32x12 \
        --target "$t" \
        --split standard \
        --models cnn \
        --arch resnet18 \
        --epochs 50
done

# ------------------------------------------------------------------
# 3. Full LOCO sweep — 5 seeds, speed / feed / doc
# ------------------------------------------------------------------
for t in speed feed doc; do
    python cv_evaluate.py \
        --img_dir scalograms_32x12 \
        --target "$t" \
        --models cnn \
        --arch resnet18 \
        --epochs 50 \
        --seeds 42 43 44 45 46
done

# ------------------------------------------------------------------
# 4. Roughness LOCO — primary grouping (by doc)
# ------------------------------------------------------------------
python cv_evaluate.py \
    --img_dir scalograms_32x12 \
    --target roughness \
    --models cnn \
    --arch resnet18 \
    --epochs 50 \
    --seeds 42 43 44 45 46

# ------------------------------------------------------------------
# 5. Roughness LOCO — secondary grouping (by speed x feed)
# ------------------------------------------------------------------
python cv_evaluate.py \
    --img_dir scalograms_32x12 \
    --target roughness \
    --models cnn \
    --arch resnet18 \
    --epochs 50 \
    --seeds 42 43 44 45 46 \
    --roughness_group secondary
