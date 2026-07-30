### resnet50_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run17 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Low | N |
| run25 | Low | Low | Low | Low | Low | Low | Hi | Med | Med | Hi | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Low | Hi | N |
| run36 | Hi | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Low | Low | Low | Low | Low | Med | Med | Med | Hi | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **34.3%** (37/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.375 | 0.750 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.250 | 0.286 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.236** | **0.333** | **0.262** | |