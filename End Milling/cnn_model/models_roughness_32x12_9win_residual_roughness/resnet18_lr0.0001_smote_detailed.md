### resnet18_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Rgh | Med | Rgh | Med | Smt | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | N |
| run40 | Smt | Med | Med | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Smt | Rgh | Med | Med | Smt | Smt | Med | Med | Med | Med | N |
| run5 | Smt | Smt | Med | Smt | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | ~ |
| run7 | Med | Rgh | Rgh | Smt | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **50.0%** (54/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)