### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Med | Smt | Smt | Smt | Smt | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)