### resnet50_lr0.001  |  target=roughness  |  scalogram=32x3  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Rgh | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Med | Rgh | Smt | Med | Med | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Smt | Med | Med | Med | Y |

Window accuracy: **69.4%** (25/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)