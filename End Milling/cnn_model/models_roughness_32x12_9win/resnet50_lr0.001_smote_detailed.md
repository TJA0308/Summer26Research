### resnet50_lr0.001_smote  |  target=roughness  |  scalogram=32x12_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Smt | Med | Smt | Rgh | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **58.3%** (63/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)