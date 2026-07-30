### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Low | Low | Low | Hi | Low | Hi | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Low | Low | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Low | Low | Low | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Low | Hi | Low | Hi | Hi | Hi | Low | Hi | Hi | N |
| run45 | Med | Hi | Low | Hi | Hi | Hi | Low | Low | Hi | Low | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Med | Low | Low | Low | Low | Low | Hi | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Hi | Low | Hi | Hi | Med | Low | Med | Low | Low | N |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.750 | 0.600 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.333 | 0.500 | 0.400 | 4 |
| **macro avg** | **0.278** | **0.417** | **0.333** | |