### resnet18_lr0.001_best  |  target=roughness  |  scalogram=scalograms_32x3  |  arch=resnet18

| Run | True | a | b | c | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y5z25 | smooth | rough | rough | rough | rough | ✗ |
| s35f5y5z25 | rough | rough | rough | rough | rough | ✓ |
| s25f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z25 | rough | rough | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z125 | smooth | rough | rough | rough | rough | ✗ |
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **75.0%** (18/24)
Run MV accuracy: **75.0%** (6/8)