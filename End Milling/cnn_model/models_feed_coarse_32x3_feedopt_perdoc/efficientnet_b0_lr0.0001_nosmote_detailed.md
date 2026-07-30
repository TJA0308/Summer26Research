### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Med | Med | Med | Med | N |
| run25 | Low | Med | Low | Med | Med | Med | N |
| run3 | Hi | Low | Med | Low | Low | Low | N |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Low | Med | Low | Low | N |
| run5 | Hi | Med | Low | Low | Low | Low | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.167 | 0.250 | 0.200 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.500 | 0.400 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.167** | **0.250** | **0.200** | |