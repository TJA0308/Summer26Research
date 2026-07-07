### resnet50_lr0.0001_exp12_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x3_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z25 | rough | rough | smooth | smooth | smooth | ✗ |
| s25f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | smooth | smooth | smooth | smooth | ✗ |
| s35f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f7y25z125 | rough | smooth | smooth | rough | smooth | ✗ |
| s35f7y5z25 | smooth | smooth | smooth | smooth | smooth | ✓ |

Window accuracy: **70.8%** (17/24)
Run MV accuracy: **62.5%** (5/8)