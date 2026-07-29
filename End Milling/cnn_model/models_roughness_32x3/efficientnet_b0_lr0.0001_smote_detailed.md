### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=32x3  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Smt | Med | Smt | Y |
| run19 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Rgh | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Smt | Med | Med | Med | N |
| run40 | Smt | Med | Rgh | Smt | Med | Smt | ~ |
| run43 | Smt | Med | Med | Med | Med | Med | N |
| run5 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Rgh | Smt | Smt | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)