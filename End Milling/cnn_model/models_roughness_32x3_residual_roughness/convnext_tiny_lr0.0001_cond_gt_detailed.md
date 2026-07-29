### convnext_tiny_lr0.0001_cond_gt  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Smt | Smt | N |
| run19 | Med | Smt | Med | Rgh | Smt | Rgh | N |
| run22 | Rgh | Med | Med | Smt | Med | Med | N |
| run27 | Med | Med | Smt | Rgh | Med | Smt | Y |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Rgh | Smt | Med | Smt | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)