### resnet50_lr0.0001_smote  |  target=feed_coarse  |  scalogram=raw_10w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Low | Hi | Med | Med | Hi | Med | Med | Hi | Hi | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Med | Med | Med | Low | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Hi | Low | Hi | Low | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run31 | Med | Med | Med | Hi | Med | Med | Med | Hi | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | N |
| run45 | Med | Low | Med | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Hi | Hi | Hi | Med | Hi | Hi | Low | Med | Med | Hi | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **56.7%** (68/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.750 | 0.600 | 4 |
| 7-8 mm/rev (high) | 0.800 | 1.000 | 0.889 | 4 |
| **macro avg** | **0.433** | **0.583** | **0.496** | |