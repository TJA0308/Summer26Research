### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Low | Med | Low | Hi | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Med | Hi | Hi | Hi | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Med | Low | Hi | Hi | Low | Low | Low | Hi | Low | Low | N |
| run25 | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Low | Med | Low | Low | Med | Med | N |
| run31 | Med | Low | Med | Med | Hi | Low | Low | Low | Low | Hi | Low | Low | N |
| run36 | Hi | Low | Med | Med | Low | Hi | Low | Low | Hi | Hi | Low | Low | N |
| run37 | Low | Low | Med | Low | Hi | Hi | Low | Low | Low | Hi | Low | Low | Y |
| run45 | Med | Med | Low | Med | Low | Med | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Low | Med | Low | Hi | Low | Hi | Low | Hi | Low | Low | N |
| run7 | Low | Med | Low | Low | Low | Hi | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Hi | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **41.7%** (45/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.400 | 1.000 | 0.571 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.250 | 0.333 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.300** | **0.417** | **0.302** | |