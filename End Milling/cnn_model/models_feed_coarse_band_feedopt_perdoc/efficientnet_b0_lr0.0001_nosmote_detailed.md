### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=band_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Low | Hi | Med | Low | Low | N |
| run21 | Hi | Low | Low | Med | Low | Low | N |
| run25 | Low | Low | Hi | Med | Low | Low | Y |
| run3 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Low | Med | Low | Low | N |
| run37 | Low | Low | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Hi | Med | Low | Low | Y |
| run9 | Med | Med | Hi | Med | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.500 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.600 | 0.750 | 0.667 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.644** | **0.500** | **0.489** | |