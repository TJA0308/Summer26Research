### resnet18_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Hi | Med | Med | N |
| run17 | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Med | Low | Hi | Med | Low | N |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Med | Low | Hi | Med | Med | N |
| run31 | Med | Med | Low | Hi | Med | Low | Y |
| run36 | Hi | Med | Low | Hi | Med | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Low | Low | Hi | Low | Low | N |
| run7 | Low | Med | Low | Hi | Med | Low | ~ |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.750 | 0.462 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.111** | **0.250** | **0.154** | |