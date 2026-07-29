### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=32x3  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Rgh | Med | Smt | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run27 | Med | Smt | Smt | Rgh | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Med | Smt | Rgh | ~ |
| run34 | Rgh | Smt | Rgh | Med | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Smt | Rgh | Rgh | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)