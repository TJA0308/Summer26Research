### efficientnet_b0_lr0.001_dropout03_ls01  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Rgh | Smt | Rgh | Smt | ~ |
| run43 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Rgh | Smt | Smt | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)