### resnet50_lr0.001_cascade_nosmote  |  target=roughness  |  scalogram=32x12  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Rgh | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Smt | Rgh | Med | Rgh | ~ |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.571 | 1.000 | 0.727 | 4 |
| Medium (0.7-1.0) | 0.667 | 0.500 | 0.571 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.746** | **0.667** | **0.655** | |