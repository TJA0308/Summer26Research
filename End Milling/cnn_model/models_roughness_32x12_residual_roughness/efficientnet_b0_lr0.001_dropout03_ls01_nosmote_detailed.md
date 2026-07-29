### efficientnet_b0_lr0.001_dropout03_ls01_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Med | Med | Med | Med | Y |
| run22 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Med | Med | Med | Rgh | ~ |
| run32 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Med | Rgh | Rgh | N |
| run40 | Smt | Rgh | Rgh | Med | Rgh | Rgh | N |
| run43 | Smt | Rgh | Med | Med | Med | Rgh | N |
| run5 | Smt | Rgh | Med | Med | Med | Med | N |
| run7 | Med | Rgh | Med | Med | Med | Rgh | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)