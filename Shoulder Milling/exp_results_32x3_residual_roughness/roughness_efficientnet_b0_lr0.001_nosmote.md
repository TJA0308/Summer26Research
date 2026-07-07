### efficientnet_b0_lr0.001_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y5z25 | smooth | rough | smooth | rough | rough | ✗ |
| s35f5y25z125 | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z25 | rough | rough | rough | rough | rough | ✓ |
| s35f5y5z125 | smooth | smooth | rough | rough | rough | ✗ |
| s35f5y5z25 | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **83.3%** (20/24)
Run MV accuracy: **75.0%** (6/8)