### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_perdoc  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Hi | Hi | N |
| run17 | Med | Hi | Med | Med | Med | Hi | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Hi | Hi | Med | Hi | Hi | N |
| run3 | Hi | Hi | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Med | Hi | Med | Y |
| run37 | Low | Hi | Med | Med | Med | Med | N |
| run45 | Med | Hi | Hi | Med | Hi | Med | ~ |
| run5 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Med | Hi | Hi | N |
| run9 | Med | Hi | Hi | Med | Hi | Med | ~ |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.429 | 0.750 | 0.545 | 4 |
| 7-8 mm/rev (high) | 0.200 | 0.250 | 0.222 | 4 |
| **macro avg** | **0.210** | **0.333** | **0.256** | |