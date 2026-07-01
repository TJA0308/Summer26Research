# Cascade conditioning sweep for experimental splits exp11 and exp12,
# combining the two strongest levers found so far for feed:
#   - feed-correlated scale selection (feedopt scalograms)
#   - 9-window sub-splitting + cascade conditioning (speed -> doc -> feed)
# Mirrors run_cascade_exp.ps1 (regular splits) and run_feedopt_9win_cascade.ps1
# (base split, no exp11/exp12), but combines both to test whether the
# feedopt+9win project-best (87.5% feed run accuracy) holds up on the
# harder, cross-target-balanced exp11/exp12 test sets.
#
# Naming matches the existing exp11/exp12 9win cascade convention:
#   run_tag = <split>            (e.g. "exp11")   -- no-SMOTE cascade
#   run_tag = <split>_smote       (e.g. "exp11_smote") -- SMOTE cascade
# Results land in exp_results_<scalo_tag>_<split>/ (per eval_detailed_param.py
# default). Move/rename to _cascading to match the existing convention once
# training is done, e.g.:
#   mv exp_results_32x12_feedopt_9win_exp11 exp_results_32x12_feedopt_9win_exp11_cascading
#
# Run from the Shoulder Milling directory:
#   .\run_cascade_exp_feedopt_9win.ps1

$ErrorActionPreference = "Continue"
$splits   = @("exp11", "exp12")
$img_dirs = @("scalograms_32x12_feedopt_9win", "scalograms_32x3_feedopt_9win")
$archs    = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs      = @("1e-3", "1e-4")
$n_combo  = $archs.Count * $lrs.Count   # 8

foreach ($split in $splits) {
    foreach ($smote_mode in @($false, $true)) {
        $run_tag = if ($smote_mode) { "${split}_smote" } else { $split }
        Write-Host "`n==============================" -ForegroundColor Magenta
        Write-Host "  SPLIT: $split  SMOTE: $smote_mode  (run_tag=$run_tag)" -ForegroundColor Magenta
        Write-Host "==============================`n" -ForegroundColor Magenta

        foreach ($img_dir in $img_dirs) {
            Write-Host "--- $img_dir ---" -ForegroundColor Green

            # ── Stage 1: speed ───────────────────────────────────────────────
            Write-Host "  [Stage 1] speed" -ForegroundColor Yellow
            $i = 0
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    Write-Host "    [$i/$n_combo] $arch lr=$lr" -ForegroundColor Cyan
                    if ($smote_mode) {
                        python cnn_train_param.py --target speed --img_dir $img_dir `
                            --arch $arch --lr $lr --epochs 50 `
                            --split_id $split --run_tag $run_tag
                    } else {
                        python cnn_train_param.py --target speed --img_dir $img_dir `
                            --arch $arch --lr $lr --epochs 50 `
                            --split_id $split --run_tag $run_tag --no_smote
                    }
                    if ($LASTEXITCODE -ne 0) { Write-Host "    ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }

            # Generate speed conditioning CSV -> speed_pred_<scalo>_<run_tag>.csv
            Write-Host "  [Stage 1] generating speed predictions..." -ForegroundColor Yellow
            python predict_conditioning.py --target speed --img_dir $img_dir --run_tag $run_tag
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR generating speed predictions" -ForegroundColor Red }

            # ── Stage 2: doc (auto-conditions on speed predictions) ──────────
            Write-Host "  [Stage 2] doc (conditioned on speed)" -ForegroundColor Yellow
            $i = 0
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    Write-Host "    [$i/$n_combo] $arch lr=$lr" -ForegroundColor Cyan
                    if ($smote_mode) {
                        python cnn_train_param.py --target doc --img_dir $img_dir `
                            --arch $arch --lr $lr --epochs 50 `
                            --split_id $split --run_tag $run_tag
                    } else {
                        python cnn_train_param.py --target doc --img_dir $img_dir `
                            --arch $arch --lr $lr --epochs 50 `
                            --split_id $split --run_tag $run_tag --no_smote
                    }
                    if ($LASTEXITCODE -ne 0) { Write-Host "    ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }

            # Generate doc conditioning CSV -> doc_pred_<scalo>_<run_tag>.csv
            Write-Host "  [Stage 2] generating doc predictions..." -ForegroundColor Yellow
            python predict_conditioning.py --target doc --img_dir $img_dir --run_tag $run_tag
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR generating doc predictions" -ForegroundColor Red }

            # ── Stage 3: feed (auto-conditions on speed + doc predictions) ───
            Write-Host "  [Stage 3] feed (conditioned on speed+doc)" -ForegroundColor Yellow
            $i = 0
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    Write-Host "    [$i/$n_combo] $arch lr=$lr" -ForegroundColor Cyan
                    if ($smote_mode) {
                        python cnn_train_param.py --target feed --img_dir $img_dir `
                            --arch $arch --lr $lr --epochs 50 `
                            --split_id $split --run_tag $run_tag
                    } else {
                        python cnn_train_param.py --target feed --img_dir $img_dir `
                            --arch $arch --lr $lr --epochs 50 `
                            --split_id $split --run_tag $run_tag --no_smote
                    }
                    if ($LASTEXITCODE -ne 0) { Write-Host "    ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }
        }
    }
}

# ── Eval all cascade models ───────────────────────────────────────────────────
Write-Host "`n=== EVAL cascade ===" -ForegroundColor Green
$cascade_targets = @("speed", "doc", "feed")
$total = $splits.Count * 2 * $cascade_targets.Count * $img_dirs.Count * $archs.Count * $lrs.Count
$i = 0
foreach ($split in $splits) {
    foreach ($smote_mode in @($false, $true)) {
        $run_tag = if ($smote_mode) { "${split}_smote" } else { $split }
        foreach ($target in $cascade_targets) {
            foreach ($img_dir in $img_dirs) {
                $scalo_tag = $img_dir -replace "scalograms_", ""
                foreach ($arch in $archs) {
                    foreach ($lr in $lrs) {
                        $i++
                        $lr_fmt     = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                        $model_path = "models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}_${run_tag}_best.pt"
                        Write-Host "[$i/$total] eval $split | smote=$smote_mode | $target | $img_dir | $arch | lr=$lr" -ForegroundColor Cyan
                        python eval_detailed_param.py --target $target --img_dir $img_dir `
                            --arch $arch --lr $lr --split_id $split --run_tag $run_tag `
                            --model $model_path
                        if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                    }
                }
            }
        }
    }
}

Write-Host "`nAll done. Results in exp_results_32x12_feedopt_9win_exp11/, exp_results_32x12_feedopt_9win_exp12/, and 32x3 equivalents." -ForegroundColor Green
Write-Host "Rename to _cascading suffix to match the existing exp11/exp12 9win convention if desired." -ForegroundColor Green
