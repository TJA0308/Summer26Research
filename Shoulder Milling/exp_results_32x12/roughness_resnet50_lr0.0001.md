### resnet50_lr0.0001_best  |  target=roughness  |  scalogram=scalograms_32x12  |  arch=resnet50

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| 1a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 2b | rough | rough | smooth | smooth | smooth | ✗ |
| 3a | rough | smooth | smooth | smooth | smooth | ✗ |
| 4b | rough | rough | rough | rough | rough | ✓ |
| 5a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 6b | smooth | rough | smooth | smooth | smooth | ✓ |
| 7a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 8b | rough | smooth | smooth | smooth | smooth | ✗ |

Window accuracy: **62.5%** (15/24)
Run MV accuracy: **62.5%** (5/8)