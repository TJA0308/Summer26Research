### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=band_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Hi | Hi | Hi | Hi | N |
| run17 | Med | Low | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Low | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Low | Hi | Hi | Hi | Hi | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.364 | 1.000 | 0.533 | 4 |
| **macro avg** | **0.455** | **0.417** | **0.311** | |