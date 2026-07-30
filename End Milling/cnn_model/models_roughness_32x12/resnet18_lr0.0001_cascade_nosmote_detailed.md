### resnet18_lr0.0001_cascade_nosmote  |  target=roughness  |  scalogram=32x12  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run5 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.333 | 1.000 | 0.500 | 4 |
| **macro avg** | **0.111** | **0.333** | **0.167** | |