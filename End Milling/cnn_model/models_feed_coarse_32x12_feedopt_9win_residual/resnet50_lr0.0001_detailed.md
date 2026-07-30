### resnet50_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | N |
| run17 | Med | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Med | Med | Med | Med | Med | Hi | Med | Hi | Med | Med | Y |
| run5 | Hi | Med | Hi | Med | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Low | Hi | Hi | Hi | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Hi | Low | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.500 | 0.667 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.250 | 0.333 | 4 |
| 7-8 mm/rev (high) | 0.500 | 1.000 | 0.667 | 4 |
| **macro avg** | **0.667** | **0.583** | **0.556** | |