### resnet18_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Low | Med | Med | Med | Low | Low | Low | Low | Low | Med | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Med | Med | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **32.4%** (35/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.273 | 0.750 | 0.400 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.091** | **0.250** | **0.133** | |