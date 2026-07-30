### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Hi | Med | Low | Med | Low | Low | Low | Y |
| run17 | Med | Low | Low | Med | Low | Med | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Med | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Med | Low | Med | Med | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Hi | Med | Low | Low | Med | Med | Low | Low | N |
| run31 | Med | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Low | Med | Low | Low | Low | Med | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Med | Med | Low | Low | Low | Low | Med | Low | Low | Y |
| run45 | Med | Low | Med | Med | Med | Med | Med | Hi | Low | Low | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Low | Low | Med | Med | Med | Med | Med | Y |

Window accuracy: **43.5%** (47/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.571 | 1.000 | 0.727 | 4 |
| 5-6 mm/rev (med) | 0.600 | 0.750 | 0.667 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.390** | **0.583** | **0.465** | |