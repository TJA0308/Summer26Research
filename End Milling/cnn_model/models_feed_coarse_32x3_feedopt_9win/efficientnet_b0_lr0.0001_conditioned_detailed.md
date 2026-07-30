### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Med | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Low | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Med | Low | Low | Low | Low | Low | Med | Low | Low | Low | N |
| run25 | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Med | Med | Low | Low | Low | Low | Med | Low | Low | N |
| run31 | Med | Med | Low | Hi | Med | Low | Low | Low | Low | Med | Low | Low | N |
| run36 | Hi | Med | Low | Low | Med | Low | Med | Low | Low | Med | Low | Low | N |
| run37 | Low | Med | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Low | Med | Low | Low | Med | Med | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Med | Low | Low | Med | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Med | Med | Low | Low | Low | Med | Med | Y |

Window accuracy: **41.7%** (45/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.400 | 1.000 | 0.571 | 4 |
| 5-6 mm/rev (med) | 1.000 | 0.500 | 0.667 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.467** | **0.500** | **0.413** | |