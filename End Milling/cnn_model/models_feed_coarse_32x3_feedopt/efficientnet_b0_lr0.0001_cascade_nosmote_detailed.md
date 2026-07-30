### efficientnet_b0_lr0.0001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Hi | Med | Low | Low | N |
| run21 | Hi | Low | Hi | Med | Low | Low | N |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Low | Hi | Med | Low | Low | N |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Med | Low | Med | Med | Med | Y |

Window accuracy: **25.0%** (9/36)
Run hard-vote accuracy: **16.7%** (2/12)
Run soft-vote accuracy: **16.7%** (2/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.250 | 0.500 | 0.333 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.083** | **0.167** | **0.111** | |