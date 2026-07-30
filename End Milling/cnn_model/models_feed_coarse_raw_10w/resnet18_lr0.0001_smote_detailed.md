### resnet18_lr0.0001_smote  |  target=feed_coarse  |  scalogram=raw_10w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Low | Med | Med | Med | Low | Med | Med | Med | Med | N |
| run17 | Med | Hi | Low | Hi | Low | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Med | Med | Med | Low | Med | Med | Low | Med | Med | Med | N |
| run45 | Med | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Med | Med | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | ~ |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **60.0%** (72/120)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.500 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.250 | 0.286 | 4 |
| 7-8 mm/rev (high) | 0.800 | 1.000 | 0.889 | 4 |
| **macro avg** | **0.544** | **0.583** | **0.558** | |