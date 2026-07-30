### resnet50_lr0.0001  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Med | Hi | Hi | Low | Med | Low | Hi | Med | Med | Hi | N |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Hi | Med | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | N |
| run37 | Low | Low | Low | Med | Low | Med | Low | Hi | Low | Hi | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Low | Med | Low | Low | Hi | Hi | Med | Hi | Med | Med | N |
| run7 | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Med | Low | Low | Low | Low | Med | Med | Low | Y |

Window accuracy: **54.2%** (65/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.750 | 0.750 | 0.750 | 4 |
| 5-6 mm/rev (med) | 0.400 | 0.500 | 0.444 | 4 |
| 7-8 mm/rev (high) | 0.333 | 0.250 | 0.286 | 4 |
| **macro avg** | **0.494** | **0.500** | **0.493** | |