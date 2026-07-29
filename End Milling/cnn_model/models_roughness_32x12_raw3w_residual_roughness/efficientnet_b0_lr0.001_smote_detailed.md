### efficientnet_b0_lr0.001_smote  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |
| run19 | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Med | Smt | Rgh | Smt | ~ |
| run40 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run5 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run7 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)