### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run27 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Y |
| run32 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.400 | 1.000 | 0.571 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.300** | **0.417** | **0.302** | |