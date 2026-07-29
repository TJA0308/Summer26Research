### resnet18_lr0.001_conditioned  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Rgh | Med | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Med | Smt | Smt | Med | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Med | Med | Med | Rgh | Med | Smt | Smt | Med | Med | Y |

Window accuracy: **64.8%** (70/108)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)