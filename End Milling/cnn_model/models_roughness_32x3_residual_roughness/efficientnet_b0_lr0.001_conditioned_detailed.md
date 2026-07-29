### efficientnet_b0_lr0.001_conditioned  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Med | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Rgh | Med | Rgh | Y |
| run28 | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Smt | Rgh | Smt | Rgh | ~ |
| run38 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)