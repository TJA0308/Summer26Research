### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Med | Hi | Hi | Med | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Med | Med | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | N |
| run36 | Hi | Med | Hi | Med | Med | Med | Med | Hi | Hi | Hi | Hi | Med | Hi | ~ |
| run37 | Low | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | N |
| run45 | Med | Med | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Med | Med | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Med | Low | Low | Med | Med | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (60/120)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.500 | 0.667 | 4 |
| 5-6 mm/rev (med) | 1.000 | 0.250 | 0.400 | 4 |
| 7-8 mm/rev (high) | 0.444 | 1.000 | 0.615 | 4 |
| **macro avg** | **0.815** | **0.583** | **0.561** | |