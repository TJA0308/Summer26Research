### convnext_tiny_lr0.001_smote  |  target=roughness  |  scalogram=32x3_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Med | Rgh | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Med | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Smt | Smt | Med | Smt | Smt | Med | Med | Smt | Rgh | Smt | Med | ~ |
| run28 | Rgh | Med | Smt | Med | Smt | Smt | Med | Smt | Smt | Smt | Smt | Med | N |
| run32 | Rgh | Smt | Rgh | Smt | Smt | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Med | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Rgh | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)