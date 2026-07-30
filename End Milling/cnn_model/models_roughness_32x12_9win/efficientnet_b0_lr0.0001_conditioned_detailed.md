### efficientnet_b0_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x12_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Rgh | Smt | Smt | Med | Smt | Med | Med | Med | Smt | Y |
| run19 | Med | Smt | Med | Rgh | Smt | Smt | Smt | Smt | Rgh | Med | Smt | Smt | N |
| run22 | Rgh | Rgh | Smt | Med | Smt | Smt | Med | Rgh | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Rgh | Smt | Smt | Smt | Rgh | Smt | Med | Smt | Smt | Smt | N |
| run28 | Rgh | Smt | Rgh | Med | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | N |
| run32 | Rgh | Med | Smt | Rgh | Smt | Smt | Smt | Rgh | Rgh | Rgh | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Rgh | Smt | Smt | Rgh | Rgh | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Smt | N |

Window accuracy: **41.7%** (45/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.333 | 1.000 | 0.500 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.111** | **0.333** | **0.167** | |