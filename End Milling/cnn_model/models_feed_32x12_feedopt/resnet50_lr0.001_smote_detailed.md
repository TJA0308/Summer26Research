### resnet50_lr0.001_smote  |  target=feed  |  scalogram=32x12_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 6mm | 8mm | 8mm | 8mm | 6mm | ~ |
| run28 | 4mm | 3mm | 6mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 4mm | 8mm | 7mm | 4mm | 7mm | ~ |
| run40 | 3mm | 6mm | 4mm | 5mm | 6mm | 4mm | N |
| run6 | 8mm | 6mm | 6mm | 6mm | 6mm | 6mm | N |

Window accuracy: **11.1%** (2/18)
Run hard-vote accuracy: **0.0%** (0/6)
Run soft-vote accuracy: **33.3%** (2/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 0.250 | 1.000 | 0.400 | 1 |
| 7 mm/rev | 1.000 | 1.000 | 1.000 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.208** | **0.333** | **0.233** | |