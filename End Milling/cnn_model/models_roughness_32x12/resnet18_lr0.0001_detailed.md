### resnet18_lr0.0001  |  target=roughness  |  scalogram=32x12  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Smt | Med | Med | Med | N |
| run34 | Rgh | Med | Rgh | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Med | Smt | Med | Y |
| run40 | Smt | Smt | Rgh | Med | Smt | Med | Y |
| run43 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run5 | Smt | Med | Med | Med | Med | Med | N |
| run7 | Med | Med | Smt | Med | Med | Med | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)