### resnet18_lr0.0001  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Low | Hi | Low | Low | Low | Low | Hi | Low | Low | Hi | Low | Low | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Low | Low | Med | Med | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Med | Med | Med | Med | Med | Low | Low | Low | Med | Med | N |
| run45 | Med | Hi | Hi | Low | Low | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | N |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Hi | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Med | Med | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Med | Low | Med | Low | Low | Med | Med | Y |

Window accuracy: **57.5%** (69/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.750 | 0.750 | 0.750 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.250 | 0.286 | 4 |
| 7-8 mm/rev (high) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.561** | **0.583** | **0.567** | |