### efficientnet_b0_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Rgh | Smt | Med | Smt | Med | Rgh | Smt | Smt | N |
| run19 | Med | Med | Rgh | Rgh | Med | Med | Smt | Smt | Rgh | Smt | Med | Smt | Y |
| run22 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Smt | Rgh | Rgh | Y |
| run27 | Med | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Smt | Smt | Smt | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Med | Rgh | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Smt | Rgh | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Rgh | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | Rgh | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | N |

Window accuracy: **36.1%** (39/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)