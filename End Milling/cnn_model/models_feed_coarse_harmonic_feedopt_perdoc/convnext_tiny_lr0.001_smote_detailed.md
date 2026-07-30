### convnext_tiny_lr0.001_smote  |  target=feed_coarse  |  scalogram=harmonic_feedopt_perdoc  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Y |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Low | Low | Low | N |
| run31 | Med | Med | Low | Low | Low | Low | N |
| run36 | Hi | Med | Med | Low | Med | Med | N |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Med | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.444 | 1.000 | 0.615 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.315** | **0.417** | **0.316** | |