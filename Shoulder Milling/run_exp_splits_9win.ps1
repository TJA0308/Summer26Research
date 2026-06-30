$ErrorActionPreference = "Continue"
$targets  = @("speed", "feed", "doc", "roughness")
$img_dirs = @("scalograms_32x12_9win", "scalograms_32x3_9win")
$archs    = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs      = @("1e-3", "1e-4")
$splits   = @("exp11", "exp12")

# ── 1. Generate SMOTE for each split x 9win scalogram dir ─────────────────────
Write-Host "`n=== SMOTE generation (9win) ===" -ForegroundColor Yellow
foreach ($split in $splits) {
    foreach ($img_dir in $img_dirs) {
        Write-Host "  smote | $split | $img_dir" -ForegroundColor Cyan
        python smote_generate_param.py --split_id $split --img_dir $img_dir
        if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
    }
}

# ── 2. Train: no SMOTE ────────────────────────────────────────────────────────
# Total: 2 splits x 4 targets x 2 dirs x 4 archs x 2 lrs = 128
Write-Host "`n=== TRAIN (no SMOTE) ===" -ForegroundColor Yellow
$total = $splits.Count * $targets.Count * $img_dirs.Count * $archs.Count * $lrs.Count
$i = 0
foreach ($split in $splits) {
    foreach ($target in $targets) {
        foreach ($img_dir in $img_dirs) {
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    Write-Host "[$i/$total] $split | $target | $img_dir | $arch | lr=$lr" -ForegroundColor Cyan
                    python cnn_train_param.py --target $target --img_dir $img_dir `
                        --arch $arch --lr $lr --epochs 50 `
                        --split_id $split --run_tag $split --no_smote
                    if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }
        }
    }
}

# ── 3. Train: with SMOTE ──────────────────────────────────────────────────────
Write-Host "`n=== TRAIN (with SMOTE) ===" -ForegroundColor Yellow
$i = 0
foreach ($split in $splits) {
    foreach ($target in $targets) {
        foreach ($img_dir in $img_dirs) {
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    Write-Host "[$i/$total] $split | $target | $img_dir | $arch | lr=$lr (smote)" -ForegroundColor Cyan
                    python cnn_train_param.py --target $target --img_dir $img_dir `
                        --arch $arch --lr $lr --epochs 50 `
                        --split_id $split --run_tag "${split}_smote"
                    if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }
        }
    }
}

# ── 4. Eval: no SMOTE ─────────────────────────────────────────────────────────
Write-Host "`n=== EVAL (no SMOTE) ===" -ForegroundColor Yellow
$i = 0
foreach ($split in $splits) {
    foreach ($target in $targets) {
        foreach ($img_dir in $img_dirs) {
            $scalo_tag = $img_dir -replace "scalograms_", ""
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    $lr_fmt     = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                    $model_path = "models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}_${split}_best.pt"
                    Write-Host "[$i/$total] eval $split | $target | $img_dir | $arch | lr=$lr" -ForegroundColor Cyan
                    python eval_detailed_param.py --target $target --img_dir $img_dir `
                        --arch $arch --lr $lr --split_id $split --run_tag $split `
                        --model $model_path
                    if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }
        }
    }
}

# ── 5. Eval: with SMOTE ───────────────────────────────────────────────────────
Write-Host "`n=== EVAL (with SMOTE) ===" -ForegroundColor Yellow
$i = 0
foreach ($split in $splits) {
    foreach ($target in $targets) {
        foreach ($img_dir in $img_dirs) {
            $scalo_tag = $img_dir -replace "scalograms_", ""
            foreach ($arch in $archs) {
                foreach ($lr in $lrs) {
                    $i++
                    $run_tag    = "${split}_smote"
                    $lr_fmt     = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                    $model_path = "models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}_${run_tag}_best.pt"
                    Write-Host "[$i/$total] eval $split | $target | $img_dir | $arch | lr=$lr (smote)" -ForegroundColor Cyan
                    python eval_detailed_param.py --target $target --img_dir $img_dir `
                        --arch $arch --lr $lr --split_id $split --run_tag $run_tag `
                        --model $model_path
                    if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                }
            }
        }
    }
}

Write-Host "`nAll done. Results in exp_results_32x12_9win_exp11/, exp_results_32x12_9win_exp12/, etc." -ForegroundColor Green
