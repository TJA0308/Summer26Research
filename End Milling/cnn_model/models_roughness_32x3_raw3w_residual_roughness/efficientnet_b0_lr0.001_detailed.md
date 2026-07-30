### efficientnet_b0_lr0.001  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Med | Med | Med | Y |
| run19 | Med | Med | Med | Smt | Med | Med | Y |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Smt | Rgh | Med | Med | N |
| run32 | Rgh | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Smt | Med | Smt | Smt | Smt | N |
| run38 | Smt | Med | Smt | Med | Med | Med | N |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Med | Med | Med | Med | N |
| run5 | Smt | Med | Med | Smt | Med | Med | N |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 0.250 | 0.333 | 4 |
| Medium (0.7-1.0) | 0.444 | 1.000 | 0.615 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.648** | **0.500** | **0.450** | |