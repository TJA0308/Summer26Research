### resnet50_lr0.0001_smote  |  target=feed  |  scalogram=32x12_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 6mm | 5mm | 7mm | 7mm | N |
| run17 | 6mm | 4mm | 6mm | 5mm | 4mm | 4mm | N |
| run28 | 4mm | 4mm | 4mm | 5mm | 4mm | 5mm | Y |
| run35 | 7mm | 4mm | 6mm | 5mm | 4mm | 4mm | N |
| run40 | 3mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run6 | 8mm | 4mm | 4mm | 5mm | 4mm | 4mm | N |

Window accuracy: **22.2%** (4/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **0.0%** (0/6)