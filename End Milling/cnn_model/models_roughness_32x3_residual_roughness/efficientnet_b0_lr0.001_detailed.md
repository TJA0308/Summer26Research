### efficientnet_b0_lr0.001  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Smt | Smt | Smt | Smt | N |
| run19 | Med | Med | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Smt | Rgh | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Med | Smt | Smt | Smt | Smt | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)