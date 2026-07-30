### convnext_tiny_lr0.001_alt1  |  target=feed_coarse  |  scalogram=32x3_feedopt_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run1 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run10 | Low | Low | Med | Low | Low | Hi | Low | Low | Hi | Low | Low | Low | Y |
| run11 | Low | Med | Med | Low | Med | Hi | Low | Low | Low | Low | Low | Low | Y |
| run12 | Med | Med | Med | Med | Med | Hi | Low | Low | Low | Low | Med | Low | Y |
| run18 | Hi | Med | Low | Med | Med | Hi | Low | Low | Med | Low | Med | Low | N |
| run2 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run20 | Hi | Med | Med | Med | Med | Hi | Low | Low | Low | Low | Med | Low | N |
| run22 | Low | Low | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run33 | Hi | Med | Med | Med | Hi | Hi | Low | Low | Low | Hi | Med | Low | N |
| run4 | Med | Med | Low | Low | Hi | Low | Med | Low | Med | Hi | Low | Low | N |
| run6 | Hi | Hi | Low | Low | Hi | Low | Med | Low | Low | Hi | Low | Hi | ~ |
| run8 | Low | Low | Med | Low | Med | Low | Med | Med | Med | Med | Med | Med | N |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 0.286 | 0.500 | 0.364 | 4 |
| 5-6 mm/rev (med) | 0.500 | 0.500 | 0.500 | 4 |
| 7-8 mm/rev (high) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.595** | **0.417** | **0.421** | |