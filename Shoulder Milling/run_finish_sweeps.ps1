$ErrorActionPreference = "Continue"
$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

# ── 1. Train speed+doc on feedopt dirs (needed for conditioning CSVs) ─────────
Write-Host "`n=== TRAIN speed+doc on feedopt dirs ===" -ForegroundColor Yellow
$i = 0; $total = 2 * 2 * $archs.Count * $lrs.Count
foreach ($target in @("speed", "doc")) {
    foreach ($dir in @("scalograms_32x12_feedopt", "scalograms_32x3_feedopt")) {
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "[$i/$total] $target | $dir | $arch | lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target $target --img_dir $dir --arch $arch --lr $lr --run_tag smote --epochs 50
                if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }
    }
}

# ── 2. Retrain the one roughness model that failed (file lock) ────────────────
Write-Host "`nRetraining roughness | scalograms_32x3 | convnext_tiny | lr=1e-4 ..." -ForegroundColor Yellow
python cnn_train_param.py --target roughness --img_dir scalograms_32x3 --arch convnext_tiny --lr 1e-4 --no_smote --epochs 50
if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }

# ── 3. Consolidate all root-level models_* into models/ ──────────────────────
Write-Host "`nConsolidating into models/ ..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "models" | Out-Null
Get-ChildItem -Directory -Filter "models_*" | ForEach-Object {
    $dest = "models\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $dest -Force
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  Merged $($_.Name) -> $dest"
}

# ── 4. Generate conditioning CSVs for feedopt dirs ────────────────────────────
Write-Host "`n=== Generating conditioning CSVs ===" -ForegroundColor Yellow
foreach ($dir in @("scalograms_32x12_feedopt", "scalograms_32x3_feedopt")) {
    python predict_conditioning.py --target speed --img_dir $dir --run_tag smote
    python predict_conditioning.py --target doc   --img_dir $dir --run_tag smote
}

# ── 5. eval_all_param_sweep.py (roughness + speed/feed/doc on standard dirs) ──
Write-Host "`n=== EVAL: eval_all_param_sweep.py ===" -ForegroundColor Yellow
python eval_all_param_sweep.py
if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR in eval_all_param_sweep.py" -ForegroundColor Red }

# ── 6. Eval feed+speed+doc on feedopt scalograms ─────────────────────────────
Write-Host "`n=== EVAL: all targets on feedopt scalograms ===" -ForegroundColor Yellow
$i = 0; $total = 3 * 2 * $archs.Count * $lrs.Count
foreach ($target in @("speed", "doc", "feed")) {
    foreach ($dir in @("scalograms_32x12_feedopt", "scalograms_32x3_feedopt")) {
        $scalo_tag = $dir -replace "scalograms_", ""
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                $lr_fmt = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                $tag    = if ($target -eq "feed") { "_smote" } else { "_smote" }
                $model_path = "models\models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}${tag}_best.pt"
                Write-Host "[$i/$total] $target | $dir | $arch | lr=$lr" -ForegroundColor Cyan
                python eval_detailed_param.py --target $target --img_dir $dir --arch $arch --lr $lr --run_tag smote --model $model_path
                if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }
    }
}

Write-Host "`nAll done." -ForegroundColor Green
