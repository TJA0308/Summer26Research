### efficientnet_b0_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Med | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Smt | Med | Med | Med | N |
| run7 | Med | Smt | Med | Rgh | Smt | Smt | N |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.375 | 0.750 | 0.500 | 4 |
| Medium (0.7-1.0) | 0.500 | 0.250 | 0.333 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.625** | **0.500** | **0.500** | |