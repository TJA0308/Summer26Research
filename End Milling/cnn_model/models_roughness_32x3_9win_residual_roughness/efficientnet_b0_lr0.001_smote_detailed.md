### efficientnet_b0_lr0.001_smote  |  target=roughness  |  scalogram=32x3_9win_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Med | Med | Rgh | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Med | N |
| run27 | Med | Smt | Smt | Med | Rgh | Rgh | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Med | Med | Med | Med | Med | Rgh | Rgh | Rgh | Med | Med | N |
| run34 | Rgh | Rgh | Rgh | Med | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Med | Y |
| run38 | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run40 | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run43 | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run5 | Smt | Smt | Rgh | Smt | Smt | Med | Rgh | Rgh | Rgh | Med | Rgh | Rgh | N |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.400 | 1.000 | 0.571 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.300** | **0.417** | **0.302** | |