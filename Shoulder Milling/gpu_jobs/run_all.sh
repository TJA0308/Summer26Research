#!/usr/bin/env bash
set -euo pipefail
d="$(dirname "$0")"
bash "$d/00_repro_check.sh"
bash "$d/A_missing_lr1e-4.sh"
bash "$d/B_multiseed.sh"
bash "$d/C_nested_preproc.sh"
