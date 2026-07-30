### efficientnet_b0_lr0.0001  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Smt | Med | Smt | Y |
| run19 | Med | Smt | Smt | Rgh | Smt | Smt | N |
| run22 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Smt | Rgh | Med | Smt | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Smt | Rgh | Med | Smt | N |
| run38 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Med | Rgh | Smt | Med | Smt | ~ |
| run7 | Med | Smt | Smt | Rgh | Smt | Smt | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.444 | 1.000 | 0.615 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.750 | 0.857 | 4 |
| **macro avg** | **0.481** | **0.583** | **0.491** | |