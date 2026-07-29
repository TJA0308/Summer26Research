### resnet18_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Smt | Y |
| run19 | Med | Rgh | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run27 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)