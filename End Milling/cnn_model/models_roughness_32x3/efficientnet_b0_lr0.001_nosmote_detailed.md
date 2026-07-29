### efficientnet_b0_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Med | Smt | Rgh | Med | Smt | ~ |
| run5 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Rgh | Rgh | Smt | Rgh | Smt | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)