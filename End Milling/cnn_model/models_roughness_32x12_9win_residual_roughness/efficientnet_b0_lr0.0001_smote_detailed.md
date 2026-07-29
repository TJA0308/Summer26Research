### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Smt | Med | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Smt | Smt | Rgh | Rgh | Med | Med | Med | Med | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Med | Rgh | Med | Smt | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Rgh | Med | Rgh | Smt | Med | Med | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Rgh | Rgh | Smt | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Med | Rgh | Med | Med | Smt | Smt | Smt | Med | Med | Med | N |
| run40 | Smt | Rgh | Med | Med | Smt | Med | Med | Med | Med | Rgh | Med | Med | N |
| run43 | Smt | Rgh | Smt | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | N |
| run5 | Smt | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **43.5%** (47/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)