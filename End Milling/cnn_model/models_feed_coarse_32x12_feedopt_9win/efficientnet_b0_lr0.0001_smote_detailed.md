### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Med | Med | Med | Med | Med | Hi | Hi | Hi | Hi | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Med | Med | Med | Med | Hi | Med | Hi | Hi | Med | Med | Y |
| run36 | Hi | Med | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Med | Med | Med | Hi | Hi | Hi | Med | Med | Med | N |
| run45 | Med | Med | Med | Hi | Med | Hi | Hi | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Hi | Med | Hi | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Med | Med | Med | Med | Hi | Med | Hi | Hi | Med | Med | N |
| run9 | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.667 | 1.000 | 0.800 | 4 |
| 7-8 mm/rev (high) | 0.667 | 1.000 | 0.800 | 4 |
| **macro avg** | **0.444** | **0.667** | **0.533** | |