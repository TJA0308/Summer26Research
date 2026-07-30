### resnet18_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Smt | Med | Smt | Smt | Smt | Med | Med | Y |
| run19 | Med | Rgh | Med | Med | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Smt | Med | Rgh | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Med | Med | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Med | N |
| run40 | Smt | Med | Med | Med | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Rgh | Y |
| run43 | Smt | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Smt | Med | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Med | Y |

Window accuracy: **53.7%** (58/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.250 | 0.400 | 4 |
| Medium (0.7-1.0) | 0.600 | 0.750 | 0.667 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.750 | 0.600 | 4 |
| **macro avg** | **0.700** | **0.583** | **0.556** | |