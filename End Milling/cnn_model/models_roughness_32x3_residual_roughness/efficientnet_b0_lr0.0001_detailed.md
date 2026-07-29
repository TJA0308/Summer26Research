### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run27 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Med | Rgh | Smt | Med | Med | N |
| run32 | Rgh | Rgh | Med | Smt | Rgh | Smt | Y |
| run34 | Rgh | Smt | Med | Rgh | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Smt | Rgh | Rgh | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)