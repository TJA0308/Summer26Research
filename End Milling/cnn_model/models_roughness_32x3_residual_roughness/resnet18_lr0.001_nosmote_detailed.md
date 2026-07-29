### resnet18_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Rgh | Smt | Smt | Rgh | N |
| run19 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Rgh | Rgh | Med | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **58.3%** (7/12)