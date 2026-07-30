### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | Hi | Med | Low | Low | Med | Med | N |
| run17 | Med | Hi | Low | Low | Hi | Med | Low | Low | Low | Hi | Low | Low | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Low | Low | Med | Med | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Low | Med | Med | Med | Med | Hi | Hi | Med | Hi | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Low | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Med | Med | Low | Low | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Med | Low | Med | Med | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Low | Low | Med | Hi | Low | Low | Y |
| run9 | Med | Low | Low | Low | Med | Med | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **59.3%** (64/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.500 | 0.500 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.250 | 0.286 | 4 |
| 7-8 mm/rev (high) | 0.800 | 1.000 | 0.889 | 4 |
| **macro avg** | **0.544** | **0.583** | **0.558** | |