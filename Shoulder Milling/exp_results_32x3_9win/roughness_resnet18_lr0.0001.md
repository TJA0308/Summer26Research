### resnet18_lr0.0001_best  |  target=roughness  |  scalogram=scalograms_32x3_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| 1a | smooth | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | ✓ |
| 2b | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| 3a | rough | smooth | rough | rough | smooth | rough | rough | smooth | rough | rough | rough | ✓ |
| 4b | rough | rough | smooth | rough | rough | rough | rough | rough | rough | rough | rough | ✓ |
| 5a | smooth | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | ✓ |
| 6b | smooth | rough | rough | rough | rough | rough | rough | rough | smooth | rough | rough | ✗ |
| 7a | smooth | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | ✓ |
| 8b | rough | smooth | smooth | smooth | smooth | smooth | rough | rough | smooth | rough | smooth | ✗ |

Window accuracy: **62.5%** (45/72)
Run MV accuracy: **75.0%** (6/8)