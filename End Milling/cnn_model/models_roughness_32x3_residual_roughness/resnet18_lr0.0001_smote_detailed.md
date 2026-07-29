### resnet18_lr0.0001_smote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Med | Med | Med | Med | N |
| run27 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Smt | Med | Rgh | Smt | Med | N |
| run32 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Smt | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)