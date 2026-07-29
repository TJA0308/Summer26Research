### resnet18_lr0.0001_cond_gt  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Med | Med | Med | Y |
| run19 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Med | Med | Med | N |
| run27 | Med | Med | Rgh | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Med | Med | Rgh | ~ |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Rgh | Smt | Med | Med | N |
| run40 | Smt | Med | Rgh | Med | Med | Med | N |
| run43 | Smt | Med | Rgh | Med | Med | Med | N |
| run5 | Smt | Med | Rgh | Med | Med | Med | N |
| run7 | Med | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)