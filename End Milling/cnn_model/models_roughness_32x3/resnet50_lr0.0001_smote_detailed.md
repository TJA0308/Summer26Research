### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x3  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Med | Smt | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Smt | Med | Med | N |
| run32 | Rgh | Smt | Med | Med | Med | Smt | N |
| run34 | Rgh | Smt | Med | Med | Med | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Smt | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)