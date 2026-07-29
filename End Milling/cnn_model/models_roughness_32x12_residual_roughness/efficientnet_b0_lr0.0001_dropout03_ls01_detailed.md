### efficientnet_b0_lr0.0001_dropout03_ls01  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run27 | Med | Smt | Smt | Med | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Rgh | Smt | Med | Smt | ~ |
| run43 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run5 | Smt | Rgh | Med | Med | Med | Med | N |
| run7 | Med | Rgh | Smt | Med | Rgh | Smt | N |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **16.7%** (2/12)
Run soft-vote accuracy: **25.0%** (3/12)