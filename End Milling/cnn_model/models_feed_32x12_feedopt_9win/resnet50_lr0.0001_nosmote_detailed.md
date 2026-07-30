### resnet50_lr0.0001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run1 | 5mm | 3mm | 6mm | 8mm | 8mm | 8mm | 8mm | 8mm | 8mm | 3mm | 8mm | 8mm | N |
| run17 | 6mm | 3mm | 8mm | 4mm | 8mm | 5mm | 8mm | 8mm | 8mm | 3mm | 8mm | 8mm | N |
| run28 | 4mm | 8mm | 8mm | 4mm | 8mm | 8mm | 3mm | 3mm | 8mm | 8mm | 8mm | 8mm | N |
| run35 | 7mm | 4mm | 8mm | 8mm | 5mm | 8mm | 8mm | 8mm | 3mm | 4mm | 8mm | 8mm | N |
| run40 | 3mm | 3mm | 8mm | 4mm | 8mm | 8mm | 3mm | 3mm | 3mm | 4mm | 3mm | 8mm | Y |
| run6 | 8mm | 3mm | 8mm | 4mm | 8mm | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |

Window accuracy: **13.0%** (7/54)
Run hard-vote accuracy: **16.7%** (1/6)
Run soft-vote accuracy: **0.0%** (0/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 7 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.000** | **0.000** | **0.000** | |