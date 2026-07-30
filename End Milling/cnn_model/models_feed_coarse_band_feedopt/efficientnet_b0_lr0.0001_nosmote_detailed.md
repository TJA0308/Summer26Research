### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=band_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Hi | Med | Hi | Hi | Hi | N |
| run3 | Hi | Low | Med | Low | Low | Low | N |
| run31 | Med | Low | Med | Low | Low | Low | N |
| run36 | Hi | Hi | Med | Med | Med | Med | N |
| run37 | Low | Hi | Med | Low | Hi | Low | ~ |
| run45 | Med | Low | Med | Low | Low | Low | N |
| run5 | Hi | Low | Med | Hi | Low | Low | N |
| run7 | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Low | Med | Med | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.500 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.400 | 0.500 | 0.444 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.244** | **0.333** | **0.281** | |