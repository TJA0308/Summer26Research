### resnet18_lr0.001_smote  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Rgh | Smt | Smt | Rgh | Smt | Smt | Rgh | Med | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **56.5%** (61/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 1.000 | 0.800 | 4 |
| Medium (0.7-1.0) | 0.600 | 0.750 | 0.667 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.756** | **0.667** | **0.622** | |