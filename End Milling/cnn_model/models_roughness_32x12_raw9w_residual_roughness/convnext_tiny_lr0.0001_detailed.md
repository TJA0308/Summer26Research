### convnext_tiny_lr0.0001  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Smt | Smt | Smt | Smt | Med | Med | Smt | Smt | N |
| run19 | Med | Med | Med | Med | Rgh | Med | Med | Med | Med | Rgh | Med | Med | Y |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Med | Med | Med | Y |

Window accuracy: **65.7%** (71/108)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **75.0%** (9/12)