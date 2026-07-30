### resnet18_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Med | Low | Low | Low | N |
| run25 | Low | Low | Med | Hi | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Med | Low | N |
| run31 | Med | Low | Low | Med | Low | Low | N |
| run36 | Hi | Low | Med | Hi | Low | Low | N |
| run37 | Low | Med | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Low | Med | Hi | Low | Low | N |
| run7 | Low | Low | Med | Med | Med | Med | N |
| run9 | Med | Low | Med | Med | Med | Low | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.250 | 0.500 | 0.333 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.500 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.250** | **0.333** | **0.278** | |