### convnext_tiny_lr0.001_best  |  target=feed  |  scalogram=scalograms_32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | a_1 | a_2 | a_3 | b_1 | b_2 | b_3 | c_1 | c_2 | c_3 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y5z25 | f3 | f3 | f3 | f5 | f3 | f3 | f5 | f3 | f3 | f5 | f3 | ✓ |
| s25f5y5z25 | f5 | f3 | f5 | f5 | f3 | f5 | f5 | f3 | f5 | f5 | f5 | ✓ |
| s25f7y5z25 | f7 | f3 | f5 | f5 | f3 | f5 | f5 | f3 | f5 | f5 | f5 | ✗ |
| s25f7y25z25 | f7 | f5 | f3 | f5 | f3 | f5 | f5 | f3 | f5 | f5 | f5 | ✗ |
| s35f3y5z125 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | ✓ |
| s35f3y25z125 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | f3 | ✓ |
| s35f5y25z125 | f5 | f3 | f3 | f7 | f3 | f3 | f7 | f3 | f3 | f7 | f3 | ✗ |
| s35f7y25z125 | f7 | f7 | f3 | f7 | f7 | f7 | f7 | f7 | f3 | f7 | f7 | ✓ |

Window accuracy: **51.4%** (37/72)
Run MV accuracy: **62.5%** (5/8)