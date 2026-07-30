### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Low | Hi | Med | Hi | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Low | Hi | Low | Hi | Med | Hi | Med | Med | N |
| run25 | Low | Med | Med | Hi | Med | Med | Low | Hi | Hi | Hi | Med | Med | N |
| run3 | Hi | Hi | Med | Low | Hi | Med | Hi | Hi | Med | Low | Hi | Hi | Y |
| run31 | Med | Med | Low | Hi | Med | Low | Low | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Low | Med | Hi | Low | Med | Hi | Hi | Med | Med | Med | N |
| run37 | Low | Hi | Low | Hi | Low | Hi | Med | Low | Low | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Hi | Hi | Med | Hi | Med | Med | N |
| run7 | Low | Low | Med | Med | Med | Low | Low | Hi | Hi | Hi | Low | Hi | Y |
| run9 | Med | Med | Med | Med | Med | Med | Hi | Med | Hi | Med | Med | Med | Y |

Window accuracy: **46.3%** (50/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.444 | 1.000 | 0.615 | 4 |
| 7-8 mm/rev (high) | 0.333 | 0.250 | 0.286 | 4 |
| **macro avg** | **0.259** | **0.417** | **0.300** | |