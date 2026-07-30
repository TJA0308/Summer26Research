### efficientnet_b0_lr0.001  |  target=roughness  |  scalogram=32x12_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Smt | Smt | Med | Med | Med | Med | Med | Smt | Y |
| run19 | Med | Smt | Med | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Med | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Med | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Smt | Med | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Smt | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **48.1%** (52/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.750 | 0.750 | 0.750 | 4 |
| Medium (0.7-1.0) | 0.375 | 0.750 | 0.500 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.375** | **0.500** | **0.417** | |