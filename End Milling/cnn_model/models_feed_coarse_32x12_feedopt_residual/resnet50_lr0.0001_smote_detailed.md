### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Med | Med | Med | Low | Y |
| run21 | Hi | Low | Med | Med | Med | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Low | Low | N |
| run31 | Med | Low | Med | Med | Med | Low | Y |
| run36 | Hi | Low | Low | Med | Low | Low | N |
| run37 | Low | Low | Med | Med | Med | Low | ~ |
| run45 | Med | Low | Low | Low | Low | Low | N |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Med | Med | Med | Low | ~ |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.364 | 1.000 | 0.533 | 4 |
| 5-6 mm/rev (med) | 1.000 | 0.250 | 0.400 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.455** | **0.417** | **0.311** | |