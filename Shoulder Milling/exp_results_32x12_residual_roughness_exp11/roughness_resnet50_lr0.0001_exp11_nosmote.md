### resnet50_lr0.0001_exp11_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s25f5y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | smooth | smooth | rough | smooth | ✗ |
| s35f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z125 | rough | rough | rough | rough | rough | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f7y5z25 | smooth | rough | smooth | rough | rough | ✗ |

Window accuracy: **83.3%** (20/24)
Run MV accuracy: **75.0%** (6/8)