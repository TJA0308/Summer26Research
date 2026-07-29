### efficientnet_b0_lr0.001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_residual_feed  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 5mm | 3mm | 7mm | 5mm | ~ |
| run17 | 6mm | 3mm | 5mm | 7mm | 3mm | 5mm | N |
| run28 | 4mm | 3mm | 3mm | 5mm | 3mm | 3mm | N |
| run35 | 7mm | 7mm | 5mm | 5mm | 5mm | 5mm | N |
| run40 | 3mm | 7mm | 5mm | 5mm | 5mm | 7mm | N |
| run6 | 8mm | 4mm | 3mm | 3mm | 3mm | 3mm | N |

Window accuracy: **11.1%** (2/18)
Run hard-vote accuracy: **0.0%** (0/6)
Run soft-vote accuracy: **16.7%** (1/6)