### resnet18_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Low | Low | Y |
| run17 | Med | Low | Med | Low | Med | Med | Med | Low | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Med | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Hi | Med | Med | Hi | Hi | Low | Hi | Low | Med | Hi | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Hi | Med | Hi | Hi | Hi | Med | Med | N |
| run7 | Low | Low | Low | Med | Med | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Med | Med | Low | Low | Low | Med | Med | Y |

Window accuracy: **62.5%** (75/120)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.750 | 0.857 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.500 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.700** | **0.667** | **0.675** | |