### resnet18_lr0.0001_exp12_best  |  target=feed  |  scalogram=scalograms_32x12_feedopt_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y25z25 | f3 | f7 | f3 | f3 | f3 | f3 | f3 | f7 | f3 | f3 | f3 | ✓ |
| s25f5y5z125 | f5 | f3 | f7 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | f7 | ✗ |
| s25f7y25z125 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | f7 | ✓ |
| s25f7y5z25 | f7 | f7 | f5 | f7 | f7 | f5 | f7 | f7 | f5 | f7 | f7 | ✓ |
| s35f3y25z25 | f3 | f7 | f7 | f7 | f3 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s35f5y5z125 | f5 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s35f7y25z125 | f7 | f7 | f7 | f7 | f3 | f7 | f7 | f7 | f7 | f7 | f7 | ✓ |
| s35f7y5z25 | f7 | f3 | f7 | f7 | f7 | f7 | f7 | f3 | f7 | f7 | f7 | ✓ |

Window accuracy: **48.6%** (35/72)
Run MV accuracy: **62.5%** (5/8)