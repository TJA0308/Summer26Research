### efficientnet_b0_lr0.0001_nosmote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw9w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Med | Low | Hi | Med | Med | Low | Low | Low | Med | Low | ~ |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Low | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run45 | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Low | Low | Low | Med | Low | Low | Med | Low | Low | Low | Y |
| run9 | Med | Med | Low | Med | Med | Low | Med | Low | Med | Low | Med | Med | Y |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.750 | 0.857 | 4 |
| 5-6 mm/rev (med) | 0.444 | 1.000 | 0.615 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.481** | **0.583** | **0.491** | |