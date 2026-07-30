### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Med | Med | Hi | Med | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Med | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Low | Hi | Hi | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Low | Med | Low | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Med | Low | Med | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.750 | 0.750 | 0.750 | 4 |
| 5-6 mm/rev (med) | 0.429 | 0.750 | 0.545 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.726** | **0.583** | **0.565** | |