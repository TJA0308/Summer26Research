### convnext_tiny_lr0.0001_smote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Rgh | Smt | Rgh | Rgh | Rgh | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Med | Med | Med | Smt | Rgh | Rgh | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | N |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)