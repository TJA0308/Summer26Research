### convnext_tiny_lr0.0001_smote  |  target=roughness  |  scalogram=32x3  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Smt | Med | Smt | Med | ~ |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Med | Rgh | Smt | Rgh | ~ |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Smt | Rgh | Med | Smt | Y |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)