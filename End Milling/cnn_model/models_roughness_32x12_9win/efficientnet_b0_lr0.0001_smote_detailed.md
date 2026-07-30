### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=32x12_9win  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Smt | Rgh | Smt | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Med | Smt | Smt | Rgh | Smt | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Smt | Rgh | Rgh | Rgh | Med | Med | Rgh | Med | Med | Med | N |
| run27 | Med | Smt | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Smt | Med | Med | Med | Smt | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Rgh | Smt | Rgh | Med | Med | Med | Med | Rgh | Med | Med | N |
| run34 | Rgh | Smt | Smt | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Rgh | Smt | Rgh | Med | Rgh | Med | Med | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Rgh | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Med | Rgh | Smt | Rgh | Med | Med | Smt | Med | Med | Med | N |
| run5 | Smt | Rgh | Smt | Smt | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Rgh | Med | Med | Med | Med | Rgh | Med | Rgh | Med | Med | Y |

Window accuracy: **39.8%** (43/108)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.750 | 0.857 | 4 |
| Medium (0.7-1.0) | 0.444 | 1.000 | 0.615 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.481** | **0.583** | **0.491** | |