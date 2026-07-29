### efficientnet_b0_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Smt | Rgh | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Med | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Med | Smt | Smt | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)