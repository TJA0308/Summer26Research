### convnext_tiny_lr0.0001  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Smt | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Rgh | Smt | Rgh | Smt | ~ |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Med | Med | Med | Med | Y |

Window accuracy: **66.7%** (24/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **83.3%** (10/12)