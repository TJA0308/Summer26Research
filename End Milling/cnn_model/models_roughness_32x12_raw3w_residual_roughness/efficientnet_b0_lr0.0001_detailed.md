### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Smt | Med | Med | Med | Med | Y |
| run22 | Rgh | Smt | Med | Rgh | Smt | Smt | N |
| run27 | Med | Med | Rgh | Smt | Med | Smt | Y |
| run28 | Rgh | Smt | Med | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run38 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)