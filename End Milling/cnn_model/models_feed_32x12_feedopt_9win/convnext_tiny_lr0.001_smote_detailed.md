### convnext_tiny_lr0.001_smote  |  target=feed  |  scalogram=32x12_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run1 | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | Y |
| run17 | 6mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run28 | 4mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run35 | 7mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run40 | 3mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run6 | 8mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |

Window accuracy: **16.7%** (9/54)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 5 mm/rev | 0.167 | 1.000 | 0.286 | 1 |
| 6 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 7 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.028** | **0.167** | **0.048** | |