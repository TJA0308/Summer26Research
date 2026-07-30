### resnet18_lr0.001_nosmote  |  target=feed  |  scalogram=32x12_feedopt_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run1 | 5mm | 7mm | 6mm | 6mm | 6mm | 6mm | 6mm | 6mm | 4mm | 6mm | 6mm | 6mm | N |
| run17 | 6mm | 7mm | 7mm | 6mm | 6mm | 7mm | 6mm | 6mm | 6mm | 7mm | 6mm | 6mm | Y |
| run28 | 4mm | 6mm | 6mm | 6mm | 4mm | 6mm | 6mm | 7mm | 7mm | 6mm | 6mm | 6mm | N |
| run35 | 7mm | 7mm | 7mm | 6mm | 6mm | 6mm | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | Y |
| run40 | 3mm | 5mm | 4mm | 4mm | 8mm | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | 4mm | N |
| run6 | 8mm | 6mm | 6mm | 8mm | 8mm | 6mm | 7mm | 7mm | 7mm | 7mm | 7mm | 7mm | N |

Window accuracy: **25.9%** (14/54)
Run hard-vote accuracy: **33.3%** (2/6)
Run soft-vote accuracy: **33.3%** (2/6)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 4 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 5 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| 6 mm/rev | 0.333 | 1.000 | 0.500 | 1 |
| 7 mm/rev | 0.500 | 1.000 | 0.667 | 1 |
| 8 mm/rev | 0.000 | 0.000 | 0.000 | 1 |
| **macro avg** | **0.139** | **0.333** | **0.194** | |