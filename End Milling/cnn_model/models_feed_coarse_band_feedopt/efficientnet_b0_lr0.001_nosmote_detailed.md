### efficientnet_b0_lr0.001_nosmote  |  target=feed_coarse  |  scalogram=band_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Low | Hi | Med | Low | ~ |
| run17 | Med | Med | Low | Hi | Med | Low | Y |
| run21 | Hi | Med | Low | Hi | Med | Low | N |
| run25 | Low | Med | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Hi | Med | Low | N |
| run31 | Med | Med | Low | Hi | Med | Low | Y |
| run36 | Hi | Med | Low | Hi | Med | Low | N |
| run37 | Low | Med | Low | Hi | Med | Low | ~ |
| run45 | Med | Med | Low | Hi | Med | Low | Y |
| run5 | Hi | Med | Med | Hi | Med | Med | N |
| run7 | Low | Med | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Hi | Med | Low | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.364 | 1.000 | 0.533 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.121** | **0.333** | **0.178** | |