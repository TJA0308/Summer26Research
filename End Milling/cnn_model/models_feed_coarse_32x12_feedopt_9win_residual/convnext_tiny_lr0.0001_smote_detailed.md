### convnext_tiny_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Low | Med | Hi | Med | Hi | Hi | Hi | Hi | Med | ~ |
| run36 | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | Med | Y |
| run7 | Low | Low | Low | Med | Med | Med | Low | Low | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.9%** (55/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.429 | 0.750 | 0.545 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.643** | **0.500** | **0.482** | |