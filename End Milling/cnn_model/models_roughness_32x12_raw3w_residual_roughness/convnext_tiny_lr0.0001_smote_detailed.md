### convnext_tiny_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Med | Smt | Smt | N |
| run22 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Rgh | Med | Smt | Med | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Med | Med | Med | Y |

Window accuracy: **63.9%** (23/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)