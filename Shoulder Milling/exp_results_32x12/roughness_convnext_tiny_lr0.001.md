### convnext_tiny_lr0.001_best  |  target=roughness  |  scalogram=scalograms_32x12  |  arch=convnext_tiny

| Run | True | a | b | c | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y5z25 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z25 | rough | rough | rough | rough | rough | ✓ |
| s25f3y25z25 | rough | smooth | smooth | smooth | smooth | ✗ |
| s35f5y25z25 | rough | rough | rough | rough | rough | ✓ |
| s25f3y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f3y25z125 | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f5y25z125 | rough | smooth | smooth | smooth | smooth | ✗ |

Window accuracy: **75.0%** (18/24)
Run MV accuracy: **75.0%** (6/8)