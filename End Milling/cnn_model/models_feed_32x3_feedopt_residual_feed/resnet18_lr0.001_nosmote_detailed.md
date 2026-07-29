### resnet18_lr0.001_nosmote  |  target=feed  |  scalogram=32x3_feedopt_residual_feed  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 6mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 5mm | 6mm | 6mm | 6mm | 5mm | Y |
| run28 | 4mm | 3mm | 6mm | 5mm | 3mm | 3mm | N |
| run35 | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | Y |
| run40 | 3mm | 4mm | 4mm | 5mm | 4mm | 4mm | N |
| run6 | 8mm | 4mm | 7mm | 8mm | 4mm | 7mm | N |

Window accuracy: **33.3%** (6/18)
Run hard-vote accuracy: **33.3%** (2/6)
Run soft-vote accuracy: **16.7%** (1/6)