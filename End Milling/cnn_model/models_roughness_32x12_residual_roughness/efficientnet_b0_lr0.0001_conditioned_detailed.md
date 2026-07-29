### efficientnet_b0_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Smt | Med | Smt | Y |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Med | Rgh | Smt | Med | Smt | ~ |
| run7 | Med | Smt | Smt | Rgh | Smt | Smt | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)