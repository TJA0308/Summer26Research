### resnet18_lr0.001_smote  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Low | Med | Low | Med | Med | Med | Med | Low | Hi | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Low | Low | Low | Low | Low | Low | Hi | Hi | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Hi | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Med | Med | Low | Hi | Hi | Low | Med | Hi | Hi | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Low | Low | Hi | Hi | N |

Window accuracy: **53.3%** (64/120)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.500 | 0.667 | 4 |
| 5-6 mm/rev (med) | 0.667 | 0.500 | 0.571 | 4 |
| 7-8 mm/rev (high) | 0.571 | 1.000 | 0.727 | 4 |
| **macro avg** | **0.746** | **0.667** | **0.655** | |