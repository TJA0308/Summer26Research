### resnet18_lr0.001_best  |  target=feed  |  scalogram=scalograms_32x3_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| 1a | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | ✓ |
| 1b | f5 | f3 | f5 | f5 | f3 | f5 | f5 | f3 | f5 | f5 | f5 | ✓ |
| 1c | f7 | f3 | f5 | f5 | f3 | f5 | f3 | f3 | f3 | f3 | f3 | ✗ |
| 3c | f7 | f5 | f3 | f7 | f3 | f5 | f5 | f3 | f5 | f5 | f5 | ✗ |
| 6a | f3 | f7 | f3 | f7 | f7 | f3 | f7 | f3 | f3 | f7 | f7 | ✗ |
| 8a | f3 | f3 | f3 | f7 | f5 | f3 | f7 | f3 | f3 | f7 | f3 | ✓ |
| 8b | f5 | f5 | f3 | f3 | f5 | f3 | f7 | f5 | f3 | f7 | f3 | ✗ |
| 8c | f7 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | ✓ |

Window accuracy: **47.2%** (34/72)
Run MV accuracy: **50.0%** (4/8)