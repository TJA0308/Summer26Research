### resnet18_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Rgh | Rgh | Smt | Med | Med | Smt | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Rgh | ~ |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Med | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Rgh | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **57.4%** (62/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)