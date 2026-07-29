### resnet18_lr0.001_smote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Rgh | Med | Med | Smt | Med | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Med | Med | Smt | Med | Smt | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Rgh | Med | Rgh | Rgh | Smt | Smt | Smt | Rgh | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Smt | Rgh | Med | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | N |

Window accuracy: **56.5%** (61/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)