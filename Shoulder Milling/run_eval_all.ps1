param(
    [string]$RunTag = ""
)
$ErrorActionPreference = "Continue"
$targets  = @("speed", "feed", "doc")
$img_dirs = @("scalograms_32x12", "scalograms_32x3")
$archs    = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs      = @("1e-3", "1e-4")

$total = $targets.Count * $img_dirs.Count * $archs.Count * $lrs.Count
$i = 0
$tagSuffix = if ($RunTag) { "_$RunTag" } else { "" }

foreach ($target in $targets) {
    foreach ($img_dir in $img_dirs) {
        $scalo_tag = $img_dir -replace "scalograms_", ""
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                $lr_fmt = if ($lr -eq "1e-3") { "0.001" } else { "0.0001" }
                $model_path = "models\models_${target}_${scalo_tag}\${arch}_lr${lr_fmt}${tagSuffix}_best.pt"
                Write-Host "[$i/$total] target=$target img_dir=$img_dir arch=$arch lr=$lr" -ForegroundColor Cyan
                python eval_detailed_param.py --target $target --img_dir $img_dir --arch $arch --lr $lr --model $model_path --run_tag $RunTag
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red
                }
            }
        }
    }
}

Write-Host "`nAll evals complete." -ForegroundColor Green
