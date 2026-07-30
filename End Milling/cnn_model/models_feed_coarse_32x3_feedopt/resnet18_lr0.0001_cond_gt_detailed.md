### resnet18_lr0.0001_cond_gt  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Hi | Hi | Hi | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run25 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Med | Med | Hi | Med | Hi | ~ |
| run31 | Med | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Hi | Med | Hi | N |
| run45 | Med | Med | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 1.000 | 0.250 | 0.400 | 4 |
| 7-8 mm/rev (high) | 0.364 | 1.000 | 0.533 | 4 |
| **macro avg** | **0.455** | **0.417** | **0.311** | |