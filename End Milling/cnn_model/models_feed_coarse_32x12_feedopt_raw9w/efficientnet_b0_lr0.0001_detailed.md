### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Hi | Low | Low | Med | Low | Low | Low | Med | Low | Low | N |
| run25 | Low | Med | Low | Med | Hi | Low | Low | Med | Med | Low | Med | Low | ~ |
| run3 | Hi | Med | Med | Hi | Hi | Hi | Hi | Low | Hi | Low | Hi | Hi | Y |
| run31 | Med | Med | Med | Hi | Low | Low | Med | Low | Med | Low | Med | Low | Y |
| run36 | Hi | Med | Med | Med | Med | Low | Hi | Low | Hi | Low | Med | Med | N |
| run37 | Low | Low | Med | Med | Low | Hi | Low | Low | Med | Low | Low | Low | Y |
| run45 | Med | Med | Low | Low | Low | Med | Med | Med | Med | Low | Med | Med | Y |
| run5 | Hi | Low | Med | Low | Low | Med | Med | Low | Low | Med | Low | Low | N |
| run7 | Low | Low | Low | Hi | Low | Low | Med | Hi | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Med | Med | Med | Hi | Med | Hi | Hi | Med | Med | Y |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 1.000 | 0.667 | 4 |
| 5-6 mm/rev (med) | 0.667 | 0.500 | 0.571 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.722** | **0.583** | **0.546** | |