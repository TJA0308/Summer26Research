### efficientnet_b0_lr0.0001_nosmote_best  |  target=feed  |  scalogram=scalograms_32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y5z25 | f3 | f3 | f7 | f3 | f3 | ✓ |
| s25f5y5z25 | f5 | f5 | f3 | f7 | f5 | ✓ |
| s25f7y25z25 | f7 | f7 | f7 | f7 | f7 | ✓ |
| s25f7y5z25 | f7 | f3 | f3 | f7 | f3 | ✗ |
| s35f3y25z125 | f3 | f3 | f7 | f3 | f3 | ✓ |
| s35f3y5z125 | f3 | f3 | f7 | f7 | f7 | ✗ |
| s35f5y25z125 | f5 | f3 | f3 | f3 | f3 | ✗ |
| s35f7y25z125 | f7 | f3 | f3 | f7 | f3 | ✗ |

Window accuracy: **45.8%** (11/24)
Run MV accuracy: **50.0%** (4/8)