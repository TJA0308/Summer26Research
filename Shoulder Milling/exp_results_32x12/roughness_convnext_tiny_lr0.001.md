### convnext_tiny_lr0.001_best  |  target=roughness  |  scalogram=scalograms_32x12  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| 1a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 2b | rough | rough | rough | rough | rough | ✓ |
| 3a | rough | smooth | smooth | smooth | smooth | ✗ |
| 4b | rough | rough | rough | rough | rough | ✓ |
| 5a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 6b | smooth | smooth | smooth | smooth | smooth | ✓ |
| 7a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 8b | rough | smooth | smooth | smooth | smooth | ✗ |

Window accuracy: **75.0%** (18/24)
Run MV accuracy: **75.0%** (6/8)