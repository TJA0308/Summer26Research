### resnet18_lr0.001_smote  |  target=roughness  |  scalogram=32x12_raw3w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)