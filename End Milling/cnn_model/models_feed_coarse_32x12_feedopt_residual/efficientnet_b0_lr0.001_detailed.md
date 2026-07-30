### efficientnet_b0_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Hi | Med | Hi | Hi | Hi | N |
| run3 | Hi | Low | Hi | Med | Low | Hi | ~ |
| run31 | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Med | Low | Hi | Med | Med | N |
| run45 | Med | Med | Hi | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.400 | 1.000 | 0.571 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.300** | **0.417** | **0.302** | |