### efficientnet_b0_lr0.0001_exp12_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z25 | rough | rough | rough | smooth | rough | ✓ |
| s25f5y5z125 | smooth | smooth | smooth | rough | smooth | ✓ |
| s25f7y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | smooth | rough | rough | rough | ✓ |
| s35f3y25z25 | rough | rough | rough | smooth | rough | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | rough | smooth | ✓ |
| s35f7y25z125 | rough | smooth | smooth | smooth | smooth | ✗ |
| s35f7y5z25 | smooth | smooth | smooth | smooth | smooth | ✓ |

Window accuracy: **66.7%** (16/24)
Run MV accuracy: **87.5%** (7/8)