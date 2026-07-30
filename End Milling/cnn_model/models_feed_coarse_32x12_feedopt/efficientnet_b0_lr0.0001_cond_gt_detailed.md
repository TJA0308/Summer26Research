### efficientnet_b0_lr0.0001_cond_gt  |  target=feed_coarse  |  scalogram=32x12_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Hi | Med | Med | Med | Y |
| run21 | Hi | Low | Hi | Low | Low | Low | N |
| run25 | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Hi | Med | Med | Med | N |
| run31 | Med | Med | Hi | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Med | Med | Med | N |
| run37 | Low | Low | Hi | Hi | Hi | Hi | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Med | Hi | Med | Med | Med | N |
| run7 | Low | Hi | Hi | Med | Hi | Hi | N |
| run9 | Med | Med | Hi | Low | Med | Low | Y |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **16.7%** (2/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.286 | 0.500 | 0.364 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.095** | **0.167** | **0.121** | |