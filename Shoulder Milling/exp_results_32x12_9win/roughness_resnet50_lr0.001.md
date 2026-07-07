### resnet50_lr0.001_best  |  target=roughness  |  scalogram=scalograms_32x12_9win  |  arch=resnet50

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | smooth | rough | rough | rough | smooth | rough | rough | rough | rough | rough | rough | ✗ |
| s35f5y5z25 | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| s25f3y25z25 | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z25 | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | rough | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | ✓ |
| s35f5y5z125 | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | smooth | ✓ |
| s25f3y25z125 | smooth | rough | smooth | rough | smooth | smooth | rough | rough | smooth | rough | rough | ✗ |
| s35f5y25z125 | rough | rough | rough | smooth | smooth | rough | smooth | rough | rough | smooth | rough | ✓ |

Window accuracy: **66.7%** (48/72)
Run MV accuracy: **75.0%** (6/8)