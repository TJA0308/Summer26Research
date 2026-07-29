### resnet18_lr0.0001  |  target=roughness  |  scalogram=32x3_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Rgh | Rgh | Smt | Rgh | Smt | Y |
| run27 | Med | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Rgh | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Rgh | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Rgh | Smt | Smt | N |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)