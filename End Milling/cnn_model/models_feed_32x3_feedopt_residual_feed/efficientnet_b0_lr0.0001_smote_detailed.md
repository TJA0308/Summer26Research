### efficientnet_b0_lr0.0001_smote  |  target=feed  |  scalogram=32x3_feedopt_residual_feed  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 5mm | 4mm | 6mm | 5mm | 4mm | Y |
| run17 | 6mm | 6mm | 6mm | 4mm | 6mm | 6mm | Y |
| run28 | 4mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 4mm | 6mm | 4mm | 4mm | 4mm | N |
| run40 | 3mm | 6mm | 4mm | 6mm | 6mm | 6mm | N |
| run6 | 8mm | 5mm | 6mm | 6mm | 6mm | 6mm | N |

Window accuracy: **16.7%** (3/18)
Run hard-vote accuracy: **33.3%** (2/6)
Run soft-vote accuracy: **16.7%** (1/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 0.250 | 1.000 | 0.400 | 1 |
| 7 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.042** | **0.167** | **0.067** | |