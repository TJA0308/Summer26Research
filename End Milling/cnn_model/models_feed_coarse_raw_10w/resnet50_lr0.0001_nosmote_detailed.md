### resnet50_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=raw_10w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Hi | Med | Med | Med | Hi | Med | Hi | Med | Med | Hi | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Med | Med | Hi | ~ |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Hi | Hi | Hi | Med | Hi | Med | Med | Hi | Med | Med | Hi | ~ |
| run7 | Low | Med | Hi | Hi | Hi | Med | Hi | Hi | Low | Hi | Med | Hi | Med | N |
| run9 | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **45.0%** (54/120)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.429 | 0.750 | 0.545 | 4 |
| 7-8 mm/rev (high) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.343** | **0.500** | **0.404** | |