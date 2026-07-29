### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Med | Med | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Rgh | Smt | Rgh | Smt | Med | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Med | Smt | Med | Rgh | Smt | Med | Rgh | Med | Med | N |
| run27 | Med | Smt | Smt | Rgh | Med | Rgh | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Rgh | Rgh | Med | Smt | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Rgh | Smt | Med | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run40 | Smt | Rgh | Rgh | Smt | Med | Smt | Smt | Smt | Med | Med | Smt | Smt | Y |
| run43 | Smt | Rgh | Rgh | Smt | Med | Rgh | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run5 | Smt | Rgh | Rgh | Rgh | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Smt | Med | Med | Smt | Med | Med | Smt | Med | Med | Med | Med | Y |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)