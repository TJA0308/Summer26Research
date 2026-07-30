### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Rgh | Rgh | Smt | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Smt | Smt | Med | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Med | Med | Med | Smt | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Smt | Rgh | Rgh | Smt | Smt | Med | Med | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Med | Med | Med | Med | Rgh | Med | Y |
| run38 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Rgh | Y |
| run40 | Smt | Smt | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Med | Med | Med | Smt | Rgh | Rgh | N |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **43.5%** (47/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.400 | 0.500 | 0.444 | 4 |
| Medium (0.7-1.0) | 0.667 | 0.500 | 0.571 | 4 |
| Rough (Ra>1.0) | 0.250 | 0.250 | 0.250 | 4 |
| **macro avg** | **0.439** | **0.417** | **0.422** | |