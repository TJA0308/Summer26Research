### convnext_tiny_lr0.001_best  |  target=roughness  |  scalogram=scalograms_32x3  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| 1a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 2b | rough | rough | rough | rough | rough | ✓ |
| 3a | rough | smooth | rough | rough | rough | ✓ |
| 4b | rough | rough | rough | rough | rough | ✓ |
| 5a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 6b | smooth | smooth | smooth | smooth | smooth | ✓ |
| 7a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 8b | rough | smooth | smooth | smooth | smooth | ✗ |

Window accuracy: **83.3%** (20/24)
Run MV accuracy: **87.5%** (7/8)