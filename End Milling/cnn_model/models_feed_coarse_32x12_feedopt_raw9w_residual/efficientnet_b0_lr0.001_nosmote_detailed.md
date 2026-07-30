### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Med | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Low | Hi | Hi | N |
| run45 | Med | Hi | Low | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Low | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **40.7%** (44/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.250 | 0.286 | 4 |
| 7-8 mm/rev (high) | 0.444 | 1.000 | 0.615 | 4 |
| **macro avg** | **0.259** | **0.417** | **0.300** | |