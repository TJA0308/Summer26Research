### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=raw_10w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Low | Low | Hi | Low | Hi | Low | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Hi | Low | Low | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Low | Hi | Low | Low | Hi | Hi | Low | Hi | Low | Y |
| run31 | Med | Hi | Low | Low | Low | Hi | Med | Hi | Hi | Low | Hi | Hi | Hi | N |
| run36 | Hi | Low | Low | Hi | Low | Low | Hi | Low | Low | Low | Low | Low | Low | N |
| run37 | Low | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Hi | Med | Low | Low | Low | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Med | Med | Low | Low | N |

Window accuracy: **49.2%** (59/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.444 | 1.000 | 0.615 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.370** | **0.500** | **0.396** | |