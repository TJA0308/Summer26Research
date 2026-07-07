### efficientnet_b0_lr0.0001_exp11_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z25 | rough | smooth | smooth | rough | smooth | ✗ |
| s25f5y25z125 | smooth | rough | smooth | smooth | smooth | ✓ |
| s25f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | smooth | smooth | smooth | smooth | ✗ |
| s35f3y25z25 | rough | rough | smooth | smooth | smooth | ✗ |
| s35f5y25z125 | rough | smooth | rough | smooth | smooth | ✗ |
| s35f5y5z125 | smooth | rough | rough | smooth | rough | ✗ |
| s35f7y5z25 | smooth | smooth | smooth | smooth | smooth | ✓ |

Window accuracy: **50.0%** (12/24)
Run MV accuracy: **37.5%** (3/8)