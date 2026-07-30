### resnet50_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Hi | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Hi | Low | Low | Hi | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Hi | Hi | Hi | Med | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run31 | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Hi | Med | Med | Hi | Med | Hi | Med | Hi | Y |
| run5 | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run7 | Low | Med | Med | Med | Hi | Med | Med | Hi | Med | Med | Med | Med | N |
| run9 | Med | Med | Hi | Med | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **43.5%** (47/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.400 | 1.000 | 0.571 | 4 |
| **macro avg** | **0.467** | **0.417** | **0.324** | |