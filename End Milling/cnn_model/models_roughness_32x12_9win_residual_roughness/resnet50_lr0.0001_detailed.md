### resnet50_lr0.0001  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run40 | Smt | Med | Smt | Smt | Med | Smt | Med | Med | Med | Med | Med | Smt | ~ |
| run43 | Smt | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run5 | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | ~ |
| run7 | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **36.1%** (39/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **50.0%** (6/12)