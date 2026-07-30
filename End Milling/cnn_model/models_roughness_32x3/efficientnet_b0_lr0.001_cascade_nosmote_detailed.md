### efficientnet_b0_lr0.001_cascade_nosmote  |  target=roughness  |  scalogram=32x3  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Rgh | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Smt | Smt | Smt | Rgh | N |
| run22 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run27 | Med | Smt | Smt | Rgh | Smt | Smt | N |
| run28 | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run40 | Smt | Rgh | Smt | Smt | Smt | Rgh | Y |
| run43 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Smt | Smt | Smt | Smt | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.250 | 0.500 | 0.333 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.250 | 0.250 | 0.250 | 4 |
| **macro avg** | **0.167** | **0.250** | **0.194** | |