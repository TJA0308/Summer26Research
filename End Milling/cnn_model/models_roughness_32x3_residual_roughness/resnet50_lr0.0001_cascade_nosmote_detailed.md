### resnet50_lr0.0001_cascade_nosmote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Rgh | Smt | Smt | N |
| run19 | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Smt | Smt | Rgh | Smt | Smt | N |
| run28 | Rgh | Med | Smt | Rgh | Med | Rgh | ~ |
| run32 | Rgh | Smt | Med | Rgh | Smt | Rgh | ~ |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Rgh | Smt | Med | Y |
| run40 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Med | Smt | Med | ~ |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.600 | 0.750 | 0.667 | 4 |
| Medium (0.7-1.0) | 0.333 | 0.250 | 0.286 | 4 |
| Rough (Ra>1.0) | 0.750 | 0.750 | 0.750 | 4 |
| **macro avg** | **0.561** | **0.583** | **0.567** | |