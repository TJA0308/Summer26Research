### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=32x12  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Smt | Rgh | Smt | Y |
| run27 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run40 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)