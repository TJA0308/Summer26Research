### resnet18_lr0.0001_ordinal_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Low | Hi | Med | N |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Med | Hi | Low | Med | N |
| run25 | Low | Low | Med | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Med | Hi | Low | Med | N |
| run37 | Low | Low | Med | Med | Med | Med | N |
| run45 | Med | Hi | Med | Med | Med | Low | Y |
| run5 | Hi | Low | Med | Med | Med | Med | N |
| run7 | Low | Low | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.250 | 0.286 | 4 |
| 5-6 mm/rev (med) | 0.222 | 0.500 | 0.308 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.185** | **0.250** | **0.198** | |