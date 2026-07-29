### resnet18_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Smt | Smt | N |
| run19 | Med | Med | Med | Smt | Med | Med | Y |
| run22 | Rgh | Smt | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Smt | Med | Med | Med | N |
| run34 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Med | Med | Med | Med | N |
| run40 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Med | Smt | Med | Med | N |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Smt | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)