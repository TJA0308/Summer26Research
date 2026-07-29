### convnext_tiny_lr0.0001  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Rgh | Smt | Rgh | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Rgh | Med | Med | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Med | Med | Rgh | Med | Med | Y |

Window accuracy: **66.7%** (24/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)