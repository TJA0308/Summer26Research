### resnet50_lr0.001_alt2  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw9w_residual  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run14 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run15 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run16 | Med | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run18 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run19 | Med | Low | Low | Low | Med | Low | Low | Low | Low | Med | Low | Low | N |
| run20 | Hi | Hi | Low | Low | Hi | Low | Low | Low | Low | Low | Low | Low | N |
| run23 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |
| run26 | Low | Low | Med | Low | Low | Med | Med | Med | Low | Low | Low | Low | Y |
| run28 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run33 | Hi | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | N |
| run35 | Hi | Low | Hi | Low | Low | Hi | Low | Low | Low | Low | Low | Low | N |
| run38 | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Low | Y |

Window accuracy: **26.9%** (29/108)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.273 | 0.750 | 0.400 | 4 |
| 5-6 mm/rev (med) | 0.000 | 0.000 | 0.000 | 4 |
| 7-8 mm/rev (high) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.091** | **0.250** | **0.133** | |