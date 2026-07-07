### resnet50_lr0.0001_nosmote_best  |  target=doc  |  scalogram=scalograms_32x12_residual_doc  |  arch=resnet50

| Run | True | w1 | w2 | w3 | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y25z125 | Y25Z125 | Y25Z125 | Y25Z250 | Y25Z125 | Y25Z125 | ✓ |
| s25f3y25z25 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | ✓ |
| s25f3y5z125 | Y50Z125 | Y25Z250 | Y25Z125 | Y25Z250 | Y25Z250 | ✗ |
| s25f3y5z25 | Y50Z250 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | ✗ |
| s35f5y25z125 | Y25Z125 | Y25Z125 | Y25Z125 | Y25Z125 | Y25Z125 | ✓ |
| s35f5y25z25 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | ✓ |
| s35f5y5z125 | Y50Z125 | Y25Z125 | Y25Z250 | Y25Z125 | Y25Z125 | ✗ |
| s35f5y5z25 | Y50Z250 | Y25Z250 | Y25Z250 | Y25Z250 | Y25Z250 | ✗ |

Window accuracy: **45.8%** (11/24)
Run MV accuracy: **50.0%** (4/8)