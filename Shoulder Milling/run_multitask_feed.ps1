# Multi-task feed experiment: fixed config (efficientnet_b0, lr=1e-4 -- feed's
# historically most stable arch/lr per experiments_writeup.md), swept over
# scalogram variant x split x seed, NOT over arch/lr. The point is to report
# a mean+/-std over seeds and splits for ONE pre-committed config, rather than
# best-of-sweep-picking -- see cnn_train_multitask.py's module docstring for
# why (the cascade's reported "project-best" 87.5% didn't survive a rerun
# after a conditioning bugfix; this experiment is designed so a false win
# can't hide in sweep noise the same way).
#
# 2 scalogram dirs x 3 splits x 3 seeds = 18 runs. Uses the 3-window feedopt
# scalograms (not 9win -- experiments_writeup.md §6 showed 9win increases
# variance without a real accuracy gain once cascade conditioning is
# accounted for correctly).
#
# Run from the Shoulder Milling directory:
#   .\run_multitask_feed.ps1
# Then:
#   python summarize_multitask.py

$ErrorActionPreference = "Continue"
$img_dirs = @("scalograms_32x3_feedopt", "scalograms_32x12_feedopt")
$splits   = @("", "exp11", "exp12")
$seeds    = @(42, 43, 44)
$arch     = "efficientnet_b0"
$lr       = "1e-4"

$total = $img_dirs.Count * $splits.Count * $seeds.Count
$i = 0
foreach ($img_dir in $img_dirs) {
    foreach ($split in $splits) {
        foreach ($seed in $seeds) {
            $i++
            $split_label = if ($split) { $split } else { "base" }
            Write-Host "[$i/$total] $img_dir | split=$split_label | seed=$seed" -ForegroundColor Cyan
            if ($split) {
                python cnn_train_multitask.py --img_dir $img_dir --arch $arch --lr $lr `
                    --seed $seed --split_id $split
            } else {
                python cnn_train_multitask.py --img_dir $img_dir --arch $arch --lr $lr `
                    --seed $seed
            }
            if ($LASTEXITCODE -ne 0) { Write-Host "  ERROR (exit $LASTEXITCODE)" -ForegroundColor Red }
        }
    }
}

Write-Host "`nAll done. Results in models_multitask_feed_32x3_feedopt/ and models_multitask_feed_32x12_feedopt/." -ForegroundColor Green
Write-Host "Run 'python summarize_multitask.py' to aggregate mean+/-std across seeds." -ForegroundColor Green
