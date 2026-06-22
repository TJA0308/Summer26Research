### convnext_tiny_lr0.0001_best  |  target=roughness  |  scalogram=scalograms_32x12_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| 1a | smooth | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✗ |
| 2b | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| 3a | rough | rough | rough | rough | smooth | rough | rough | rough | rough | rough | rough | ✓ |
| 4b | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| 5a | smooth | smooth | smooth | smooth | smooth | smooth | smooth | rough | smooth | smooth | smooth | ✓ |
| 6b | smooth | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | rough | ✗ |
| 7a | smooth | smooth | smooth | smooth | rough | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| 8b | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **75.0%** (54/72)
Run MV accuracy: **75.0%** (6/8)