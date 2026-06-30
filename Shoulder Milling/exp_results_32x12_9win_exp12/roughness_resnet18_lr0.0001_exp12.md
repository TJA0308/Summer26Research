### resnet18_lr0.0001_exp12_best  |  target=roughness  |  scalogram=scalograms_32x12_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | MV | ✓/✗ |
|-----|------|----|----|----|----|----|----|----|----|----|-----|-----|
| s25f3y25z25 | rough | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | smooth | ✗ |
| s25f5y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y25z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s25f7y5z25 | rough | rough | smooth | smooth | rough | smooth | smooth | rough | smooth | smooth | smooth | ✗ |
| s35f3y25z25 | rough | smooth | smooth | smooth | smooth | smooth | smooth | rough | smooth | smooth | smooth | ✗ |
| s35f5y5z125 | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |
| s35f7y25z125 | rough | smooth | smooth | smooth | smooth | smooth | smooth | rough | smooth | smooth | smooth | ✗ |
| s35f7y5z25 | smooth | rough | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | smooth | ✓ |

Window accuracy: **59.7%** (43/72)
Run MV accuracy: **50.0%** (4/8)