### convnext_tiny_lr0.001_alt2  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run14 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run15 | Med | Hi | Hi | Hi | Hi | Hi | Med | Hi | Med | Hi | Hi | Hi | N |
| run16 | Med | Low | Low | Low | Hi | Hi | Med | Med | Med | Low | Low | Low | N |
| run18 | Hi | Low | Med | Low | Low | Hi | Med | Med | Med | Low | Low | Low | N |
| run19 | Med | Low | Low | Hi | Hi | Hi | Med | Med | Med | Hi | Hi | Low | N |
| run20 | Hi | Low | Low | Hi | Hi | Hi | Med | Med | Med | Med | Med | Med | N |
| run23 | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run26 | Low | Med | Med | Med | Med | Med | Low | Med | Med | Med | Med | Med | N |
| run28 | Low | Hi | Low | Low | Low | Low | Med | Med | Med | Low | Low | Low | Y |
| run33 | Hi | Low | Med | Hi | Hi | Hi | Low | Low | Med | Hi | Hi | Hi | Y |
| run35 | Hi | Hi | Low | Hi | Hi | Hi | Med | Med | Med | Hi | Hi | Hi | Y |
| run38 | Low | Low | Low | Low | Hi | Low | Med | Med | Med | Med | Low | Med | Y |

Window accuracy: **37.0%** (40/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.250 | 0.250 | 0.250 | 4 |
| 5-6 mm/rev (med) | 0.200 | 0.250 | 0.222 | 4 |
| 7-8 mm/rev (high) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.372** | **0.333** | **0.348** | |