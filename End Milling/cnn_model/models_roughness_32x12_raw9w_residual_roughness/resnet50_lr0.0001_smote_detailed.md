### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Med | Med | Rgh | Smt | Med | Med | Med | N |
| run32 | Rgh | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run7 | Med | Med | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | N |

Window accuracy: **55.6%** (60/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)