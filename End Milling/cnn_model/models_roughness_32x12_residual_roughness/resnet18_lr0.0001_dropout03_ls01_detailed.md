### resnet18_lr0.0001_dropout03_ls01  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Smt | Med | ~ |
| run19 | Med | Med | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Med | Med | Med | Med | N |
| run27 | Med | Med | Smt | Med | Med | Med | Y |
| run28 | Rgh | Med | Smt | Med | Med | Med | N |
| run32 | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)