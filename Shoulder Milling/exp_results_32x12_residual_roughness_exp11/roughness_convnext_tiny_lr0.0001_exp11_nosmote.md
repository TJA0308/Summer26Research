### convnext_tiny_lr0.0001_exp11_nosmote_best  |  target=roughness  |  scalogram=scalograms_32x12_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s25f5y25z125 | smooth | rough | rough | rough | rough | ✗ |
| s25f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | rough | rough | smooth | rough | ✓ |
| s35f3y25z25 | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z125 | rough | rough | rough | rough | rough | ✓ |
| s35f5y5z125 | smooth | rough | rough | rough | rough | ✗ |
| s35f7y5z25 | smooth | smooth | rough | rough | rough | ✗ |

Window accuracy: **62.5%** (15/24)
Run MV accuracy: **62.5%** (5/8)