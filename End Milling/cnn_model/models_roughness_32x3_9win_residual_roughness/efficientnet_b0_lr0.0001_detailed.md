### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Smt | Rgh | Rgh | Rgh | Med | Smt | Med | Rgh | Y |
| run19 | Med | Smt | Rgh | Smt | Med | Rgh | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Med | Rgh | Smt | Smt | Rgh | Smt | Med | Rgh | Rgh | N |
| run28 | Rgh | Smt | Rgh | Rgh | Med | Med | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Med | Med | Smt | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Med | Smt | Smt | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Med | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Rgh | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Rgh | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Rgh | Rgh | Smt | Med | Smt | Med | Med | Rgh | Smt | Smt | N |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **66.7%** (8/12)