### resnet18_lr0.001_conditioned  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Smt | Smt | N |
| run19 | Med | Med | Med | Rgh | Med | Med | Y |
| run22 | Rgh | Med | Med | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Med | Smt | Med | Med | N |
| run40 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **69.4%** (25/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)