### resnet50_lr0.001_dropout03_ls01  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Hi | Med | Hi | N |
| run17 | Med | Med | Low | Hi | Med | Hi | Y |
| run21 | Hi | Med | Low | Hi | Med | Med | N |
| run25 | Low | Hi | Low | Hi | Hi | Hi | N |
| run3 | Hi | Med | Med | Hi | Med | Med | N |
| run31 | Med | Med | Low | Hi | Med | Hi | Y |
| run36 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run37 | Low | Med | Low | Hi | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run7 | Low | Low | Hi | Hi | Hi | Hi | N |
| run9 | Med | Low | Low | Med | Low | Low | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.250 | 0.250 | 0.250 | 4 |
| 7-8 mm/rev (high) | 0.286 | 0.500 | 0.364 | 4 |
| **macro avg** | **0.179** | **0.250** | **0.205** | |