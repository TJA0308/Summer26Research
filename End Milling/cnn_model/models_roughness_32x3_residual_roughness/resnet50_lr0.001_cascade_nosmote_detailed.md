### resnet50_lr0.001_cascade_nosmote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Rgh | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Smt | Rgh | Rgh | Smt | N |
| run22 | Rgh | Med | Rgh | Smt | Med | Med | N |
| run27 | Med | Smt | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Rgh | Smt | Smt | Rgh | ~ |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Smt | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 1.000 | 0.667 | 4 |
| Medium (0.7-1.0) | 0.500 | 0.250 | 0.333 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.667** | **0.583** | **0.556** | |