### resnet18_lr0.0001_best  |  target=roughness  |  scalogram=scalograms_32x12  |  arch=resnet18

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| 1a | smooth | rough | rough | rough | rough | ✗ |
| 2b | rough | rough | rough | smooth | rough | ✓ |
| 3a | rough | rough | rough | rough | rough | ✓ |
| 4b | rough | rough | smooth | rough | rough | ✓ |
| 5a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 6b | smooth | smooth | smooth | smooth | smooth | ✓ |
| 7a | smooth | smooth | smooth | smooth | smooth | ✓ |
| 8b | rough | smooth | smooth | smooth | smooth | ✗ |

Window accuracy: **66.7%** (16/24)
Run MV accuracy: **75.0%** (6/8)