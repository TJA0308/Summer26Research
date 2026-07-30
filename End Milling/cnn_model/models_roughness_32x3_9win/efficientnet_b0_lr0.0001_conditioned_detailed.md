### efficientnet_b0_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x3_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Smt | Smt | Med | Rgh | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Smt | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Rgh | Smt | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Rgh | Rgh | Rgh | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Rgh | Smt | Med | Rgh | Rgh | Smt | Smt | Smt | N |

Window accuracy: **42.6%** (46/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.375 | 0.750 | 0.500 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.750 | 0.750 | 0.750 | 4 |
| **macro avg** | **0.375** | **0.500** | **0.417** | |