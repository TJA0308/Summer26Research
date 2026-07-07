### efficientnet_b0_lr0.0001_exp12_best  |  target=roughness  |  scalogram=scalograms_32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z25 | rough | smooth | smooth | smooth | smooth | ✗ |
| s25f5y5z125 | smooth | smooth | smooth | rough | smooth | ✓ |
| s25f7y25z125 | smooth | rough | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | rough | rough | smooth | rough | ✓ |
| s35f3y25z25 | rough | smooth | smooth | smooth | smooth | ✗ |
| s35f5y5z125 | smooth | smooth | smooth | rough | smooth | ✓ |
| s35f7y25z125 | rough | rough | rough | rough | rough | ✓ |
| s35f7y5z25 | smooth | smooth | smooth | rough | smooth | ✓ |

Window accuracy: **54.2%** (13/24)
Run MV accuracy: **75.0%** (6/8)