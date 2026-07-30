### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Hi | Low | Hi | Hi | Med | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Hi | Hi | Low | Low | Hi | Low | Low | N |
| run25 | Low | Low | Med | Low | Hi | Low | Low | Low | Med | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Hi | Low | Med | Low | Low | Med | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Low | Hi | Hi | Low | Med | Low | Low | Low | N |
| run36 | Hi | Hi | Low | Hi | Med | Hi | Med | Hi | Hi | Low | Hi | Hi | Y |
| run37 | Low | Med | Low | Low | Hi | Low | Med | Med | Med | Low | Med | Low | ~ |
| run45 | Med | Hi | Hi | Hi | Med | Med | Low | Low | Med | Hi | Hi | Hi | N |
| run5 | Hi | Med | Low | Med | Low | Hi | Low | Low | Med | Hi | Low | Low | N |
| run7 | Low | Hi | Low | Med | Med | Low | Low | Low | Low | Hi | Low | Low | Y |
| run9 | Med | Hi | Med | Med | Hi | Hi | Hi | Low | Low | Low | Hi | Hi | N |

Window accuracy: **35.2%** (38/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.444 | 1.000 | 0.615 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.333 | 0.250 | 0.286 | 4 |
| **macro avg** | **0.259** | **0.417** | **0.300** | |