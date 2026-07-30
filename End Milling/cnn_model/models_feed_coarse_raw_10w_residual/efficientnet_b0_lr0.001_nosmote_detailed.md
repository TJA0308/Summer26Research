### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Low | Med | Low | Hi | Med | Low | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Med | Med | Low | Low | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Low | Low | Hi | Med | Med | Med | Hi | Hi | Med | Med | Hi | ~ |
| run37 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run45 | Med | Med | Med | Hi | Low | Med | Med | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | N |

Window accuracy: **52.5%** (63/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.750 | 0.750 | 0.750 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.750 | 0.600 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.750** | **0.667** | **0.672** | |