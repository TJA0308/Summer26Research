### convnext_tiny_lr0.0001  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Hi | Hi | Med | Med | Hi | Hi | Med | Med | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Low | Low | Med | Med | Low | Low | Y |
| run3 | Hi | Hi | Hi | Hi | Med | Med | Med | Hi | Med | Med | Med | Med | N |
| run31 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Low | Low | Med | Med | Low | Low | Med | Low | N |
| run7 | Low | Low | Low | Low | Low | Med | Med | Med | Low | Med | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Low | N |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.400 | 0.500 | 0.444 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.250 | 0.286 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.411** | **0.417** | **0.410** | |