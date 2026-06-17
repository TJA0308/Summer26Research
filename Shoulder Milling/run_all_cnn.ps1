param(
    [string]$RunTag = ""
)
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
                python cnn_train_param.py --target $target --img_dir $img_dir --arch $arch --lr $lr --epochs 50 --run_tag $RunTag
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
    # Merge files into the existing models\<name>\ dir (created by a prior run)
    # instead of moving the whole directory, which errors if the destination
    # already exists.
    $dest = "models\$($_.Name)"
    New-Item -ItemType Directory -Force -Path $dest | Out-Null
    Get-ChildItem -Path $_.FullName -File | Move-Item -Destination $dest -Force
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  Merged $($_.Name) -> $dest"
}
Write-Host "Done." -ForegroundColor Green
