### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=harmonic_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Med | Med | Low | Med | Med | Y |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Med | Hi | Hi | Hi | N |
| run3 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Med | Low | Med | Med | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Med | Hi | Med | N |
| run45 | Med | Med | Med | Hi | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Med | Hi | Med | Med | N |
| run9 | Med | Med | Med | Hi | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.571 | 1.000 | 0.727 | 4 |
| 7-8 mm/rev (high) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.390** | **0.583** | **0.465** | |