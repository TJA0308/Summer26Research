### efficientnet_b0_lr0.001_cascade_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Low | Hi | Med | N |
| run17 | Med | Hi | Med | Low | Hi | Low | N |
| run21 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run25 | Low | Med | Hi | Hi | Hi | Hi | N |
| run3 | Hi | Hi | Low | Low | Low | Low | N |
| run31 | Med | Hi | Hi | Low | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Low | Hi | Low | ~ |
| run45 | Med | Hi | Med | Low | Hi | Med | ~ |
| run5 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Hi | Med | Low | Hi | Med | ~ |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.250 | 0.286 | 4 |
| 5-6 mm/rev (med) | 0.667 | 0.500 | 0.571 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.750 | 0.600 | 4 |
| **macro avg** | **0.500** | **0.500** | **0.486** | |