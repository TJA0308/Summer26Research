### efficientnet_b0_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Low | Low | Low | Low | Med | Med | Hi | Low | Low | Y |
| run17 | Med | Low | Med | Med | Med | Low | Low | Low | Low | Low | Low | Low | N |
| run21 | Hi | Low | Low | Med | Med | Low | Low | Low | Low | Low | Low | Low | N |
| run25 | Low | Med | Low | Med | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Med | Med | Low | Hi | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | N |
| run36 | Hi | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run37 | Low | Med | Med | Low | Med | Med | Low | Low | Med | Med | Med | Med | N |
| run45 | Med | Med | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Med | Med | Low | Low | Low | Low | Low | Hi | ~ |
| run7 | Low | Low | Low | Low | Med | Hi | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **38.9%** (42/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.429 | 0.750 | 0.545 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.500 | 0.500 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.643** | **0.500** | **0.482** | |