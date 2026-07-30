### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Low | Hi | Low | N |
| run21 | Hi | Hi | Low | Hi | Hi | Med | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Med | Low | Low | Y |
| run45 | Med | Med | Low | Med | Med | Med | Y |
| run5 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Low | Med | Low | Y |

Window accuracy: **61.1%** (22/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.600 | 0.750 | 0.667 | 4 |
| 5-6 mm/rev (med) | 0.400 | 0.500 | 0.444 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.667** | **0.583** | **0.593** | |