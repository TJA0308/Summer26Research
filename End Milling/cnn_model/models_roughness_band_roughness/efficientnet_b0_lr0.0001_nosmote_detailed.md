### efficientnet_b0_lr0.0001_nosmote  |  target=roughness  |  scalogram=band_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Med | Med | Y |
| run19 | Med | Smt | Med | Med | Med | Med | Y |
| run22 | Rgh | Smt | Med | Smt | Smt | Smt | N |
| run27 | Med | Smt | Med | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Med | Med | Med | Med | N |
| run34 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run38 | Smt | Smt | Rgh | Med | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Med | Med | Med | N |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)