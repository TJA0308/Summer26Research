### resnet50_lr0.001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_residual_feed  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 4mm | 5mm | 6mm | 4mm | 6mm | ~ |
| run28 | 4mm | 3mm | 6mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 4mm | 6mm | 6mm | 6mm | 6mm | N |
| run40 | 3mm | 8mm | 4mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |

Window accuracy: **5.6%** (1/18)
Run hard-vote accuracy: **0.0%** (0/6)
Run soft-vote accuracy: **16.7%** (1/6)