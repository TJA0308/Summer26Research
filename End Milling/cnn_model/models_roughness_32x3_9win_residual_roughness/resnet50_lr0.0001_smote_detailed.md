### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Med | Smt | Med | Med | Smt | Med | Med | Smt | Y |
| run19 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Smt | Med | Med | Smt | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Med | Med | Med | Med | Med | Smt | Med | Smt | Med | Med | N |
| run34 | Rgh | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | N |
| run40 | Smt | Smt | Med | Med | Med | Med | Smt | Smt | Smt | Med | Med | Med | N |
| run43 | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run5 | Smt | Smt | Smt | Smt | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **40.7%** (44/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 0.250 | 0.333 | 4 |
| Medium (0.7-1.0) | 0.300 | 0.750 | 0.429 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.267** | **0.333** | **0.254** | |