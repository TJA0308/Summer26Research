### convnext_tiny_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **72.2%** (26/36)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)