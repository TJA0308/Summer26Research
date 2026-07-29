### convnext_tiny_lr0.001_smote  |  target=feed  |  scalogram=32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run1 | 5mm | 4mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 4mm | 5mm | 5mm | Y |
| run17 | 6mm | 4mm | 4mm | 8mm | 8mm | 8mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run28 | 4mm | 8mm | 3mm | 3mm | 3mm | 3mm | 6mm | 3mm | 3mm | 3mm | 3mm | 3mm | N |
| run35 | 7mm | 8mm | 4mm | 6mm | 8mm | 8mm | 8mm | 8mm | 8mm | 6mm | 8mm | 8mm | N |
| run40 | 3mm | 4mm | 4mm | 4mm | 5mm | 8mm | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 8mm | 7mm | 8mm | 8mm | 8mm | 8mm | 8mm | 6mm | 6mm | 8mm | 8mm | Y |

Window accuracy: **24.1%** (13/54)
Run hard-vote accuracy: **33.3%** (2/6)
Run soft-vote accuracy: **33.3%** (2/6)