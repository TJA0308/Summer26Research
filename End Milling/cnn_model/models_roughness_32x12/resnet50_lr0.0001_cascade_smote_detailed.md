### resnet50_lr0.0001_cascade_smote  |  target=roughness  |  scalogram=32x12  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Smt | Med | Smt | Y |
| run19 | Med | Med | Med | Smt | Med | Smt | Y |
| run22 | Rgh | Med | Med | Smt | Med | Med | N |
| run27 | Med | Med | Med | Smt | Med | Med | Y |
| run28 | Rgh | Med | Med | Smt | Med | Med | N |
| run32 | Rgh | Med | Med | Smt | Med | Smt | N |
| run34 | Rgh | Med | Med | Smt | Med | Smt | N |
| run38 | Smt | Med | Med | Smt | Med | Smt | ~ |
| run40 | Smt | Med | Med | Smt | Med | Smt | ~ |
| run43 | Smt | Med | Med | Smt | Med | Smt | ~ |
| run5 | Smt | Med | Med | Smt | Med | Smt | ~ |
| run7 | Med | Med | Med | Smt | Med | Smt | Y |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.444 | 1.000 | 0.615 | 4 |
| Medium (0.7-1.0) | 0.333 | 0.250 | 0.286 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.259** | **0.417** | **0.300** | |