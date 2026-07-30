### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Hi | Hi | Hi | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Low | Low | Low | Low | Low | Low | Low | N |
| run37 | Low | Med | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Low | Low | Med | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **63.9%** (69/108)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.750 | 0.750 | 0.750 | 4 |
| 5-6 mm/rev (med) | 0.667 | 1.000 | 0.800 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.806** | **0.750** | **0.739** | |