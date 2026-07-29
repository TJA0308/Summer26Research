### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Smt | Med | Med | N |
| run27 | Med | Smt | Med | Rgh | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Smt | Med | Rgh | Smt | ~ |
| run5 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run7 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)