### resnet50_lr0.0001_best  |  target=roughness  |  scalogram=scalograms_32x12_9win  |  arch=resnet50

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | smooth | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✗ |
| s35f5y5z25 | rough | rough | rough | rough | rough | rough | rough | smooth | rough | rough | rough | ✓ |
| s25f3y25z25 | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z25 | rough | smooth | rough | rough | smooth | rough | rough | rough | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | rough | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | smooth | rough | rough | smooth | rough | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **79.2%** (57/72)
Run MV accuracy: **87.5%** (7/8)