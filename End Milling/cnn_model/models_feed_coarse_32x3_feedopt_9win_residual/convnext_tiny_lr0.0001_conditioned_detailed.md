### convnext_tiny_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | Med | Med | Low | Low | Med | Med | N |
| run17 | Med | Hi | Med | Med | Hi | Med | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Med | Med | Med | Hi | Hi | Med | Hi | Hi | Med | Y |
| run31 | Med | Hi | Med | Med | Med | Hi | Med | Hi | Med | Hi | Med | Hi | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Hi | Med | Hi | Hi | Y |
| run37 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Low | Low | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Hi | Hi | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Med | Low | Med | Low | Low | Low | Med | Med | Med | Med | N |
| run9 | Med | Low | Low | Med | Med | Med | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **52.8%** (57/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.250 | 0.333 | 4 |
| 5-6 mm/rev (med) | 0.286 | 0.500 | 0.364 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.484** | **0.417** | **0.423** | |