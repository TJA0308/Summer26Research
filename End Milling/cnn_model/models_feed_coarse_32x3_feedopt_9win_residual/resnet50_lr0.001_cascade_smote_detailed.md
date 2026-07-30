### resnet50_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Low | Med | Med | Hi | Hi | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Med | Med | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Low | Low | Low | Low | Med | Low | Med | Low | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Med | Low | Low | Low | Med | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **57.4%** (62/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.600 | 0.750 | 0.667 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.667 | 1.000 | 0.800 | 4 |
| **macro avg** | **0.422** | **0.583** | **0.489** | |