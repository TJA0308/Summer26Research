### convnext_tiny_lr0.0001_cascade_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Med | Med | Med | N |
| run17 | Med | Med | Hi | Med | Med | Hi | Y |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Med | Hi | Med | ~ |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Med | Med | Low | Med | Med | N |
| run9 | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.667 | 0.500 | 0.571 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.500 | 0.400 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.556** | **0.500** | **0.514** | |