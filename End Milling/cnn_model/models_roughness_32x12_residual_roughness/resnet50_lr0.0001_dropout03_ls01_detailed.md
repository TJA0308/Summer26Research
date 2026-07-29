### resnet50_lr0.0001_dropout03_ls01  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Rgh | Rgh | Rgh | Smt | N |
| run22 | Rgh | Smt | Med | Smt | Smt | Smt | N |
| run27 | Med | Smt | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Y |
| run32 | Rgh | Smt | Med | Rgh | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Y |
| run38 | Smt | Smt | Med | Med | Med | Smt | ~ |
| run40 | Smt | Smt | Med | Med | Med | Smt | ~ |
| run43 | Smt | Smt | Med | Med | Med | Smt | ~ |
| run5 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Med | Rgh | Smt | Smt | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)