### resnet50_lr0.001  |  target=roughness  |  scalogram=32x3_raw9w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Smt | Rgh | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Med | Med | Rgh | Rgh | Med | Med | Rgh | Med | Y |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Rgh | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Y |

Window accuracy: **65.7%** (71/108)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **66.7%** (8/12)