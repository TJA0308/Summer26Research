### efficientnet_b0_lr0.001_smote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Med | Y |
| run19 | Med | Smt | Med | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Smt | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Smt | Med | Med | Med | N |
| run34 | Rgh | Med | Smt | Smt | Smt | Med | N |
| run38 | Smt | Med | Smt | Smt | Smt | Med | Y |
| run40 | Smt | Med | Smt | Smt | Smt | Med | Y |
| run43 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Smt | Med | Med | Med | N |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **33.3%** (4/12)