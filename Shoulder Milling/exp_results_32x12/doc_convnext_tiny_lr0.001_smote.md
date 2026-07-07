### convnext_tiny_lr0.001_smote_best  |  target=doc  |  scalogram=scalograms_32x12  |  arch=convnext_tiny

| Run | True | a | b | c | MV | ✓/✗ |
|-----|------|----|----|----|-----|-----|
| s25f3y5z25 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | ✓ |
| s35f5y5z25 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | ✓ |
| s25f3y25z25 | Y25Z250 | Y50Z250 | Y50Z250 | Y25Z250 | Y50Z250 | ✗ |
| s35f5y25z25 | Y25Z250 | Y50Z250 | Y50Z250 | Y50Z250 | Y50Z250 | ✗ |
| s25f3y5z125 | Y50Z125 | Y50Z125 | Y50Z125 | Y50Z125 | Y50Z125 | ✓ |
| s35f5y5z125 | Y50Z125 | Y50Z125 | Y50Z125 | Y50Z125 | Y50Z125 | ✓ |
| s25f3y25z125 | Y25Z125 | Y50Z125 | Y50Z125 | Y50Z125 | Y50Z125 | ✗ |
| s35f5y25z125 | Y25Z125 | Y50Z125 | Y50Z125 | Y50Z125 | Y50Z125 | ✗ |

Window accuracy: **54.2%** (13/24)
Run MV accuracy: **50.0%** (4/8)