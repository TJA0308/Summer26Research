### efficientnet_b0_lr0.001_best  |  target=speed  |  scalogram=scalograms_32x3_9win  |  arch=efficientnet_b0

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 3500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | ✓ |
| s35f3y5z25 | 3500rpm | 3500rpm | 2500rpm | 3500rpm | 3500rpm | 3500rpm | 3500rpm | 3500rpm | 3500rpm | 3500rpm | 3500rpm | ✓ |
| s25f5y25z25 | 2500rpm | 3500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | ✓ |
| s35f5y25z25 | 3500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 3500rpm | 2500rpm | ✗ |
| s25f7y5z125 | 2500rpm | 3500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 3500rpm | 2500rpm | 2500rpm | 3500rpm | 2500rpm | ✓ |
| s35f7y5z125 | 3500rpm | 3500rpm | 2500rpm | 2500rpm | 3500rpm | 2500rpm | 2500rpm | 3500rpm | 2500rpm | 2500rpm | 2500rpm | ✗ |
| s25f3y25z125 | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | ✓ |
| s35f3y25z125 | 3500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 2500rpm | 3500rpm | 2500rpm | 2500rpm | 2500rpm | ✗ |

Window accuracy: **61.1%** (44/72)
Run MV accuracy: **62.5%** (5/8)