### convnext_tiny_lr0.001_exp11_smote_best  |  target=roughness  |  scalogram=scalograms_32x3_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y25z25 | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | rough | ✓ |
| s25f5y25z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f5y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | rough | ✓ |
| s35f3y25z25 | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| s35f5y25z125 | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| s35f5y5z125 | smooth | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | ✗ |
| s35f7y5z25 | smooth | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✗ |

Window accuracy: **70.8%** (51/72)
Run MV accuracy: **75.0%** (6/8)