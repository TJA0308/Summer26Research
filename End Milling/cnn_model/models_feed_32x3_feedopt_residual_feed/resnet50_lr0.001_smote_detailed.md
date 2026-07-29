### resnet50_lr0.001_smote  |  target=feed  |  scalogram=32x3_feedopt_residual_feed  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 6mm | 7mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 6mm | 5mm | 7mm | 6mm | 5mm | Y |
| run28 | 4mm | 3mm | 5mm | 3mm | 3mm | 3mm | N |
| run35 | 7mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run40 | 3mm | 5mm | 7mm | 5mm | 5mm | 5mm | N |
| run6 | 8mm | 5mm | 6mm | 6mm | 6mm | 6mm | N |

Window accuracy: **5.6%** (1/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **0.0%** (0/6)