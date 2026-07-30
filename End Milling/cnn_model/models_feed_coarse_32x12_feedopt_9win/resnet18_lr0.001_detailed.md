### resnet18_lr0.001  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Med | ~ |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Med | Low | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Low | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | Med | Med | Med | Med | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Low | Low | Med | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Med | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Med | Low | Low | Low | Med | Med | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Low | Low | Low | Med | Med | Low | Low | Low | Low | N |

Window accuracy: **49.1%** (53/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.667 | 0.500 | 0.571 | 4 |
| 5-6 mm/rev (med) | 0.333 | 0.500 | 0.400 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.556** | **0.500** | **0.514** | |