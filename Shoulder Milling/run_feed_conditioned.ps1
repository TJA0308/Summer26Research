$ErrorActionPreference = "Continue"
$archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs   = @("1e-3", "1e-4")
$dirs  = @("scalograms_32x12_feedopt", "scalograms_32x3_feedopt")

# ── 1. Generate speed/doc conditioning CSVs ──────────────────────────────────
# speed+doc models on these feedopt dirs already exist in models\models_{speed,doc}_*_feedopt\
# (trained by run_finish_sweeps.ps1). This just runs each best one over all 72
# images and writes <target>_pred_<scalo>_smote.csv into the feedopt dir itself.
Write-Host "`n=== Generating conditioning CSVs ===" -ForegroundColor Yellow
foreach ($dir in $dirs) {
    python predict_conditioning.py --target speed --img_dir $dir --run_tag smote
    python predict_conditioning.py --target doc   --img_dir $dir --run_tag smote
}

# ── 2. Retrain feed -- cnn_train_param.py auto-detects the CSVs above and ────
# switches to ConditionedModel (concatenates predicted speed+doc onehots before
# the classifier head). SMOTE is auto-skipped once conditioned (synthetic
# windows have no real upstream conditioning value) -- no flag changes needed.
Write-Host "`n=== TRAIN feed (conditioned on speed+doc) on feedopt dirs ===" -ForegroundColor Yellow
$total = $dirs.Count * $archs.Count * $lrs.Count; $i = 0
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

# ── 3. Consolidate into models\ ───────────────────────────────────────────────
# NOTE: this overwrites the previous (unconditioned) feed-feedopt checkpoints
# at models\models_feed_*_feedopt\*_smote_best.pt with the new conditioned ones.
Write-Host "`nConsolidating into models/ ..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "models" | Out-Null
Get-ChildItem -Directory -Filter "models_*" | ForEach-Object {
    $dest = "models\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $dest -Force
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  Merged $($_.Name) -> $dest"
}

# ── 4. Detailed eval (per-run predictions + majority vote .md reports) ───────
Write-Host "`n=== EVAL: feed (conditioned) on feedopt scalograms ===" -ForegroundColor Yellow
$i = 0
foreach ($dir in $dirs) {
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
