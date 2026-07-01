### efficientnet_b0_lr0.0001_exp12_smote_best  |  target=roughness  |  scalogram=scalograms_32x3_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y25z25 | rough | rough | rough | smooth | rough | smooth | rough | rough | smooth | rough | rough | ✓ |
| s25f5y5z125 | smooth | rough | smooth | smooth | rough | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y25z125 | smooth | rough | smooth | smooth | rough | smooth | rough | rough | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | rough | rough | rough | rough | smooth | rough | smooth | smooth | rough | rough | ✓ |
| s35f3y25z25 | rough | smooth | smooth | smooth | smooth | smooth | smooth | rough | smooth | smooth | smooth | ✗ |
| s35f5y5z125 | smooth | rough | smooth | smooth | rough | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f7y25z125 | rough | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | smooth | ✗ |
| s35f7y5z25 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | rough | smooth | rough | smooth | ✓ |

Window accuracy: **58.3%** (42/72)
Run MV accuracy: **75.0%** (6/8)