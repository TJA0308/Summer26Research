### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Smt | Smt | N |
| run19 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)