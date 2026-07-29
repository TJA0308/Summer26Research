### convnext_tiny_lr0.0001_nosmote  |  target=feed  |  scalogram=32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run1 | 5mm | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | 4mm | 6mm | 6mm | N |
| run17 | 6mm | 8mm | 5mm | 5mm | 8mm | 5mm | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | N |
| run28 | 4mm | 6mm | 5mm | 3mm | 3mm | 5mm | 7mm | 7mm | 5mm | 7mm | 5mm | 7mm | N |
| run35 | 7mm | 7mm | 8mm | 5mm | 5mm | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | Y |
| run40 | 3mm | 5mm | 5mm | 5mm | 8mm | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 7mm | 5mm | 4mm | 4mm | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | N |

Window accuracy: **11.1%** (6/54)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)