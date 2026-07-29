### resnet50_lr0.001_smote  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)