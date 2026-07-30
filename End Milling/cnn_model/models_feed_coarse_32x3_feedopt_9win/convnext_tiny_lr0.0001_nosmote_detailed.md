### convnext_tiny_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Hi | Y |
| run25 | Low | Med | Med | Med | Med | Low | Hi | Low | Low | Low | Med | Low | ~ |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Hi | N |
| run45 | Med | Hi | Med | Med | Low | Med | Med | Low | Low | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Med | Low | Low | Low | Med | Med | Med | Low | Med | Med | N |
| run9 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |

Window accuracy: **29.6%** (32/108)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.250 | 0.333 | 4 |
| 5-6 mm/rev (med) | 0.200 | 0.250 | 0.222 | 4 |
| 7-8 mm/rev (high) | 0.400 | 0.500 | 0.444 | 4 |
| **macro avg** | **0.367** | **0.333** | **0.333** | |