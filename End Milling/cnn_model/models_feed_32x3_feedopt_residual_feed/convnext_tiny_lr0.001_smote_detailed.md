### convnext_tiny_lr0.001_smote  |  target=feed  |  scalogram=32x3_feedopt_residual_feed  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 6mm | 5mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | Y |
| run28 | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | Y |
| run35 | 7mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run40 | 3mm | 5mm | 4mm | 6mm | 5mm | 5mm | N |
| run6 | 8mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |

Window accuracy: **38.9%** (7/18)
Run hard-vote accuracy: **33.3%** (2/6)
Run soft-vote accuracy: **33.3%** (2/6)