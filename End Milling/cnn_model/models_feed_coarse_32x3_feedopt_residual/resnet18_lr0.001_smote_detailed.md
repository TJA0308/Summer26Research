### resnet18_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Hi | Hi | N |
| run17 | Med | Hi | Med | Med | Med | Med | Y |
| run21 | Hi | Med | Hi | Med | Med | Hi | ~ |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Med | Med | Med | Med | Y |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Low | Med | Med | Med | N |
| run45 | Med | Low | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Low | Hi | Med | Med | Y |

Window accuracy: **63.9%** (23/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **83.3%** (10/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 3-4 mm/rev (low) | 1.000 | 0.500 | 0.667 | 4 |
| 5-6 mm/rev (med) | 0.800 | 1.000 | 0.889 | 4 |
| 7-8 mm/rev (high) | 0.800 | 1.000 | 0.889 | 4 |
| **macro avg** | **0.867** | **0.833** | **0.815** | |