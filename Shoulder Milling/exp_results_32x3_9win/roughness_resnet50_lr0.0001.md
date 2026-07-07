### resnet50_lr0.0001_best  |  target=roughness  |  scalogram=scalograms_32x3_9win  |  arch=resnet50

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z25 | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✗ |
| s25f3y25z25 | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | rough | ✓ |
| s35f5y25z25 | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | ✗ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | ✗ |

Window accuracy: **66.7%** (48/72)
Run MV accuracy: **62.5%** (5/8)