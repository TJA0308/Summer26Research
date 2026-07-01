# Cascade conditioning for feed on feedopt_9win scalogram dirs.
# Mirrors the original run_feed_conditioned.ps1 but for 9win and WITHOUT the
# consolidation step that was destroying .pt checkpoint files.
#
# Pipeline (run_tag = "fc" for "feed conditioned"):
#   Stage 1 -- train speed  (no parents)        -> top-level models_speed_*/
#   Stage 2 -- predict speed -> speed_pred_*_fc.csv in img_dir
#   Stage 3 -- train doc conditioned on speed   -> top-level models_doc_*/
#   Stage 4 -- predict doc -> doc_pred_*_fc.csv in img_dir
#   Stage 5 -- train feed conditioned on speed+doc -> top-level models_feed_*/
#   Stage 6 -- eval feed
#
# Run from the Shoulder Milling directory:
#   .\run_feedopt_9win_cascade.ps1

$ErrorActionPreference = "Continue"
$archs   = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs     = @("1e-3", "1e-4")
$dirs    = @("scalograms_32x12_feedopt_9win", "scalograms_32x3_feedopt_9win")
$run_tag = "fc"
$n_combo = $dirs.Count * $archs.Count * $lrs.Count   # 16

# ── Stage 1: speed ─────────────────────────────────────────────────────────────
Write-Host "`n=== Stage 1: speed ===" -ForegroundColor Yellow
$i = 0
foreach ($dir in $dirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$n_combo] speed | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python cnn_train_param.py --target speed --img_dir $dir `
                --arch $arch --lr $lr --epochs 50 --run_tag $run_tag --no_smote
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

# ── Generate speed conditioning CSVs ───────────────────────────────────────────
Write-Host "`n=== Generating speed predictions ===" -ForegroundColor Yellow
foreach ($dir in $dirs) {
    Write-Host "  $dir" -ForegroundColor Cyan
    python predict_conditioning.py --target speed --img_dir $dir --run_tag $run_tag
    if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR generating speed predictions" -ForegroundColor Red }
}

# ── Stage 2: doc (auto-conditions on speed since speed_pred_*_fc.csv now exists) ─
Write-Host "`n=== Stage 2: doc (conditioned on speed) ===" -ForegroundColor Yellow
$i = 0
foreach ($dir in $dirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$n_combo] doc | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python cnn_train_param.py --target doc --img_dir $dir `
                --arch $arch --lr $lr --epochs 50 --run_tag $run_tag --no_smote
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

# ── Generate doc conditioning CSVs ─────────────────────────────────────────────
Write-Host "`n=== Generating doc predictions ===" -ForegroundColor Yellow
foreach ($dir in $dirs) {
    Write-Host "  $dir" -ForegroundColor Cyan
    python predict_conditioning.py --target doc --img_dir $dir --run_tag $run_tag
    if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR generating doc predictions" -ForegroundColor Red }
}

# ── Stage 3: feed (auto-conditions on speed+doc since both CSVs now exist) ─────
Write-Host "`n=== Stage 3: feed (conditioned on speed+doc) ===" -ForegroundColor Yellow
$i = 0
foreach ($dir in $dirs) {
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            Write-Host "[$i/$n_combo] feed | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python cnn_train_param.py --target feed --img_dir $dir `
                --arch $arch --lr $lr --epochs 50 --run_tag $run_tag --no_smote
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

# ── Eval: feed conditioned ─────────────────────────────────────────────────────
Write-Host "`n=== EVAL: feed (conditioned) on feedopt_9win ===" -ForegroundColor Yellow
$i = 0
foreach ($dir in $dirs) {
    $scalo_tag  = $dir -replace "scalograms_", ""
    foreach ($arch in $archs) {
        foreach ($lr in $lrs) {
            $i++
            $lr_fmt     = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
            $model_path = "models_feed_${scalo_tag}\${arch}_lr${lr_fmt}_${run_tag}_best.pt"
            Write-Host "[$i/$n_combo] eval feed | $dir | $arch | lr=$lr" -ForegroundColor Cyan
            python eval_detailed_param.py --target feed --img_dir $dir `
                --arch $arch --lr $lr --run_tag $run_tag --model $model_path
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

Write-Host "`nAll done. Results in exp_results_32x12_feedopt_9win/ and exp_results_32x3_feedopt_9win/ (suffix _fc)." -ForegroundColor Green
