### convnext_tiny_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Rgh | Med | Smt | Smt | N |
| run19 | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Smt | Smt | Med | Smt | Med | Med | Med | Med | Smt | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Y |
| run32 | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **71.3%** (77/108)
Run hard-vote accuracy: **83.3%** (10/12)
Run soft-vote accuracy: **75.0%** (9/12)