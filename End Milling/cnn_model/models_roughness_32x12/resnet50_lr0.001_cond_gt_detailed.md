### resnet50_lr0.001_cond_gt  |  target=roughness  |  scalogram=32x12  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Smt | Y |
| run19 | Med | Rgh | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Med | Med | Smt | ~ |
| run43 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)