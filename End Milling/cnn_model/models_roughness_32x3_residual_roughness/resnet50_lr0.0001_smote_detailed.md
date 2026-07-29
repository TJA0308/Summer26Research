### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Med | Y |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Med | Med | Smt | Med | Med | Y |
| run28 | Rgh | Smt | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Med | Smt | Med | ~ |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)