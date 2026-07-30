### efficientnet_b0_lr0.001_cascade_smote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run19 | Med | Med | Med | Smt | Med | Med | Y |
| run22 | Rgh | Rgh | Med | Med | Med | Med | N |
| run27 | Med | Rgh | Smt | Med | Rgh | Med | ~ |
| run28 | Rgh | Med | Rgh | Med | Med | Med | N |
| run32 | Rgh | Rgh | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Med | Med | Med | Med | N |
| run38 | Smt | Med | Med | Med | Med | Med | N |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Med | Med | Med | Med | N |
| run5 | Smt | Rgh | Med | Rgh | Rgh | Rgh | N |
| run7 | Med | Smt | Rgh | Smt | Smt | Smt | N |

Window accuracy: **27.8%** (10/36)
Run hard-vote accuracy: **16.7%** (2/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 0.250 | 0.333 | 4 |
| Medium (0.7-1.0) | 0.250 | 0.500 | 0.333 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.250** | **0.250** | **0.222** | |