### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=raw_10w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Low | Med | Low | Low | Med | Low | Med | Low | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Low | Med | Med | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Low | Med | Low | Low | Low | Med | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Low | Low | Med | Med | Low | Low | Low | Med | Low | Low | N |
| run31 | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Low | Med | Med | Low | Med | Med | Med | Low | Med | Med | Med | N |
| run37 | Low | Med | Low | Med | Med | Low | Med | Low | Low | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Low | Low | Low | Med | Low | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Hi | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Med | Low | Low | Low | Low | Low | Low | Med | Med | Low | Med | Y |
| run9 | Med | Low | Low | Med | Low | Low | Med | Low | Low | Med | Med | Low | Med | ~ |

Window accuracy: **42.5%** (51/120)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.250 | 0.333 | 4 |
| 5-6 mm/rev (med) | 0.400 | 1.000 | 0.571 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.300** | **0.417** | **0.302** | |