### resnet50_lr0.001_nosmote  |  target=feed  |  scalogram=32x3_feedopt_residual_feed  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 7mm | 6mm | 7mm | 7mm | N |
| run17 | 6mm | 7mm | 8mm | 8mm | 8mm | 8mm | N |
| run28 | 4mm | 3mm | 3mm | 3mm | 3mm | 3mm | N |
| run35 | 7mm | 6mm | 7mm | 7mm | 7mm | 7mm | Y |
| run40 | 3mm | 7mm | 7mm | 8mm | 7mm | 8mm | N |
| run6 | 8mm | 4mm | 7mm | 6mm | 4mm | 6mm | N |

Window accuracy: **11.1%** (2/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 7 mm/rev | 0.500 | 1.000 | 0.667 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.083** | **0.167** | **0.111** | |