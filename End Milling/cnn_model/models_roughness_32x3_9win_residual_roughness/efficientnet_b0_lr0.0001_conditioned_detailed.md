### efficientnet_b0_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Med | Smt | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Med | Smt | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Med | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Med | Rgh | Smt | Smt | Rgh | Rgh | Med | Rgh | Rgh | N |
| run28 | Rgh | Smt | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Med | Med | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Med | Med | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Rgh | Med | Med | Med | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run43 | Smt | Smt | Rgh | Smt | Rgh | Med | Med | Smt | Med | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Rgh | Rgh | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Rgh | Rgh | Smt | Med | Rgh | Med | Med | Rgh | Rgh | Rgh | N |

Window accuracy: **45.4%** (49/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 1.000 | 1.000 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.500 | 1.000 | 0.667 | 4 |
| **macro avg** | **0.500** | **0.667** | **0.556** | |