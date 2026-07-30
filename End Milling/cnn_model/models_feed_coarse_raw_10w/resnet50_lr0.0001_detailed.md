### resnet50_lr0.0001  |  target=feed_coarse  |  scalogram=raw_10w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Hi | Med | Hi | Med | Hi | Med | Hi | Hi | Med | Hi | Hi | Med | N |
| run17 | Med | Med | Med | Hi | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Y |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | N |
| run45 | Med | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Low | Med | Med | Low | Med | Low | Low | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Hi | Med | Med | Y |

Window accuracy: **51.7%** (62/120)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.400 | 0.500 | 0.444 | 4 |
| 7-8 mm/rev (high) | 0.571 | 1.000 | 0.727 | 4 |
| **macro avg** | **0.324** | **0.500** | **0.391** | |