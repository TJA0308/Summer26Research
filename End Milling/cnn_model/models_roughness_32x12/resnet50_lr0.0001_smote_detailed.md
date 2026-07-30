### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x12  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Rgh | Med | Med | Y |
| run19 | Med | Med | Med | Rgh | Med | Med | Y |
| run22 | Rgh | Med | Smt | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Med | Med | Rgh | Med | Med | N |
| run34 | Rgh | Med | Med | Rgh | Med | Med | N |
| run38 | Smt | Med | Med | Rgh | Med | Med | N |
| run40 | Smt | Med | Med | Rgh | Med | Med | N |
| run43 | Smt | Med | Med | Rgh | Med | Med | N |
| run5 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Rgh | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 0.250 | 0.333 | 4 |
| Medium (0.7-1.0) | 0.400 | 1.000 | 0.571 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.300** | **0.417** | **0.302** | |