# Cascade conditioning sweep for experimental splits exp11 and exp12.
# Mirrors run_cascade.ps1 + run_9win_sweep.ps1 for the original splits:
#   Stage 1 — train speed independently
#   Stage 2 — generate speed predictions, train doc conditioned on speed
#   Stage 3 — generate doc predictions, train feed conditioned on speed+doc
# Roughness does not use conditioning (no COND_PARENTS entry); it was already
# trained with/without SMOTE in run_exp_splits.ps1 and run_exp_splits_9win.ps1.
#
# Run from the Shoulder Milling directory:
#   .\run_cascade_exp.ps1

$ErrorActionPreference = "Continue"
$splits   = @("exp11", "exp12")
$img_dirs = @("scalograms_32x12", "scalograms_32x3",
              "scalograms_32x12_9win", "scalograms_32x3_9win")
$archs    = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs      = @("1e-3", "1e-4")
$n_combo  = $archs.Count * $lrs.Count   # 8

foreach ($split in $splits) {
    $run_tag = "${split}_cascade"
    Write-Host "`n==============================" -ForegroundColor Magenta
    Write-Host "  SPLIT: $split  (run_tag=$run_tag)" -ForegroundColor Magenta
    Write-Host "==============================`n" -ForegroundColor Magenta

    foreach ($img_dir in $img_dirs) {
        $scalo_tag = $img_dir -replace "scalograms_", ""
        Write-Host "--- $img_dir ---" -ForegroundColor Green

        # ── Stage 1: speed ───────────────────────────────────────────────────
        Write-Host "  [Stage 1] speed" -ForegroundColor Yellow
        $i = 0
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "    [$i/$n_combo] $arch lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target speed --img_dir $img_dir `
                    --arch $arch --lr $lr --epochs 50 `
                    --split_id $split --run_tag $run_tag --no_smote
                if ($LASTEXITCODE -ne 0) { Write-Host "    ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }

        # Generate speed conditioning CSV → speed_pred_<scalo>_<run_tag>.csv
        Write-Host "  [Stage 1] generating speed predictions..." -ForegroundColor Yellow
        python predict_conditioning.py --target speed --img_dir $img_dir --run_tag $run_tag
        if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR generating speed predictions" -ForegroundColor Red }

        # ── Stage 2: doc (auto-conditions on speed predictions) ──────────────
        Write-Host "  [Stage 2] doc (conditioned on speed)" -ForegroundColor Yellow
        $i = 0
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "    [$i/$n_combo] $arch lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target doc --img_dir $img_dir `
                    --arch $arch --lr $lr --epochs 50 `
                    --split_id $split --run_tag $run_tag --no_smote
                if ($LASTEXITCODE -ne 0) { Write-Host "    ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }

        # Generate doc conditioning CSV → doc_pred_<scalo>_<run_tag>.csv
        Write-Host "  [Stage 2] generating doc predictions..." -ForegroundColor Yellow
        python predict_conditioning.py --target doc --img_dir $img_dir --run_tag $run_tag
        if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR generating doc predictions" -ForegroundColor Red }

        # ── Stage 3: feed (auto-conditions on speed + doc predictions) ───────
        Write-Host "  [Stage 3] feed (conditioned on speed+doc)" -ForegroundColor Yellow
        $i = 0
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "    [$i/$n_combo] $arch lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target feed --img_dir $img_dir `
                    --arch $arch --lr $lr --epochs 50 `
                    --split_id $split --run_tag $run_tag --no_smote
                if ($LASTEXITCODE -ne 0) { Write-Host "    ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }
    }
}

# ── Eval all cascade models ───────────────────────────────────────────────────
Write-Host "`n=== EVAL cascade ===" -ForegroundColor Green
$cascade_targets = @("speed", "doc", "feed")
$total = $splits.Count * $cascade_targets.Count * $img_dirs.Count * $archs.Count * $lrs.Count
$i = 0
foreach ($split in $splits) {
    $run_tag = "${split}_cascade"
    foreach ($target in $cascade_targets) {
        foreach ($img_dir in $img_dirs) {
            $scalo_tag = $img_dir -replace "scalograms_", ""
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    $lr_fmt     = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                    $model_path = "models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}_${run_tag}_best.pt"
                    Write-Host "[$i/$total] eval $split | $target | $img_dir | $arch | lr=$lr" -ForegroundColor Cyan
                    python eval_detailed_param.py --target $target --img_dir $img_dir `
                        --arch $arch --lr $lr --split_id $split --run_tag $run_tag `
                        --model $model_path
                    if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }
        }
    }
}

Write-Host "`nAll done. Results in exp_results_*_exp11_cascade/ and exp_results_*_exp12_cascade/." -ForegroundColor Green
