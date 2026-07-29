### resnet50_lr0.001_nosmote  |  target=feed  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 7mm | 6mm | 7mm | 7mm | 6mm | ~ |
| run28 | 4mm | 6mm | 4mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 6mm | 6mm | 4mm | 6mm | 6mm | N |
| run40 | 3mm | 7mm | 7mm | 7mm | 7mm | 7mm | N |
| run6 | 8mm | 6mm | 6mm | 4mm | 6mm | 4mm | N |

Window accuracy: **11.1%** (2/18)
Run hard-vote accuracy: **0.0%** (0/6)
Run soft-vote accuracy: **16.7%** (1/6)