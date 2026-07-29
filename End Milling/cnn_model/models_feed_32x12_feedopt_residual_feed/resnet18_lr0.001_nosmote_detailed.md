### resnet18_lr0.001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_residual_feed  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 6mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 5mm | 7mm | 6mm | 5mm | 5mm | N |
| run28 | 4mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 4mm | 7mm | 7mm | 7mm | 7mm | Y |
| run40 | 3mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 6mm | 6mm | 7mm | 6mm | 7mm | N |

Window accuracy: **16.7%** (3/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)