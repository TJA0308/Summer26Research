### efficientnet_b0_lr0.001_cascade_nosmote  |  target=roughness  |  scalogram=32x12  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Rgh | Rgh | Med | ~ |
| run19 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Med | Y |
| run32 | Rgh | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Med | Rgh | Smt | Med | Smt | ~ |
| run5 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run7 | Med | Med | Med | Rgh | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)