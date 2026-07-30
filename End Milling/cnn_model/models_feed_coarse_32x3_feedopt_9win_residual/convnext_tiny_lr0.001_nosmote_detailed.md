### convnext_tiny_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run36 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **33.3%** (36/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 1.000 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.111** | **0.333** | **0.167** | |