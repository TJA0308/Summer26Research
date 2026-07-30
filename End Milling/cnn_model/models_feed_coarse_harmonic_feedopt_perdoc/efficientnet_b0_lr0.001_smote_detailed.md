### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=harmonic_feedopt_perdoc  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Hi | Low | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | N |
| run25 | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Low | Low | Low | Low | Low | N |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Low | Med | ~ |
| run5 | Hi | Low | Low | Low | Low | Low | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Hi | Low | Med | Med | Y |

Window accuracy: **25.0%** (9/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.750 | 0.462 | 4 |
| 5-6 mm/rev (med) | 0.667 | 0.500 | 0.571 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.333** | **0.417** | **0.344** | |