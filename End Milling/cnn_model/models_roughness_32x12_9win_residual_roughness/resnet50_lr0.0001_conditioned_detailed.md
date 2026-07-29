### resnet50_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Med | Med | Med | Med | Med | Smt | Med | Smt | Y |
| run19 | Med | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | Y |
| run22 | Rgh | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | N |
| run27 | Med | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | Y |
| run28 | Rgh | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | N |
| run34 | Rgh | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | ~ |
| run40 | Smt | Smt | Med | Smt | Med | Med | Med | Med | Med | Smt | Med | Smt | ~ |
| run43 | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Med | Smt | Med | Smt | ~ |
| run5 | Smt | Smt | Smt | Smt | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **37.0%** (40/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)