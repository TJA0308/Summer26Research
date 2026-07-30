### resnet18_lr0.0001_smote  |  target=feed  |  scalogram=32x12_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run1 | 5mm | 4mm | 6mm | 5mm | 4mm | 4mm | N |
| run17 | 6mm | 7mm | 5mm | 7mm | 7mm | 7mm | N |
| run28 | 4mm | 7mm | 7mm | 5mm | 7mm | 7mm | N |
| run35 | 7mm | 4mm | 7mm | 5mm | 4mm | 7mm | ~ |
| run40 | 3mm | 4mm | 5mm | 5mm | 5mm | 4mm | N |
| run6 | 8mm | 7mm | 7mm | 7mm | 7mm | 7mm | N |

Window accuracy: **11.1%** (2/18)
Run hard-vote accuracy: **0.0%** (0/6)
Run soft-vote accuracy: **16.7%** (1/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 7 mm/rev | 0.250 | 1.000 | 0.400 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.042** | **0.167** | **0.067** | |