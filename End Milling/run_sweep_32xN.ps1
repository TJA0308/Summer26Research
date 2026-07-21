# Full training sweep for the 32x3 / 32x12 precomputed-feature pipelines --
# all 4 targets x 4 backbones x 2 LRs x with/without SMOTE, across both
# feature layouts (32x3, 32x12) and both window variants (3win baseline,
# 9win), i.e. this IS the "all four backbones and with/without SMOTE"
# sweep. Follows this repo's existing foreach-loop sweep convention (see
# run_eval_nosmote_a.ps1) rather than one flat line per combo, since the
# grid here (2 layouts x 2 win variants x 4 targets x 4 archs x 2 LRs x 2
# SMOTE = 256 runs) is much larger than the single-pipeline sweeps that
# convention was originally written for.
#
# Each target trains on its OWN scale-selection-tuned directory --
# roughness on the base dir, feed_coarse on _feedopt, speed on _speedopt,
# doc on _docopt. compare_scale_selection.py found reusing roughness's
# selection for speed/doc left real signal on the table (only 86.7%/93.2%
# as efficient as a dedicated selection), which is why _speedopt/_docopt
# exist at all -- see build_32x3_features.py's docstring.
#
# NOT included here (separate, smaller scripts / manual steps -- see
# README_32x3.md): residual-corrected img_dirs, and the feed_coarse cascade
# (--conditioned / --cascade_predicted), which only apply to one target and
# need speed/doc trained first.
#
# Usage:
#   powershell -File run_sweep_32xN.ps1
#   (edit the $Layouts / $WinVariants / $Archs / $LRs arrays below to
#    narrow the sweep, e.g. comment out 32x12 or _9win to halve the runs)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$Archs = @("resnet18", "resnet50", "efficientnet_b0", "convnext_tiny")
$LRs   = @("1e-3", "1e-4")
$Targets = @("speed", "doc", "feed_coarse", "roughness")

$Layouts = @(
    @{ Name = "32x3";  Base = "scalograms_32x3";  Feedopt = "scalograms_32x3_feedopt";
       Speedopt = "scalograms_32x3_speedopt"; Docopt = "scalograms_32x3_docopt" },
    @{ Name = "32x12"; Base = "scalograms_32x12"; Feedopt = "scalograms_32x12_feedopt";
       Speedopt = "scalograms_32x12_speedopt"; Docopt = "scalograms_32x12_docopt" }
)
$WinVariants = @("", "_9win")

$total = $Layouts.Count * $WinVariants.Count * $Targets.Count * $Archs.Count * $LRs.Count * 2
$done  = 0

foreach ($layout in $Layouts) {
    foreach ($winSuffix in $WinVariants) {
        $dirFor = @{
            "roughness"   = "$($layout.Base)$winSuffix"
            "feed_coarse" = "$($layout.Feedopt)$winSuffix"
            "speed"       = "$($layout.Speedopt)$winSuffix"
            "doc"         = "$($layout.Docopt)$winSuffix"
        }

        foreach ($target in $Targets) {
            $imgDir = $dirFor[$target]

            foreach ($arch in $Archs) {
                foreach ($lr in $LRs) {
                    foreach ($smoteMode in @("smote", "nosmote")) {
                        $done++
                        Write-Host "[$done/$total] $imgDir target=$target arch=$arch lr=$lr $smoteMode"
                        $cmdArgs = @("--target", $target, "--img_dir", $imgDir, "--arch", $arch,
                                     "--lr", $lr, "--run_tag", $smoteMode)
                        if ($smoteMode -eq "nosmote") { $cmdArgs += "--no_smote" }
                        python cnn_model/cnn_train_32x3.py @cmdArgs
                    }
                }
            }
        }
    }
}
Write-Host "Sweep complete: $done runs."
