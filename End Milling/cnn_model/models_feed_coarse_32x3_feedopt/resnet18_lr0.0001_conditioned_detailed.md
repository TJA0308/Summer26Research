### resnet18_lr0.0001_conditioned  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Low | Med | Med | Med | Med | Y |
| run21 | Hi | Low | Low | Med | Low | Low | N |
| run25 | Low | Low | Hi | Med | Low | Med | Y |
| run3 | Hi | Low | Low | Med | Low | Med | N |
| run31 | Med | Low | Med | Med | Med | Med | Y |
| run36 | Hi | Low | Low | Hi | Low | Low | N |
| run37 | Low | Low | Low | Med | Low | Med | Y |
| run45 | Med | Med | Low | Med | Med | Med | Y |
| run5 | Hi | Low | Hi | Hi | Hi | Low | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Low | Low | Med | Low | Med | ~ |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.400 | 0.500 | 0.444 | 4 |
| 5-6 mm/rev (med) | 0.571 | 1.000 | 0.727 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.324** | **0.500** | **0.391** | |