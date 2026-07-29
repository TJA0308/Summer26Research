### convnext_tiny_lr0.0001  |  target=roughness  |  scalogram=32x12_raw9w  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Med | Rgh | Smt | Smt | Rgh | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Smt | Smt | Smt | Smt | Smt | Rgh | Med | Med | Smt | Smt | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Smt | Smt | Smt | Med | Rgh | Smt | Rgh | Rgh | Smt | Smt | N |
| run34 | Rgh | Rgh | Med | Med | Smt | Rgh | Rgh | Med | Med | Rgh | Rgh | Med | Y |
| run38 | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Med | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **57.4%** (62/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)