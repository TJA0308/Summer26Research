Set-Location "D:\Users\svk6639\Documents\GitHub\Summer26Research\End Milling"

foreach ($target in @("speed", "doc", "roughness", "feed_coarse")) {
    foreach ($bb_short in @("rn18", "rn50", "enb0", "cnxt")) {
        $bb = switch ($bb_short) {
            "rn18" { "resnet18" }
            "rn50" { "resnet50" }
            "enb0" { "efficientnet_b0" }
            "cnxt" { "convnext_tiny" }
        }
        foreach ($lr in @("lr1e3", "lr1e4")) {
            $model = "..\models\std_${target}_${bb_short}_${lr}.pt"
            $out   = "results_a\std_${target}_${bb_short}_${lr}.md"
            Write-Host "[eval-A] $model"
            python cnn_model/eval_detailed.py `
                --model   $model `
                --target  $target `
                --backbone $bb `
                --pipeline a `
                --save_md $out
        }
    }
}
Write-Host "[eval-A] DONE"
