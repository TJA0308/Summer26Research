### resnet50_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Smt | Smt | N |
| run19 | Med | Smt | Med | Med | Med | Smt | Y |
| run22 | Rgh | Smt | Med | Med | Med | Med | N |
| run27 | Med | Smt | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Med | Med | Med | Smt | N |
| run34 | Rgh | Smt | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Med | Med | Smt | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)