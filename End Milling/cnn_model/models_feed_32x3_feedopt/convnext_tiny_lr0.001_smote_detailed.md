### convnext_tiny_lr0.001_smote  |  target=feed  |  scalogram=32x3_feedopt  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | Y |
| run17 | 6mm | 5mm | 8mm | 8mm | 8mm | 8mm | N |
| run28 | 4mm | 6mm | 3mm | 4mm | 6mm | 3mm | N |
| run35 | 7mm | 7mm | 8mm | 8mm | 8mm | 8mm | N |
| run40 | 3mm | 5mm | 8mm | 7mm | 5mm | 8mm | N |
| run6 | 8mm | 8mm | 8mm | 8mm | 8mm | 8mm | Y |

Window accuracy: **44.4%** (8/18)
Run hard-vote accuracy: **33.3%** (2/6)
Run soft-vote accuracy: **33.3%** (2/6)