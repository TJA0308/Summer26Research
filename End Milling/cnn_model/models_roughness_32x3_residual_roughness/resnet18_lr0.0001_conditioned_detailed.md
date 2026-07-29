### resnet18_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Med | Med | Y |
| run19 | Med | Smt | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Med | Smt | Rgh | Med | Med | N |
| run32 | Rgh | Smt | Rgh | Med | Smt | Med | N |
| run34 | Rgh | Smt | Rgh | Med | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Med | Smt | Med | Med | Smt | ~ |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Smt | N |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **50.0%** (6/12)