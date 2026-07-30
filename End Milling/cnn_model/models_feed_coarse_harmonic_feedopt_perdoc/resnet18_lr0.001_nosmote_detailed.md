### resnet18_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=harmonic_feedopt_perdoc  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Med | Hi | Low | Med | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | N |
| run37 | Low | Hi | Med | Med | Med | Hi | N |
| run45 | Med | Med | Hi | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Hi | Low | Low | N |
| run7 | Low | Low | Low | Hi | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.250 | 0.286 | 4 |
| 5-6 mm/rev (med) | 0.375 | 0.750 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.236** | **0.333** | **0.262** | |