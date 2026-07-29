### resnet18_lr0.0001  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Smt | Med | Smt | N |
| run27 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Rgh | Smt | Med | Rgh | N |
| run43 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Rgh | Smt | Smt | Smt | N |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)