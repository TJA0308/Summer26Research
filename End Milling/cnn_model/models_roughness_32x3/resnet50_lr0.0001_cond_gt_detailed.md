### resnet50_lr0.0001_cond_gt  |  target=roughness  |  scalogram=32x3  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Smt | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Med | Med | Med | Med | N |
| run40 | Smt | Med | Med | Med | Med | Med | N |
| run43 | Smt | Med | Med | Med | Med | Med | N |
| run5 | Smt | Med | Med | Med | Med | Med | N |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.333 | 1.000 | 0.500 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.111** | **0.333** | **0.167** | |