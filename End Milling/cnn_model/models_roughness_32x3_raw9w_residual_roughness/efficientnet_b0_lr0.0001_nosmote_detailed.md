### efficientnet_b0_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x3_raw9w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Smt | N |
| run19 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | N |
| run27 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Smt | Smt | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Rgh | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | N |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.400 | 1.000 | 0.571 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.300** | **0.417** | **0.302** | |