### resnet18_lr0.0001_cascade_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Rgh | Rgh | Med | ~ |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Rgh | Smt | Med | Rgh | N |
| run40 | Smt | Med | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run5 | Smt | Med | Rgh | Smt | Med | Rgh | N |
| run7 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)