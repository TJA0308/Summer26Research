### resnet50_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run13 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run17 | Med | Hi | Med | Med | Med | Low | Low | Med | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run25 | Low | Med | Med | Med | Med | Low | Low | Med | Med | Med | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Low | Med | Low | Med | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run37 | Low | Med | Low | Med | Low | Low | Low | Med | Med | Med | Med | Low | ~ |
| run45 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Low | Low | Med | Low | Low | Med | Med | Med | Med | Med | Med | Med | N |
| run9 | Med | Low | Med | Low | Low | Low | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **31.5%** (34/108)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.500 | 0.250 | 0.333 | 4 |
| 5-6 mm/rev (med) | 0.300 | 0.750 | 0.429 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.267** | **0.333** | **0.254** | |