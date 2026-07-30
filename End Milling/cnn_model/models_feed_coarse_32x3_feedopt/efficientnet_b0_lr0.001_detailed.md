### efficientnet_b0_lr0.001  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Hi | Low | Low | Y |
| run17 | Med | Low | Hi | Low | Low | Low | N |
| run21 | Hi | Low | Med | Hi | Low | Hi | ~ |
| run25 | Low | Low | Hi | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Hi | Low | Low | N |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | N |
| run5 | Hi | Hi | Med | Low | Hi | Med | Y |
| run7 | Low | Low | Hi | Low | Low | Low | Y |
| run9 | Med | Hi | Low | Low | Low | Low | N |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 1.000 | 0.667 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.250 | 0.333 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.667** | **0.583** | **0.556** | |