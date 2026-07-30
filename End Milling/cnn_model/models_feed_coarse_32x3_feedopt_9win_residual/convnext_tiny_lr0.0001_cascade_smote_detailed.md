### convnext_tiny_lr0.0001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Med | Med | Hi | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Low | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Med | Low | Low | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Med | Low | Med | Med | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Med | Med | Low | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.250 | 0.333 | 4 |
| 5-6 mm/rev (med) | 0.375 | 0.750 | 0.500 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.625** | **0.500** | **0.500** | |