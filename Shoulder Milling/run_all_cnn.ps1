$ErrorActionPreference = "Continue"
$targets = @("speed", "feed", "doc")
$img_dirs = @("scalograms_32x12", "scalograms_32x3")
$archs   = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs     = @("1e-3", "1e-4")

$total = $targets.Count * $img_dirs.Count * $archs.Count * $lrs.Count
$i = 0

foreach ($target in $targets) {
    foreach ($img_dir in $img_dirs) {
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "[$i/$total] target=$target img_dir=$img_dir arch=$arch lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target $target --img_dir $img_dir --arch $arch --lr $lr --epochs 50
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "  ERROR on above command (exit $LASTEXITCODE)" -ForegroundColor Red
                }
            }
        }
    }
}

Write-Host "`nAll runs complete. Consolidating into models/ ..." -ForegroundColor Green
New-Item -ItemType Directory -Force -Path "models" | Out-Null
Get-ChildItem -Directory -Filter "models_*" | ForEach-Object {
    Move-Item $_.FullName "models\" -Force
    Write-Host "  Moved $($_.Name)"
}
Write-Host "Done." -ForegroundColor Green
