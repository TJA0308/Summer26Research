### resnet50_lr0.001  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Smt | Y |
| run19 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Smt | Med | Med | Med | Smt | Y |
| run28 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Smt | Med | Med | Smt | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **41.7%** (5/12)