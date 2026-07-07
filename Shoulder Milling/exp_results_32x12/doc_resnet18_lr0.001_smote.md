### resnet18_lr0.001_smote_best  |  target=doc  |  scalogram=scalograms_32x12  |  arch=resnet18

| Run | True | a | b | c | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y5z25 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | ✓ |
| s35f5y5z25 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | ✓ |
| s25f3y25z25 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | ✓ |
| s35f5y25z25 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | ✓ |
| s25f3y5z125 | Y50Z125 | Y25Z250 | Y25Z125 | Y25Z125 | Y25Z125 | ✗ |
| s35f5y5z125 | Y50Z125 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | ✗ |
| s25f3y25z125 | Y25Z125 | Y25Z125 | Y25Z125 | Y25Z250 | Y25Z125 | ✓ |
| s35f5y25z125 | Y25Z125 | Y25Z125 | Y25Z125 | Y25Z125 | Y25Z125 | ✓ |

Window accuracy: **70.8%** (17/24)
Run MV accuracy: **75.0%** (6/8)