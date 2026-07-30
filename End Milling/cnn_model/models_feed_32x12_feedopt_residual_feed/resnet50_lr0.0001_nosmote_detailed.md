### resnet50_lr0.0001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_residual_feed  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run17 | 6mm | 6mm | 4mm | 4mm | 4mm | 4mm | N |
| run28 | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | Y |
| run35 | 7mm | 6mm | 4mm | 4mm | 4mm | 4mm | N |
| run40 | 3mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 6mm | 4mm | 8mm | 6mm | 6mm | N |

Window accuracy: **27.8%** (5/18)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **16.7%** (1/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.200 | 1.000 | 0.333 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 7 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.033** | **0.167** | **0.056** | |