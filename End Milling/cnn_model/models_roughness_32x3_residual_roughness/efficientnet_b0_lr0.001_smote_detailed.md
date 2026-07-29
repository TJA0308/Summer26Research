### efficientnet_b0_lr0.001_smote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Med | Med | Med | Med | Y |
| run22 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Med | Med | Med | N |
| run32 | Rgh | Rgh | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Med | Med | Med | Med | N |
| run40 | Smt | Med | Rgh | Med | Med | Med | N |
| run43 | Smt | Rgh | Med | Med | Med | Med | N |
| run5 | Smt | Med | Med | Med | Med | Med | N |
| run7 | Med | Med | Med | Rgh | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)