### efficientnet_b0_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 1.000 | 0.800 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.667 | 1.000 | 0.800 | 4 |
| **macro avg** | **0.444** | **0.667** | **0.533** | |