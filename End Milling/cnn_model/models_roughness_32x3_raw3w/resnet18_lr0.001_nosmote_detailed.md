### resnet18_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3_raw3w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Rgh | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **63.9%** (23/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)