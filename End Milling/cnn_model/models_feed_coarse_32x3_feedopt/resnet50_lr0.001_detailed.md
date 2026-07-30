### resnet50_lr0.001  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Low | Hi | Med | ~ |
| run21 | Hi | Hi | Med | Med | Med | Hi | ~ |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run37 | Low | Low | Low | Low | Low | Low | Y |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run7 | Low | Med | Med | Low | Med | Low | ~ |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **83.3%** (10/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.750 | 0.857 | 4 |
| 5-6 mm/rev (med) | 0.667 | 1.000 | 0.800 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.750 | 0.857 | 4 |
| **macro avg** | **0.889** | **0.833** | **0.838** | |