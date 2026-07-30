### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **46.3%** (50/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.571 | 1.000 | 0.727 | 4 |
| 7-8 mm/rev (high) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.390** | **0.583** | **0.465** | |