# Full residual CNN sweep for speed, doc, roughness targets.
# 2 dirs x 3 targets x 3 splits x 2 SMOTE x 4 archs x 2 LRs = 288 training runs + evals.
#
# Run from the Shoulder Milling directory:
#   .\run_residual_sweep_all_targets.ps1

$ErrorActionPreference = "Continue"

$target_dirs = @{
    "speed"     = @("scalograms_32x3_residual_speed",     "scalograms_32x12_residual_speed")
    "doc"       = @("scalograms_32x3_residual_doc",       "scalograms_32x12_residual_doc")
    "roughness" = @("scalograms_32x3_residual_roughness", "scalograms_32x12_residual_roughness")
}
$archs  = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs    = @("1e-3", "1e-4")
$splits = @("", "exp11", "exp12")   # "" = base split

$total = $target_dirs.Count * 2 * $splits.Count * 2 * $archs.Count * $lrs.Count
$i = 0

foreach ($target in $target_dirs.Keys) {
    foreach ($img_dir in $target_dirs[$target]) {
        $scalo_tag = $img_dir -replace "scalograms_", ""
        foreach ($split in $splits) {
            $split_label = if ($split) { $split } else { "base" }
            foreach ($smote_mode in @($false, $true)) {
                $smote_label = if ($smote_mode) { "smote" } else { "nosmote" }
                $run_tag = if ($split -and !$smote_mode) { "${split}_nosmote" } `
                           elseif ($split)               { $split } `
                           elseif (!$smote_mode)         { "nosmote" } `
                           else                          { "" }

                foreach ($arch in $archs) {
                    foreach ($lr in $lrs) {
                        $i++
                        Write-Host "[$i/$total] $target | $img_dir | $split_label | $smote_label | $arch | lr=$lr" -ForegroundColor Cyan
                        $train_args = @("cnn_train_param.py",
                            "--target", $target, "--img_dir", $img_dir,
                            "--arch", $arch, "--lr", $lr, "--epochs", "50")
                        if ($split)       { $train_args += @("--split_id", $split) }
                        if ($run_tag)     { $train_args += @("--run_tag", $run_tag) }
                        if (!$smote_mode) { $train_args += "--no_smote" }
                        python @train_args
                        if ($LASTEXITCODE -ne 0) { Write-Host "  TRAIN ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
                    }
                }

                # Eval this batch
                foreach ($arch in $archs) {
                    foreach ($lr in $lrs) {
                        $lr_fmt     = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                        $tag_suffix = if ($run_tag) { "_${run_tag}" } else { "" }
                        $model_path = "models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}${tag_suffix}_best.pt"
                        $eval_args  = @("eval_detailed_param.py",
                            "--target", $target, "--img_dir", $img_dir,
                            "--arch", $arch, "--lr", $lr, "--model", $model_path)
                        if ($split)   { $eval_args += @("--split_id", $split) }
                        if ($run_tag) { $eval_args += @("--run_tag", $run_tag) }
                        python @eval_args
                        if ($LASTEXITCODE -ne 0) { Write-Host "  EVAL ERROR" -ForegroundColor Red }
                    }
                }
            }
        }
    }
}

Write-Host "`nAll done." -ForegroundColor Green
