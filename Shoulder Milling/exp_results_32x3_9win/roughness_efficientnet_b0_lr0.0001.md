### efficientnet_b0_lr0.0001_best  |  target=roughness  |  scalogram=scalograms_32x3_9win  |  arch=efficientnet_b0

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | smooth | rough | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z25 | rough | rough | smooth | rough | rough | smooth | smooth | rough | smooth | smooth | smooth | ✗ |
| s25f3y25z25 | rough | smooth | rough | rough | rough | rough | rough | smooth | rough | smooth | rough | ✓ |
| s35f5y25z25 | rough | rough | rough | rough | smooth | rough | rough | smooth | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | smooth | smooth | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z125 | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | smooth | ✓ |
| s25f3y25z125 | smooth | smooth | smooth | rough | smooth | rough | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | rough | smooth | smooth | smooth | smooth | rough | rough | smooth | rough | smooth | ✗ |

Window accuracy: **68.1%** (49/72)
Run MV accuracy: **75.0%** (6/8)