### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Hi | Med | Med | Hi | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Med | Med | Med | Low | Med | Hi | Hi | Hi | Hi | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Low | Low | Med | Low | Med | Med | Med | Low | Med | Med | Med | N |
| run3 | Hi | Low | Hi | Med | Med | Med | Med | Med | Med | Hi | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Low | Med | Med | Hi | Hi | Hi | Med | Med | Hi | ~ |
| run37 | Low | Med | Med | Low | Low | Med | Med | Med | Med | Hi | Med | Med | N |
| run45 | Med | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Low | Low | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Med | Low | Med | Med | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **49.1%** (53/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.500 | 1.000 | 0.667 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.722** | **0.583** | **0.546** | |