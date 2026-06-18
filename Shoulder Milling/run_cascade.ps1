param(
    [string]$RunTag = "cascade"
)
$ErrorActionPreference = "Continue"
$archs    = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$lrs      = @("1e-3", "1e-4")
$img_dirs = @("scalograms_32x12", "scalograms_32x3")

function Train-Combos($target) {
    $i = 0
    foreach ($img_dir in $img_dirs) {
        foreach ($arch in $archs) {
            foreach ($lr in $lrs) {
                $i++
                Write-Host "[$target $i/16] img_dir=$img_dir arch=$arch lr=$lr" -ForegroundColor Cyan
                python cnn_train_param.py --target $target --img_dir $img_dir --arch $arch --lr $lr --epochs 50 --run_tag $RunTag
                if ($LASTEXITCODE -ne 0) {
                    Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red
                }
            }
        }
    }
}

Write-Host "=== Stage 1: speed ===" -ForegroundColor Green
Train-Combos "speed"

Write-Host "`n=== Selecting best speed model per pipeline, generating predictions ===" -ForegroundColor Green
foreach ($img_dir in $img_dirs) {
    python predict_conditioning.py --target speed --img_dir $img_dir --run_tag $RunTag
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR generating speed predictions for $img_dir (exit $LASTEXITCODE)" -ForegroundColor Red
    }
}

Write-Host "`n=== Stage 2: doc (conditioned on predicted speed) ===" -ForegroundColor Green
Train-Combos "doc"

Write-Host "`n=== Selecting best doc model per pipeline, generating predictions ===" -ForegroundColor Green
foreach ($img_dir in $img_dirs) {
    python predict_conditioning.py --target doc --img_dir $img_dir --run_tag $RunTag
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR generating doc predictions for $img_dir (exit $LASTEXITCODE)" -ForegroundColor Red
    }
}

Write-Host "`n=== Stage 3: feed (conditioned on predicted speed + doc) ===" -ForegroundColor Green
Train-Combos "feed"

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
