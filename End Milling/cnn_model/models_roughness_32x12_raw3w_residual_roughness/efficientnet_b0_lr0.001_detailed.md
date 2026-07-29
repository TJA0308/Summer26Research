### efficientnet_b0_lr0.001  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Rgh | Med | Smt | Smt | N |
| run19 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Smt | Med | Rgh | Smt | Smt | N |
| run28 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)