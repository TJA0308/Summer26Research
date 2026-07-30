### efficientnet_b0_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Low | Med | Low | Low | Med | ~ |
| run21 | Hi | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Low | Low | Low | N |
| run36 | Hi | Low | Med | Med | Med | Med | N |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.750 | 0.750 | 0.750 | 4 |
| 5-6 mm/rev (med) | 0.375 | 0.750 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.375** | **0.500** | **0.417** | |