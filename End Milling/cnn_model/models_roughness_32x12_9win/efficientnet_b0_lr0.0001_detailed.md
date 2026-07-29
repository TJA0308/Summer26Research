### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=32x12_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Smt | Med | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Smt | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Rgh | Rgh | Smt | Med | Rgh | Rgh | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Med | Smt | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Rgh | Smt | Rgh | Rgh | Smt | Smt | Med | Med | Med | Smt | ~ |
| run40 | Smt | Med | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | N |
| run5 | Smt | Smt | Med | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | N |

Window accuracy: **36.1%** (39/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)