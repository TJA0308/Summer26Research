### convnext_tiny_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run17 | Med | Hi | Low | Low | Hi | Low | Med | Med | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Low | Hi | Hi | Low | Med | Med | Med | Low | Hi | Med | Y |
| run25 | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Hi | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run31 | Med | Med | Low | Low | Hi | Low | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Med | Low | Low | Low | Low | Med | Hi | Hi | Hi | Low | Low | N |
| run37 | Low | Med | Hi | Low | Hi | Hi | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | N |
| run7 | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.750 | 0.600 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.750 | 0.600 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.333** | **0.500** | **0.400** | |