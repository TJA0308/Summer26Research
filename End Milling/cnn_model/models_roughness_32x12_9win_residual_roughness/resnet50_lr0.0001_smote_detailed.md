### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Smt | Smt | Smt | Med | Med | Smt | Smt | Smt | N |
| run19 | Med | Med | Med | Smt | Med | Med | Rgh | Rgh | Rgh | Smt | Med | Smt | Y |
| run22 | Rgh | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Smt | Smt | Med | Smt | Smt | Smt | Med | Smt | Smt | Med | N |
| run32 | Rgh | Smt | Smt | Rgh | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Med | Smt | Med | Med | Med | Med | Med | Smt | Med | Med | N |
| run43 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)