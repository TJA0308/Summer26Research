### efficientnet_b0_lr0.0001_cascade_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Med | Smt | Smt | N |
| run22 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run27 | Med | Rgh | Med | Smt | Rgh | Smt | N |
| run28 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run32 | Rgh | Rgh | Med | Smt | Rgh | Smt | Y |
| run34 | Rgh | Smt | Med | Rgh | Smt | Smt | N |
| run38 | Smt | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run40 | Smt | Rgh | Med | Rgh | Rgh | Rgh | N |
| run43 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run5 | Smt | Rgh | Med | Smt | Rgh | Smt | ~ |
| run7 | Med | Rgh | Med | Smt | Rgh | Smt | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **16.7%** (2/12)
Run soft-vote accuracy: **16.7%** (2/12)