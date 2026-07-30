### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Med | Med | Hi | Med | Med | N |
| run25 | Low | Med | Hi | Med | Med | Med | N |
| run3 | Hi | Med | Hi | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Med | Med | Med | N |
| run37 | Low | Med | Hi | Hi | Hi | Hi | N |
| run45 | Med | Med | Med | Hi | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Hi | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.300 | 0.750 | 0.429 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.100** | **0.250** | **0.143** | |