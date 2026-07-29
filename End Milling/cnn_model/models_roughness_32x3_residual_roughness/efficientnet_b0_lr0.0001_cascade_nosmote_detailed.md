### efficientnet_b0_lr0.0001_cascade_nosmote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Smt | Rgh | Smt | Smt | N |
| run28 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Smt | Med | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)