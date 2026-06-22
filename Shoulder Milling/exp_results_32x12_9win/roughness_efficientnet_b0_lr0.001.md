### efficientnet_b0_lr0.001_best  |  target=roughness  |  scalogram=scalograms_32x12_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| 1a | smooth | rough | smooth | smooth | rough | smooth | rough | rough | smooth | smooth | smooth | ✓ |
| 2b | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| 3a | rough | rough | smooth | rough | rough | rough | smooth | smooth | smooth | rough | rough | ✓ |
| 4b | rough | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | ✓ |
| 5a | smooth | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | ✗ |
| 6b | smooth | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | ✗ |
| 7a | smooth | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | ✗ |
| 8b | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |

Window accuracy: **59.7%** (43/72)
Run MV accuracy: **62.5%** (5/8)