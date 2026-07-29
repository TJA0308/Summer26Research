### convnext_tiny_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Rgh | Rgh | Smt | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Smt | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Rgh | Rgh | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Med | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **66.7%** (72/108)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)