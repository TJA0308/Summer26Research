### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Smt | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Med | Smt | Rgh | Med | Med | N |
| run32 | Rgh | Med | Smt | Smt | Smt | Med | N |
| run34 | Rgh | Rgh | Smt | Smt | Smt | Rgh | ~ |
| run38 | Smt | Med | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Smt | Rgh | Med | Rgh | N |
| run5 | Smt | Smt | Med | Med | Med | Med | N |
| run7 | Med | Med | Smt | Rgh | Med | Med | Y |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.250 | 0.400 | 4 |
| Medium (0.7-1.0) | 0.429 | 0.750 | 0.545 | 4 |
| Rough (Ra>1.0) | 0.250 | 0.250 | 0.250 | 4 |
| **macro avg** | **0.560** | **0.417** | **0.398** | |