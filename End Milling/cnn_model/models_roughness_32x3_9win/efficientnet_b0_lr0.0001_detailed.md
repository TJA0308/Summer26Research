### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=32x3_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Smt | Smt | Med | Rgh | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Smt | Smt | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Smt | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Rgh | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Rgh | Smt | Smt | Med | Smt | Med | Rgh | Rgh | Smt | Smt | Smt | N |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)