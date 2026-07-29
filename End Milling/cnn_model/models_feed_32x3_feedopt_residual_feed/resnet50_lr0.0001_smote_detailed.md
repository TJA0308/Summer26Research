### resnet50_lr0.0001_smote  |  target=feed  |  scalogram=32x3_feedopt_residual_feed  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 3mm | 6mm | 5mm | 3mm | 6mm | N |
| run17 | 6mm | 5mm | 6mm | 6mm | 6mm | 6mm | Y |
| run28 | 4mm | 5mm | 5mm | 3mm | 5mm | 3mm | N |
| run35 | 7mm | 4mm | 5mm | 3mm | 4mm | 5mm | N |
| run40 | 3mm | 6mm | 4mm | 6mm | 6mm | 5mm | N |
| run6 | 8mm | 4mm | 3mm | 5mm | 4mm | 4mm | N |

Window accuracy: **16.7%** (3/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)