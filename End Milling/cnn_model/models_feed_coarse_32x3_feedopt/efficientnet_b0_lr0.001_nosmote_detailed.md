### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Hi | Med | Med | Hi | Y |
| run21 | Hi | Med | Hi | Hi | Hi | Med | Y |
| run25 | Low | Hi | Med | Med | Med | Med | N |
| run3 | Hi | Med | Low | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Med | Hi | Med | ~ |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Hi | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Med | Med | Med | N |
| run7 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Low | Hi | Hi | Hi | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.286 | 0.500 | 0.364 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.429** | **0.250** | **0.255** | |