### convnext_tiny_lr0.0001_smote  |  target=roughness  |  scalogram=32x3_raw9w_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Smt | Smt | Smt | Med | Smt | Med | Smt | Smt | N |
| run19 | Med | Smt | Smt | Smt | Med | Med | Smt | Smt | Smt | Med | Smt | Med | ~ |
| run22 | Rgh | Med | Med | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Rgh | ~ |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run34 | Rgh | Med | Smt | Smt | Med | Smt | Med | Med | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **55.6%** (60/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **58.3%** (7/12)