$ErrorActionPreference = "Continue"
$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

# ── 1. Feed sweep on feed-optimized scalograms ───────────────────────────────
$dirs = @("scalograms_32x12_feedopt", "scalograms_32x3_feedopt")
$total = $dirs.Count * $archs.Count * $lrs.Count; $i = 0
Write-Host "`n=== FEED SWEEP (feedopt) ===" -ForegroundColor Yellow
foreach ($dir in $dirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$total] feed | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python cnn_train_param.py --target feed --img_dir $dir --arch $arch --lr $lr --run_tag smote --epochs 50
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

# ── 2. Roughness sweep ───────────────────────────────────────────────────────
$dirs = @("scalograms_32x12", "scalograms_32x3")
$total = $dirs.Count * $archs.Count * $lrs.Count; $i = 0
Write-Host "`n=== ROUGHNESS SWEEP ===" -ForegroundColor Yellow
foreach ($dir in $dirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$total] roughness | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python cnn_train_param.py --target roughness --img_dir $dir --arch $arch --lr $lr --no_smote --epochs 50
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

# ── 3. Consolidate into models/ ──────────────────────────────────────────────
Write-Host "`nConsolidating into models/ ..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "models" | Out-Null
Get-ChildItem -Directory -Filter "models_*" | ForEach-Object {
    $dest = "models\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $dest -Force
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  Merged $($_.Name) -> $dest"
}

# ── 4. Eval: roughness (and any other targets) via eval_all_param_sweep.py ───
Write-Host "`n=== EVAL: eval_all_param_sweep.py ===" -ForegroundColor Yellow
python eval_all_param_sweep.py
if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR in eval_all_param_sweep.py" -ForegroundColor Red }

# ── 5. Eval: feed on feedopt scalograms ──────────────────────────────────────
Write-Host "`n=== EVAL: feed on feedopt scalograms ===" -ForegroundColor Yellow
$total = 2 * $archs.Count * $lrs.Count; $i = 0
foreach ($dir in @("scalograms_32x12_feedopt", "scalograms_32x3_feedopt")) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$total] eval feed | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python eval_detailed_param.py --target feed --img_dir $dir --arch $arch --lr $lr --run_tag smote
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

Write-Host "`nAll done." -ForegroundColor Green
