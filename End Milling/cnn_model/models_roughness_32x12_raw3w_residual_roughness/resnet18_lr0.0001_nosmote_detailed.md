### resnet18_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Smt | Med | Med | Smt | ~ |
| run5 | Smt | Smt | Med | Med | Med | Smt | ~ |
| run7 | Med | Smt | Med | Med | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **58.3%** (7/12)