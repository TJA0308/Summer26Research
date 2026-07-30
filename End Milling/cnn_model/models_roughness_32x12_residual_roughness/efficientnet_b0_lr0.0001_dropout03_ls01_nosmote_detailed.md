### efficientnet_b0_lr0.0001_dropout03_ls01_nosmote  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Smt | Med | Smt | N |
| run27 | Med | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run38 | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Med | Smt | Smt | Y |
| run7 | Med | Rgh | Med | Smt | Rgh | Smt | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.375 | 0.750 | 0.500 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.250 | 0.250 | 0.250 | 4 |
| **macro avg** | **0.208** | **0.333** | **0.250** | |