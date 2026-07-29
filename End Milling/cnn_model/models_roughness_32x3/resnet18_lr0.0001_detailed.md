### resnet18_lr0.0001  |  target=roughness  |  scalogram=32x3  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Smt | Rgh | Med | Smt | Rgh | Y |
| run43 | Smt | Smt | Rgh | Med | Smt | Rgh | Y |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **58.3%** (7/12)