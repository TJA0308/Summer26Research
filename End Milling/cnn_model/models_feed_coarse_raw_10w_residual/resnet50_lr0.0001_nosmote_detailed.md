### resnet50_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Med | Hi | Med | Med | Hi | Hi | Hi | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Med | Med | Hi | Med | Med | Hi | Hi | Hi | N |
| run36 | Hi | Med | Med | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Med | Hi | ~ |
| run37 | Low | Hi | Med | Med | Hi | Med | Low | Med | Med | Hi | Med | Med | Hi | N |
| run45 | Med | Med | Med | Hi | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Hi | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Med | Med | Low | Low | N |

Window accuracy: **51.7%** (62/120)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.667 | 0.500 | 0.571 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.250 | 0.333 | 4 |
| 7-8 mm/rev (high) | 0.429 | 0.750 | 0.545 | 4 |
| **macro avg** | **0.532** | **0.500** | **0.483** | |