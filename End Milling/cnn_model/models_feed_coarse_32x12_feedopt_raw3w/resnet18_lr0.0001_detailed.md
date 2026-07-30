### resnet18_lr0.0001  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Med | Med | Hi | N |
| run17 | Med | Med | Hi | Hi | Hi | Med | ~ |
| run21 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Med | Hi | Hi | N |
| run45 | Med | Hi | Med | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Med | Hi | Med | Y |
| run7 | Low | Hi | Med | Hi | Hi | Hi | N |
| run9 | Med | Med | Hi | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.250 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.750 | 0.750 | 0.750 | 4 |
| 7-8 mm/rev (high) | 0.429 | 0.750 | 0.545 | 4 |
| **macro avg** | **0.726** | **0.583** | **0.565** | |