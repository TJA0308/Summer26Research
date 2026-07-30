### resnet18_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Med | Med | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | Hi | Med | Hi | Hi | Med | Med | N |
| run25 | Low | Med | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Low | Low | Med | Med | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Low | Low | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Low | Med | Low | Med | Low | Low | Low | Med | Low | Low | N |
| run5 | Hi | Med | Low | Low | Low | Med | Med | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **33.3%** (36/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.500 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.286 | 0.500 | 0.364 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.262** | **0.333** | **0.288** | |