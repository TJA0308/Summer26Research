### resnet50_lr0.001_cond_gt  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Smt | Med | Med | Y |
| run19 | Med | Rgh | Smt | Rgh | Rgh | Smt | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Rgh | Smt | Smt | N |

Window accuracy: **58.3%** (21/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)