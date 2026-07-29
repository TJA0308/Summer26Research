### resnet50_lr0.0001_cond_gt  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Smt | Smt | Med | Smt | Med | ~ |
| run28 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Smt | Med | Med | Med | Med | N |
| run38 | Smt | Med | Med | Med | Med | Med | N |
| run40 | Smt | Med | Med | Med | Med | Med | N |
| run43 | Smt | Med | Med | Med | Med | Med | N |
| run5 | Smt | Med | Med | Med | Med | Med | N |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **25.0%** (9/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **33.3%** (4/12)