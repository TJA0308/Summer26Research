### resnet50_lr0.001_smote  |  target=roughness  |  scalogram=32x12_raw3w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Smt | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)