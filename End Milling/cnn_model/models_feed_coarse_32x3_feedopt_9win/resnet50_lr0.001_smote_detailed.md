### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Low | Low | Low | Low | Med | Med | N |
| run17 | Med | Low | Low | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Low | Med | Low | Low | Hi | Hi | Med | Med | Low | Low | Low | N |
| run25 | Low | Low | Med | Med | Low | Low | Med | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run31 | Med | Low | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Med | Low | Low | Low | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Med | Low | Low | Low | Med | Med | Y |
| run5 | Hi | Low | Low | Low | Low | Low | Low | Med | Med | Med | Low | Low | N |
| run7 | Low | Low | Low | Low | Med | Low | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.750 | 0.600 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.750 | 0.600 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.333** | **0.500** | **0.400** | |