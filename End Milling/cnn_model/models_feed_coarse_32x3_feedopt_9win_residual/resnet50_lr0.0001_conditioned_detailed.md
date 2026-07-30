### resnet50_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Low | Low | Hi | Hi | Hi | Med | Med | Med | N |
| run25 | Low | Med | Low | Low | Low | Low | Med | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Low | Med | Med | Med | Low | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Med | Low | Low | Med | Med | Med | Low | Med | Med | N |
| run37 | Low | Low | Med | Low | Low | Low | Hi | Hi | Hi | Med | Low | Med | Y |
| run45 | Med | Med | Med | Med | Hi | Hi | Hi | Med | Hi | Med | Med | Hi | Y |
| run5 | Hi | Hi | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Med | Med | Low | Med | Med | Med | Med | Med | Y |

Window accuracy: **46.3%** (50/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.300 | 0.750 | 0.429 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.433** | **0.333** | **0.276** | |