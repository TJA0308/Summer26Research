### resnet18_lr0.001  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Rgh | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Med | Smt | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Rgh | Smt | Rgh | Y |
| run43 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Rgh | Med | Smt | Rgh | Rgh | N |

Window accuracy: **63.9%** (23/36)
Run hard-vote accuracy: **83.3%** (10/12)
Run soft-vote accuracy: **75.0%** (9/12)