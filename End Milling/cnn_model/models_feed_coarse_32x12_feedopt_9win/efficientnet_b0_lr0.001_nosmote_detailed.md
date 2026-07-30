### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Low | Med | Med | Low | Low | Low | Low | Low | Low | Y |
| run17 | Med | Hi | Med | Low | Med | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Med | Low | Low | Med | Low | Low | Low | Low | Low | Low | N |
| run25 | Low | Hi | Hi | Hi | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Med | Low | Med | Low | Med | Med | Hi | Low | Med | Low | N |
| run31 | Med | Hi | Med | Low | Low | Med | Low | Low | Low | Low | Low | Low | N |
| run36 | Hi | Hi | Hi | Low | Med | Med | Low | Low | Low | Low | Low | Low | N |
| run37 | Low | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Hi | Hi | Low | Low | Med | Low | Med | Med | Med | Med | Low | Y |
| run5 | Hi | Med | Hi | Low | Med | Med | Low | Low | Low | Low | Low | Low | N |
| run7 | Low | Hi | Med | Med | Med | Med | Low | Low | Low | Low | Med | Low | ~ |
| run9 | Med | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **33.3%** (36/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.750 | 0.462 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.250 | 0.333 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.278** | **0.333** | **0.265** | |