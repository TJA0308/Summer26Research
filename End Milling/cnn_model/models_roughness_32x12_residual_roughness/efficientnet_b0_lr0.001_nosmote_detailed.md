### efficientnet_b0_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Rgh | Med | Med | Y |
| run19 | Med | Med | Med | Rgh | Med | Med | Y |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Med | Y |
| run32 | Rgh | Rgh | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Med | Med | Med | Med | N |
| run40 | Smt | Rgh | Med | Med | Med | Med | N |
| run43 | Smt | Rgh | Med | Med | Med | Med | N |
| run5 | Smt | Smt | Med | Rgh | Smt | Med | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)