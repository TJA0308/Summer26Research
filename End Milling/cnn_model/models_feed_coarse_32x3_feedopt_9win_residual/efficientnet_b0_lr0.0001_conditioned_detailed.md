### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Med | Low | Low | Low | Med | Med | Low | Med | Low | Low | Y |
| run17 | Med | Med | Low | Low | Med | Low | Low | Low | Med | Med | Low | Low | N |
| run21 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run25 | Low | Med | Med | Low | Hi | Low | Med | Low | Low | Med | Med | Med | N |
| run3 | Hi | Low | Med | Low | Low | Low | Low | Low | Med | Med | Low | Low | N |
| run31 | Med | Hi | Low | Med | Low | Low | Low | Med | Low | Med | Low | Low | N |
| run36 | Hi | Low | Low | Low | Med | Low | Low | Low | Low | Med | Low | Low | N |
| run37 | Low | Low | Med | Low | Low | Med | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Med | Low | Low | Low | Med | Med | Med | Low | Low | Low | N |
| run5 | Hi | Low | Low | Low | Med | Low | Med | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Low | Med | Med | Low | Low | Low | Low | Med | Low | Low | Y |
| run9 | Med | Med | Low | Med | Low | Hi | Med | Med | Med | Low | Med | Med | Y |

Window accuracy: **35.2%** (38/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.300 | 0.750 | 0.429 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.250 | 0.333 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.267** | **0.333** | **0.254** | |