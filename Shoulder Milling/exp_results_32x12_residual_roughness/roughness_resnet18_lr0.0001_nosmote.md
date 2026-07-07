### resnet18_lr0.0001_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x12_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z25 | rough | smooth | rough | smooth | smooth | ✗ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y5z25 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z25 | rough | rough | rough | rough | rough | ✓ |
| s35f5y5z125 | smooth | rough | rough | rough | rough | ✗ |
| s35f5y5z25 | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **79.2%** (19/24)
Run MV accuracy: **75.0%** (6/8)