### resnet18_lr0.001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Low | Low | Hi | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Med | Med | Hi | Hi | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Low | Med | Med | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Hi | Low | Med | Low | Low | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **43.5%** (47/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.667 | 0.500 | 0.571 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.250 | 0.286 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.750 | 0.600 | 4 |
| **macro avg** | **0.500** | **0.500** | **0.486** | |