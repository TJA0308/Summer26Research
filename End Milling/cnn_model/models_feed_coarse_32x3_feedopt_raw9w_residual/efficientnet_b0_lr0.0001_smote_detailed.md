### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Low | Med | Hi | Hi | Med | Med | Hi | Low | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Med | Hi | Hi | Hi | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Med | Med | Med | Hi | Hi | Med | Hi | Hi | Hi | Hi | N |
| run9 | Med | Med | Med | Low | Hi | Hi | Med | Med | Hi | Med | Med | Med | Y |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.667 | 0.500 | 0.571 | 4 |
| 7-8 mm/rev (high) | 0.500 | 1.000 | 0.667 | 4 |
| **macro avg** | **0.722** | **0.583** | **0.546** | |