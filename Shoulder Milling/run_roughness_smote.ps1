$ErrorActionPreference = "Continue"
$img_dirs = @("scalograms_32x12", "scalograms_32x3")
$archs    = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs      = @("1e-3", "1e-4")

# Roughness was never run with --run_tag smote (smote_generate_param.py predates
# the roughness target, added in c66237f) -- generated via
# `python smote_generate_param.py --target roughness` first. Note: roughness's
# train split is already perfectly balanced (24/24 smooth/rough), so SMOTE
# generated 0 synthetic samples for both scalogram dirs -- this run is expected
# to land close to the existing no-tag roughness results, not exceed them.

# ── 1. Train roughness x both scalogram dirs x 4 archs x 2 lrs, run_tag=smote ─
Write-Host "`n=== TRAIN roughness (smote) ===" -ForegroundColor Yellow
$total = $img_dirs.Count * $archs.Count * $lrs.Count; $i = 0
foreach ($img_dir in $img_dirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$total] roughness | $img_dir | $arch | lr=$lr" -ForegroundColor Cyan
            python cnn_train_param.py --target roughness --img_dir $img_dir --arch $arch --lr $lr --run_tag smote --epochs 50
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

# ── 2. Consolidate into models/ ──────────────────────────────────────────────
Write-Host "`nConsolidating into models/ ..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "models" | Out-Null
Get-ChildItem -Directory -Filter "models_*" | ForEach-Object {
    $dest = "models\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $dest -Force
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  Merged $($_.Name) -> $dest"
}

# ── 3. Detailed eval (per-run predictions + majority vote .md reports) ───────
Write-Host "`n=== EVAL roughness (smote) ===" -ForegroundColor Yellow
$i = 0
foreach ($img_dir in $img_dirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$total] eval roughness | $img_dir | $arch | lr=$lr" -ForegroundColor Cyan
            python eval_detailed_param.py --target roughness --img_dir $img_dir --arch $arch --lr $lr --run_tag smote
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

Write-Host "`nAll done." -ForegroundColor Green
