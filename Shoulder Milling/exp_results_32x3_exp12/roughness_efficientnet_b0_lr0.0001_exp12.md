### efficientnet_b0_lr0.0001_exp12_best  |  target=roughness  |  scalogram=scalograms_32x3  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z25 | rough | smooth | rough | rough | rough | ✓ |
| s25f5y5z125 | smooth | smooth | rough | smooth | smooth | ✓ |
| s25f7y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | rough | rough | rough | rough | ✓ |
| s35f3y25z25 | rough | smooth | smooth | rough | smooth | ✗ |
| s35f5y5z125 | smooth | rough | rough | rough | rough | ✗ |
| s35f7y25z125 | rough | smooth | rough | rough | rough | ✓ |
| s35f7y5z25 | smooth | rough | smooth | rough | rough | ✗ |

Window accuracy: **58.3%** (14/24)
Run MV accuracy: **62.5%** (5/8)