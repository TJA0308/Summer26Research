### efficientnet_b0_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Low | Med | Med | N |
| run17 | Med | Low | Hi | Hi | Hi | Hi | N |
| run21 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Med | Hi | Hi | N |
| run3 | Hi | Low | Med | Hi | Low | Low | N |
| run31 | Med | Med | Low | Low | Low | Low | N |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Low | Med | Hi | Low | ~ |
| run45 | Med | Hi | Med | Low | Hi | Low | N |
| run5 | Hi | Hi | Low | Low | Low | Low | N |
| run7 | Low | Hi | Low | Low | Low | Low | Y |
| run9 | Med | Med | Med | Hi | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.333 | 0.500 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.250 | 0.333 | 4 |
| 7-8 mm/rev (high) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.444** | **0.417** | **0.411** | |