### resnet50_lr0.0001_dropout03_ls01_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Rgh | Smt | Rgh | N |
| run19 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Smt | Smt | Med | Smt | Smt | N |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Y |
| run34 | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **66.7%** (24/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **58.3%** (7/12)