### resnet50_lr0.001  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Rgh | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run43 | Smt | Med | Smt | Rgh | Med | Rgh | N |
| run5 | Smt | Rgh | Smt | Med | Rgh | Smt | ~ |
| run7 | Med | Smt | Smt | Rgh | Smt | Smt | N |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)