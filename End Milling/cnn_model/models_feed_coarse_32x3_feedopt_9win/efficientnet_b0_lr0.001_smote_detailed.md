### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Hi | Hi | Hi | Hi | Hi | Hi | Med | Low | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Med | Med | Med | Med | Low | Low | Med | Low | N |
| run31 | Med | Low | Med | Hi | Hi | Hi | Med | Med | Low | Low | Low | Low | N |
| run36 | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | N |
| run45 | Med | Low | Low | Med | Med | Low | Low | Low | Low | Med | Low | Low | N |
| run5 | Hi | Low | Low | Low | Low | Med | Med | Med | Med | Low | Low | Low | N |
| run7 | Low | Low | Low | Med | Med | Med | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **37.0%** (40/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.375 | 0.750 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.333 | 0.250 | 0.286 | 4 |
| **macro avg** | **0.236** | **0.333** | **0.262** | |