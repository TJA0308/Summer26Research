### efficientnet_b0_lr0.001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Y |
| run17 | Med | Med | Low | Hi | Hi | Hi | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Med | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Low | Low | Low | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Low | Hi | Low | Hi | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Med | Med | Med | Low | Med | Hi | ~ |
| run37 | Low | Low | Low | Low | Low | Low | Low | Low | Med | Med | Low | Low | Y |
| run45 | Med | Med | Low | Low | Low | Low | Med | Med | Low | Low | Low | Low | N |
| run5 | Hi | Low | Hi | Low | Hi | Low | Low | Low | Low | Low | Low | Low | N |
| run7 | Low | Low | Low | Low | Low | Low | Hi | Hi | Hi | Hi | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Med | Med | Med | Med | Low | Low | N |

Window accuracy: **51.9%** (56/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.571 | 1.000 | 0.727 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.500 | 0.500 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.690** | **0.583** | **0.542** | |