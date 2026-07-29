### convnext_tiny_lr0.0001_nosmote  |  target=feed  |  scalogram=32x3_feedopt_residual_feed  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 6mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | Y |
| run28 | 4mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 4mm | 3mm | 7mm | 4mm | 3mm | N |
| run40 | 3mm | 4mm | 7mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 6mm | 7mm | 7mm | 7mm | 6mm | N |

Window accuracy: **22.2%** (4/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)