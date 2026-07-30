### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Med | Hi | Med | Med | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Low | Low | Hi | Med | Low | Low | Med | Low | Low | N |
| run31 | Med | Med | Low | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run37 | Low | Low | Hi | Low | Hi | Hi | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Med | Low | Med | Low | Med | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **49.1%** (53/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.571 | 1.000 | 0.727 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.357** | **0.500** | **0.409** | |