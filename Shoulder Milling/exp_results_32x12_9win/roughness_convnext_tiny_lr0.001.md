### convnext_tiny_lr0.001_best  |  target=roughness  |  scalogram=scalograms_32x12_9win  |  arch=convnext_tiny

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z25 | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✗ |
| s25f3y25z25 | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✗ |
| s35f5y25z25 | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✗ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✗ |

Window accuracy: **50.0%** (36/72)
Run MV accuracy: **50.0%** (4/8)