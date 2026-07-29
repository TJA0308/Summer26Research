### efficientnet_b0_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Smt | Rgh | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)