### resnet50_lr0.001_cascade_smote  |  target=roughness  |  scalogram=32x3  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Med | Y |
| run19 | Med | Med | Rgh | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Smt | Med | Med | Med | N |
| run40 | Smt | Med | Med | Med | Med | Med | N |
| run43 | Smt | Med | Smt | Med | Med | Med | N |
| run5 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)