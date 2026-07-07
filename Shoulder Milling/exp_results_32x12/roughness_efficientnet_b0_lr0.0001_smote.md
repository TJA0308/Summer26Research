### efficientnet_b0_lr0.0001_smote_best  |  target=roughness  |  scalogram=scalograms_32x12  |  arch=efficientnet_b0

| Run | True | a | b | c | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y5z25 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z25 | rough | smooth | rough | rough | rough | ✓ |
| s25f3y25z25 | rough | rough | smooth | smooth | smooth | ✗ |
| s35f5y25z25 | rough | smooth | smooth | smooth | smooth | ✗ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | smooth | rough | smooth | smooth | ✗ |

Window accuracy: **66.7%** (16/24)
Run MV accuracy: **62.5%** (5/8)