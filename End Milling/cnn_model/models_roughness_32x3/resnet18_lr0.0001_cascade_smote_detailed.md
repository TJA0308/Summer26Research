### resnet18_lr0.0001_cascade_smote  |  target=roughness  |  scalogram=32x3  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Med | Med | Med | N |
| run27 | Med | Med | Rgh | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Med | Med | Med | N |
| run32 | Rgh | Smt | Rgh | Med | Smt | Med | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Med | Smt | Med | Y |
| run40 | Smt | Smt | Rgh | Med | Smt | Med | Y |
| run43 | Smt | Smt | Rgh | Med | Smt | Med | Y |
| run5 | Smt | Smt | Rgh | Med | Smt | Med | Y |
| run7 | Med | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.300 | 0.750 | 0.429 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.267** | **0.333** | **0.254** | |