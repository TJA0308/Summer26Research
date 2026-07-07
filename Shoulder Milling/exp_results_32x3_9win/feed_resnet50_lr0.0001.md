### resnet50_lr0.0001_best  |  target=feed  |  scalogram=scalograms_32x3_9win  |  arch=resnet50

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | f3 | f7 | f7 | f7 | f3 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s25f5y5z25 | f5 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s25f7y5z25 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✓ |
| s25f7y25z25 | f7 | f7 | f3 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✓ |
| s35f3y5z125 | f3 | f7 | f3 | f3 | f7 | f3 | f3 | f7 | f3 | f3 | f3 | ✓ |
| s35f3y25z125 | f3 | f7 | f3 | f3 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | ✗ |
| s35f5y25z125 | f5 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s35f7y25z125 | f7 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | ✓ |

Window accuracy: **47.2%** (34/72)
Run MV accuracy: **50.0%** (4/8)