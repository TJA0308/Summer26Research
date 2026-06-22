$ErrorActionPreference = "Continue"
$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")

# ── 1. Train speed/doc/feed/roughness on the standard 9win dirs ─────────────
# Direct apples-to-apples comparison against the existing 3-window results
# in exp_results_32x12/ and exp_results_32x3/ (see eval_param_sweep_summary.csv).
$stdDirs = @("scalograms_32x12_9win", "scalograms_32x3_9win")
Write-Host "`n=== TRAIN speed/doc/feed/roughness on standard 9win dirs ===" -ForegroundColor Yellow
$total = 4 * $stdDirs.Count * $archs.Count * $lrs.Count; $i = 0
foreach ($target in @("speed", "doc", "feed", "roughness")) {
    foreach ($dir in $stdDirs) {
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "[$i/$total] $target | $dir | $arch | lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target $target --img_dir $dir --arch $arch --lr $lr --no_smote --epochs 50
                if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }
    }
}

# ── 2. Train speed+doc on the feedopt 9win dirs (needed for feed conditioning) ─
$feedoptDirs = @("scalograms_32x12_feedopt_9win", "scalograms_32x3_feedopt_9win")
Write-Host "`n=== TRAIN speed+doc on feedopt 9win dirs ===" -ForegroundColor Yellow
$total = 2 * $feedoptDirs.Count * $archs.Count * $lrs.Count; $i = 0
foreach ($target in @("speed", "doc")) {
    foreach ($dir in $feedoptDirs) {
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "[$i/$total] $target | $dir | $arch | lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target $target --img_dir $dir --arch $arch --lr $lr --no_smote --epochs 50
                if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
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

# ── 4. Generate conditioning CSVs for feedopt 9win dirs ──────────────────────
Write-Host "`n=== Generating conditioning CSVs ===" -ForegroundColor Yellow
foreach ($dir in $feedoptDirs) {
    python predict_conditioning.py --target speed --img_dir $dir
    python predict_conditioning.py --target doc   --img_dir $dir
}

# ── 5. Train feed conditioned on speed+doc, on feedopt 9win dirs ─────────────
# cnn_train_param.py auto-detects the CSVs above and switches to ConditionedModel.
Write-Host "`n=== TRAIN feed (conditioned on speed+doc) on feedopt 9win dirs ===" -ForegroundColor Yellow
$total = $feedoptDirs.Count * $archs.Count * $lrs.Count; $i = 0
foreach ($dir in $feedoptDirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$total] feed | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python cnn_train_param.py --target feed --img_dir $dir --arch $arch --lr $lr --epochs 50
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

# ── 6. Re-consolidate (feed-conditioned checkpoints just trained above) ──────
Write-Host "`nConsolidating into models/ ..." -ForegroundColor Green
Get-ChildItem -Directory -Filter "models_*" | ForEach-Object {
    $dest = "models\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $dest -Force
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  Merged $($_.Name) -> $dest"
}

# ── 7. Detailed eval (per-run predictions + majority vote .md reports) ───────
Write-Host "`n=== EVAL: speed/doc/feed/roughness on standard 9win dirs ===" -ForegroundColor Yellow
$total = 4 * $stdDirs.Count * $archs.Count * $lrs.Count; $i = 0
foreach ($target in @("speed", "doc", "feed", "roughness")) {
    foreach ($dir in $stdDirs) {
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "[$i/$total] eval $target | $dir | $arch | lr=$lr" -ForegroundColor Cyan
                python eval_detailed_param.py --target $target --img_dir $dir --arch $arch --lr $lr
                if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
            }
        }
    }
}

Write-Host "`n=== EVAL: feed (conditioned) on feedopt 9win dirs ===" -ForegroundColor Yellow
$total = $feedoptDirs.Count * $archs.Count * $lrs.Count; $i = 0
foreach ($dir in $feedoptDirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$total] eval feed | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python eval_detailed_param.py --target feed --img_dir $dir --arch $arch --lr $lr
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

Write-Host "`nAll done." -ForegroundColor Green
