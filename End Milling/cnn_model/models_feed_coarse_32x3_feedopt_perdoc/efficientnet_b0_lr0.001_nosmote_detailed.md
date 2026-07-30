### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Hi | Med | Med | N |
| run17 | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Med | Hi | Low | Med | Med | N |
| run3 | Hi | Hi | Med | Low | Hi | Med | Y |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Low | Low | Low | Low | N |
| run37 | Low | Med | Hi | Low | Med | Low | ~ |
| run45 | Med | Hi | Med | Hi | Hi | Hi | N |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Med | Low | Med | Med | Med | N |
| run9 | Med | Low | Med | Hi | Low | Med | ~ |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.250 | 0.333 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.750 | 0.462 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.278** | **0.333** | **0.265** | |