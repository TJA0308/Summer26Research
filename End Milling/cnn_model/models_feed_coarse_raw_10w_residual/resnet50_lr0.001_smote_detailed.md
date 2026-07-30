### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Med | Hi | Med | Hi | Med | Low | Low | Y |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Med | Med | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Hi | Med | Med | Med | Low | Hi | Med | Med | Low | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Med | Med | Hi | Med | Med | Low | Med | Med | Med | Low | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **61.7%** (74/120)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.750 | 0.750 | 0.750 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.500 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.750 | 0.750 | 0.750 | 4 |
| **macro avg** | **0.667** | **0.667** | **0.667** | |