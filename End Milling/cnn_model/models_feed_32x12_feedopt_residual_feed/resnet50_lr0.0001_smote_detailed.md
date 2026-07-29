### resnet50_lr0.0001_smote  |  target=feed  |  scalogram=32x12_feedopt_residual_feed  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 6mm | 4mm | 7mm | 6mm | N |
| run17 | 6mm | 6mm | 7mm | 6mm | 6mm | 6mm | Y |
| run28 | 4mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run40 | 3mm | 6mm | 6mm | 4mm | 6mm | 6mm | N |
| run6 | 8mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |

Window accuracy: **11.1%** (2/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)