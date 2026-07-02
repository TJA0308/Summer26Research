### resnet50_lr0.001_exp12_smote_best  |  target=feed  |  scalogram=scalograms_32x12_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y25z25 | f3 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s25f5y5z125 | f5 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s25f7y25z125 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f3 | f7 | f7 | f7 | ✓ |
| s25f7y5z25 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✓ |
| s35f3y25z25 | f3 | f7 | f7 | f7 | f7 | f7 | f7 | f3 | f7 | f7 | f7 | ✗ |
| s35f5y5z125 | f5 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✗ |
| s35f7y25z125 | f7 | f7 | f7 | f3 | f7 | f7 | f3 | f7 | f7 | f3 | f7 | ✓ |
| s35f7y5z25 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | f7 | ✓ |

Window accuracy: **45.8%** (33/72)
Run MV accuracy: **50.0%** (4/8)