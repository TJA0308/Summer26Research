### efficientnet_b0_lr0.001_cond_gt  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Hi | Hi | Hi | N |
| run17 | Med | Med | Hi | Low | Med | Low | Y |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Hi | Med | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Med | Low | Hi | Med | Y |
| run31 | Med | Hi | Low | Low | Low | Low | N |
| run36 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Low | Hi | Low | Low | Hi | Y |
| run45 | Med | Hi | Hi | Low | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run7 | Low | Hi | Low | Low | Low | Low | Y |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.250 | 0.286 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.375 | 0.750 | 0.500 | 4 |
| **macro avg** | **0.236** | **0.333** | **0.262** | |