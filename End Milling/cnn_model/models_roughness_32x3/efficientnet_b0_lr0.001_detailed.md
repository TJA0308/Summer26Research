### efficientnet_b0_lr0.001  |  target=roughness  |  scalogram=32x3  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Smt | Med | Rgh | Smt | N |
| run19 | Med | Smt | Med | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Rgh | Med | Smt | Smt | N |
| run28 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Med | Smt | Med | Med | N |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)