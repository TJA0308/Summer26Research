### efficientnet_b0_lr0.0001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_residual_feed  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 3mm | 6mm | 8mm | 3mm | 3mm | N |
| run17 | 6mm | 6mm | 6mm | 7mm | 6mm | 6mm | Y |
| run28 | 4mm | 4mm | 6mm | 5mm | 4mm | 4mm | Y |
| run35 | 7mm | 5mm | 6mm | 7mm | 5mm | 5mm | N |
| run40 | 3mm | 5mm | 6mm | 5mm | 5mm | 5mm | N |
| run6 | 8mm | 5mm | 5mm | 7mm | 5mm | 5mm | N |

Window accuracy: **22.2%** (4/18)
Run hard-vote accuracy: **33.3%** (2/6)
Run soft-vote accuracy: **33.3%** (2/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 1.000 | 1.000 | 1.000 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 1.000 | 1.000 | 1.000 | 1 |
| 7 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.333** | **0.333** | **0.333** | |