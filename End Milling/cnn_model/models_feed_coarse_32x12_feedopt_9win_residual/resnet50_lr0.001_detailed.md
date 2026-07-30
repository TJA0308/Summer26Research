### resnet50_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Med | Low | Low | Med | Med | Hi | Low | Low | Y |
| run9 | Med | Low | Low | Low | Med | Med | Med | Med | Low | Low | Low | Med | ~ |

Window accuracy: **56.5%** (61/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.750 | 0.857 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.500 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.700** | **0.667** | **0.675** | |