### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Hi | Hi | Low | Y |
| run31 | Med | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Low | Low | Hi | Low | Hi | ~ |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Hi | Low | Hi | Hi | Low | N |
| run5 | Hi | Hi | Low | Med | Hi | Low | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.444 | 1.000 | 0.615 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.370** | **0.500** | **0.396** | |