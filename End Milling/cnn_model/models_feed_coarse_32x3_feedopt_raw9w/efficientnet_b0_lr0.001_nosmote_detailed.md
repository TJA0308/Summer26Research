### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | Low | Low | Low | Med | Med | Med | N |
| run17 | Med | Low | Low | Low | Hi | Low | Low | Low | Hi | Low | Low | Low | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run31 | Med | Med | Low | Med | Med | Med | Low | Med | Low | Low | Med | Low | Y |
| run36 | Hi | Low | Low | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | Low | Y |
| run37 | Low | Hi | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Hi | Hi | Low | Hi | Hi | Low | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | N |

Window accuracy: **50.9%** (55/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.375 | 0.750 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.347** | **0.417** | **0.357** | |