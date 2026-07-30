### efficientnet_b0_lr0.001  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Hi | Hi | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Low | Hi | Hi | Low | Low | N |
| run31 | Med | Low | Hi | Low | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | N |
| run36 | Hi | Low | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Low | Med | Med | Low | Med | Med | Med | Low | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Low | Hi | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Hi | Hi | Hi | Hi | Low | Hi | Low | Hi | Low | N |

Window accuracy: **61.1%** (66/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.571 | 1.000 | 0.727 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.390** | **0.583** | **0.465** | |