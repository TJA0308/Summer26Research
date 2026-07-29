### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Med | Med | Y |
| run19 | Med | Med | Smt | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Rgh | Med | Rgh | Rgh | Med | ~ |
| run28 | Rgh | Smt | Med | Rgh | Smt | Med | N |
| run32 | Rgh | Smt | Med | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Med | Smt | Med | Smt | ~ |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **75.0%** (9/12)