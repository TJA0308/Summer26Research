### resnet50_lr0.001_smote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Smt | Rgh | Smt | N |
| run22 | Rgh | Rgh | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Rgh | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **46.3%** (50/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)