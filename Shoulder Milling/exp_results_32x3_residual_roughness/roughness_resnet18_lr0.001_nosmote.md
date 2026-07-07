### resnet18_lr0.001_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x3_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y5z25 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | smooth | smooth | smooth | smooth | ✗ |
| s35f5y25z25 | rough | rough | rough | smooth | rough | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z25 | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **83.3%** (20/24)
Run MV accuracy: **87.5%** (7/8)