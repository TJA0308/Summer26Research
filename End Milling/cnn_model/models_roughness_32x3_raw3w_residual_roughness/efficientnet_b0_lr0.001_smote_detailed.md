### efficientnet_b0_lr0.001_smote  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Rgh | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Smt | Med | Med | Med | Y |
| run28 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Med | Smt | Med | Med | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)