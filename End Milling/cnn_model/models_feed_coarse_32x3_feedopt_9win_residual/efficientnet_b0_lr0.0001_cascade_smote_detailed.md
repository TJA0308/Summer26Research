### efficientnet_b0_lr0.0001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Med | Med | Med | Med | Low | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Low | Low | Med | Low | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Low | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run37 | Low | Med | Med | Low | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Low | Med | Med | Low | Med | Low | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Low | Med | Med | Low | Hi | Med | Med | Med | Med | Y |

Window accuracy: **33.3%** (36/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.333 | 1.000 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.111** | **0.333** | **0.167** | |