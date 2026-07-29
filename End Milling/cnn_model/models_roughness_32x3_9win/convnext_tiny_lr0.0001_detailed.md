### convnext_tiny_lr0.0001  |  target=roughness  |  scalogram=32x3_9win  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Smt | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **60.2%** (65/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)