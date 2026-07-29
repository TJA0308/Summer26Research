### resnet50_lr0.0001  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Smt | Med | Med | Y |
| run22 | Rgh | Med | Med | Smt | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Smt | Smt | Smt | Med | N |
| run32 | Rgh | Med | Med | Smt | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Smt | Med | Med | Med | N |
| run40 | Smt | Med | Med | Smt | Med | Smt | ~ |
| run43 | Smt | Med | Med | Smt | Med | Med | N |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)