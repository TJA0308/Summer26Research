### efficientnet_b0_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Med | Hi | Hi | Hi | Med | Hi | Hi | Hi | N |
| run17 | Med | Hi | Med | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Low | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Hi | Med | Med | Hi | Med | Med | Hi | Med | Med | Hi | Y |

Window accuracy: **39.8%** (43/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.333 | 1.000 | 0.500 | 4 |
| **macro avg** | **0.111** | **0.333** | **0.167** | |