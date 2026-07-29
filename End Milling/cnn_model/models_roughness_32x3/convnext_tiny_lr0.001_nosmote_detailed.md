### convnext_tiny_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Smt | Med | Rgh | Smt | Rgh | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)