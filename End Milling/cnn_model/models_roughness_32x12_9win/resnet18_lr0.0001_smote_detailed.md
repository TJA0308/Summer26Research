### resnet18_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Rgh | Med | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Smt | Rgh | Med | Rgh | Smt | Smt | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Med | Rgh | Rgh | Smt | Smt | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Smt | Med | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Smt | Smt | Med | Med | Smt | Rgh | Rgh | Smt | Smt | Rgh | Y |
| run43 | Smt | Smt | Med | Rgh | Med | Med | Smt | Smt | Rgh | Smt | Smt | Rgh | Y |
| run5 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 0.500 | 0.571 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.375 | 0.750 | 0.500 | 4 |
| **macro avg** | **0.347** | **0.417** | **0.357** | |