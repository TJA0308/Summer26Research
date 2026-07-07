### resnet50_lr0.001_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z125 | smooth | smooth | smooth | rough | smooth | ✓ |
| s25f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | rough | smooth | smooth | smooth | ✓ |
| s25f3y5z25 | smooth | smooth | rough | smooth | smooth | ✓ |
| s35f5y25z125 | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z25 | rough | rough | rough | rough | rough | ✓ |
| s35f5y5z125 | smooth | rough | rough | rough | rough | ✗ |
| s35f5y5z25 | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **75.0%** (18/24)
Run MV accuracy: **87.5%** (7/8)