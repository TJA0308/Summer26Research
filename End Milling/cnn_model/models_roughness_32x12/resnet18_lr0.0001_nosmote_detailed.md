### resnet18_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Med | Med | Med | N |
| run27 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Rgh | Rgh | Med | Rgh | Rgh | N |
| run43 | Smt | Rgh | Med | Med | Med | Rgh | N |
| run5 | Smt | Med | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)