### resnet50_lr0.0001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_residual_feed  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run17 | 6mm | 6mm | 4mm | 4mm | 4mm | 4mm | N |
| run28 | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | Y |
| run35 | 7mm | 6mm | 4mm | 4mm | 4mm | 4mm | N |
| run40 | 3mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 6mm | 4mm | 8mm | 6mm | 6mm | N |

Window accuracy: **27.8%** (5/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)