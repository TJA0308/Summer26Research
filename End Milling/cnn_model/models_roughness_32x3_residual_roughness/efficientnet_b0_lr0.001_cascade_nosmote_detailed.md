### efficientnet_b0_lr0.001_cascade_nosmote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Med | Y |
| run19 | Med | Med | Smt | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Med | Smt | Med | Med | Med | N |
| run34 | Rgh | Smt | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Med | Med | Med | Smt | ~ |
| run40 | Smt | Smt | Smt | Med | Smt | Med | Y |
| run43 | Smt | Smt | Smt | Med | Smt | Med | Y |
| run5 | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Med | ~ |

Window accuracy: **36.1%** (13/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 0.500 | 0.500 | 4 |
| Medium (0.7-1.0) | 0.375 | 0.750 | 0.500 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.292** | **0.417** | **0.333** | |