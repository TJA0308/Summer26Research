### resnet50_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x3  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Med | Med | Med | Med | N |
| run34 | Rgh | Med | Med | Med | Med | Med | N |
| run38 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Med | Med | Med | Med | N |
| run43 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Smt | Smt | Med | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.500 | 0.667 | 4 |
| Medium (0.7-1.0) | 0.400 | 1.000 | 0.571 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.467** | **0.500** | **0.413** | |