### resnet18_lr0.0001  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Rgh | Smt | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **39.8%** (43/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)