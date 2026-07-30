### convnext_tiny_lr0.0001_smote  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Med | Low | Low | Low | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Hi | Med | Med | Med | Hi | Hi | Hi | Hi | Med | Med | Hi | ~ |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Hi | Hi | Low | Hi | Low | Hi | Low | Hi | Low | Y |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Low | Low | Med | Med | N |
| run7 | Low | Low | Med | Med | Med | Low | Med | Low | Low | Med | Low | Low | Med | Y |
| run9 | Med | Low | Med | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **50.8%** (61/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.500 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.429 | 0.750 | 0.545 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.643** | **0.500** | **0.482** | |