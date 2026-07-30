### resnet50_lr0.001_alt1  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run1 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run10 | Low | Med | Med | Hi | Hi | Med | Med | Med | Med | Med | Med | Med | N |
| run11 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run12 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run18 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run2 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run20 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run22 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run33 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run4 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run6 | Hi | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run8 | Low | Hi | Med | Med | Med | Med | Med | Med | Low | Med | Med | Med | N |

Window accuracy: **34.3%** (37/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.000 | 0.000 | 0.000 | 4 |
| 5-6 mm/rev (med) | 0.333 | 1.000 | 0.500 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.111** | **0.333** | **0.167** | |