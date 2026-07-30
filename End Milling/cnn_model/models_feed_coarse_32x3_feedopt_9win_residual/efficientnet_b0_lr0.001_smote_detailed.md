### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Low | Med | Med | Med | Low | Hi | Hi | N |
| run17 | Med | Med | Med | Med | Hi | Low | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Low | Low | Low | Med | Med | Med | Med | Med | Hi | ~ |
| run25 | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Hi | Hi | Low | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run31 | Med | Hi | Med | Hi | Hi | Low | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Med | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Low | Low | Med | Med | Med | Hi | Low | Low | Y |
| run45 | Med | Hi | Low | Hi | Low | Med | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Hi | Low | Med | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Med | Low | Hi | Low | Med | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Hi | Low | Hi | Low | Med | Med | Hi | Hi | Hi | Hi | N |

Window accuracy: **50.0%** (54/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.667 | 0.500 | 0.571 | 4 |
| 5-6 mm/rev (med) | 1.000 | 0.500 | 0.667 | 4 |
| 7-8 mm/rev (high) | 0.571 | 1.000 | 0.727 | 4 |
| **macro avg** | **0.746** | **0.667** | **0.655** | |