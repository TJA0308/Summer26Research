### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=raw_10w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Rgh | Rgh | Med | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Smt | Med | Med | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Med | Smt | Med | Smt | Med | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Med | Rgh | Med | Smt | Smt | Y |
| run5 | Smt | Med | Med | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Rgh | Med | Smt | Rgh | Smt | Med | Med | Y |

Window accuracy: **57.5%** (69/120)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.571 | 1.000 | 0.727 | 4 |
| Medium (0.7-1.0) | 0.750 | 0.750 | 0.750 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.774** | **0.667** | **0.626** | |