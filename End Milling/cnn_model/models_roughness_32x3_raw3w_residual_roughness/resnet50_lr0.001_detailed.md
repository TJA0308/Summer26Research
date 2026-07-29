### resnet50_lr0.001  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |
| run28 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)