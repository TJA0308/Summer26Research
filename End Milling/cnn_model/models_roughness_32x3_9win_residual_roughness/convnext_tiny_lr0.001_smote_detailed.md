### convnext_tiny_lr0.001_smote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | ~ |
| run19 | Med | Smt | Med | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Med | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Med | Med | Rgh | Smt | Smt | Rgh | Rgh | Smt | Med | Med | N |
| run38 | Smt | Rgh | Med | Smt | Smt | Smt | Smt | Med | Med | Smt | Smt | Med | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Med | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **42.6%** (46/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)