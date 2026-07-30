### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Hi | Med | Med | Med | Med | N |
| run25 | Low | Hi | Low | Med | Hi | Low | ~ |
| run3 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run37 | Low | Hi | Med | Low | Hi | Low | ~ |
| run45 | Med | Med | Hi | Med | Med | Med | Y |
| run5 | Hi | Med | Med | Med | Med | Med | N |
| run7 | Low | Med | Low | Hi | Med | Low | ~ |
| run9 | Med | Med | Med | Hi | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **75.0%** (9/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.750 | 0.857 | 4 |
| 5-6 mm/rev (med) | 0.571 | 1.000 | 0.727 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.857** | **0.750** | **0.750** | |