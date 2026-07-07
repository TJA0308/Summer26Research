### efficientnet_b0_lr0.0001_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z125 | smooth | smooth | smooth | rough | smooth | ✓ |
| s25f3y25z25 | rough | smooth | smooth | rough | smooth | ✗ |
| s25f3y5z125 | smooth | rough | smooth | smooth | smooth | ✓ |
| s25f3y5z25 | smooth | smooth | rough | rough | rough | ✗ |
| s35f5y25z125 | rough | rough | smooth | rough | rough | ✓ |
| s35f5y25z25 | rough | rough | rough | smooth | rough | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | rough | smooth | ✓ |
| s35f5y5z25 | rough | rough | rough | smooth | rough | ✓ |

Window accuracy: **58.3%** (14/24)
Run MV accuracy: **75.0%** (6/8)