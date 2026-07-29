### resnet18_lr0.0001_cond_gt  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Smt | Med | Rgh | ~ |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Med | Rgh | Smt | Med | Smt | ~ |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Smt | N |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **58.3%** (7/12)