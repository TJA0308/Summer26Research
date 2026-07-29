### efficientnet_b0_lr0.001  |  target=roughness  |  scalogram=32x12  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Smt | Smt | N |
| run19 | Med | Smt | Smt | Med | Smt | Smt | N |
| run22 | Rgh | Med | Rgh | Med | Med | Med | N |
| run27 | Med | Med | Smt | Med | Med | Med | Y |
| run28 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Med | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Med | Med | Med | N |
| run7 | Med | Med | Smt | Med | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)