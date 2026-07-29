### efficientnet_b0_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Rgh | Med | Med | Med | Rgh | Rgh | Med | Med | Med | Y |
| run19 | Med | Rgh | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Med | Med | N |
| run40 | Smt | Med | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Med | Med | N |
| run43 | Smt | Med | Med | Rgh | Med | Med | Rgh | Rgh | Med | Med | Med | Med | N |
| run5 | Smt | Med | Med | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Med | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Med | ~ |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)