### resnet18_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | N |
| run17 | Med | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | Hi | Med | Hi | Med | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Med | Med | Hi | Med | Y |
| run37 | Low | Low | Low | Med | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Med | Hi | Hi | N |
| run5 | Hi | Med | Med | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Med | Med | Low | Low | Low | Low | Med | Med | Med | N |
| run9 | Med | Med | Hi | Med | Med | Low | Med | Med | Low | Low | Med | Med | Y |

Window accuracy: **59.3%** (64/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.429 | 0.750 | 0.545 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.643** | **0.500** | **0.482** | |