### resnet50_lr0.0001_smote  |  target=feed  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 4mm | 4mm | 5mm | 4mm | 4mm | N |
| run17 | 6mm | 5mm | 4mm | 5mm | 5mm | 5mm | N |
| run28 | 4mm | 5mm | 4mm | 8mm | 5mm | 5mm | N |
| run35 | 7mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |
| run40 | 3mm | 5mm | 4mm | 5mm | 5mm | 5mm | N |
| run6 | 8mm | 5mm | 5mm | 5mm | 5mm | 5mm | N |

Window accuracy: **11.1%** (2/18)
Run hard-vote accuracy: **0.0%** (0/6)
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