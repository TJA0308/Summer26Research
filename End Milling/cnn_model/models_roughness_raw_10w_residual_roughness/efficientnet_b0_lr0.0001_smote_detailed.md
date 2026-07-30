### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=raw_10w_residual_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Smt | Smt | Med | Med | Med | Smt | Med | Med | Smt | Med | ~ |
| run22 | Rgh | Med | Rgh | Med | Med | Med | Smt | Smt | Rgh | Smt | Rgh | Med | Rgh | ~ |
| run27 | Med | Rgh | Rgh | Med | Med | Med | Med | Med | Rgh | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Rgh | Med | Med | Med | Med | Rgh | Med | Rgh | Rgh | Med | Med | N |
| run32 | Rgh | Med | Smt | Rgh | Smt | Smt | Smt | Smt | Med | Med | Med | Smt | Med | N |
| run34 | Rgh | Med | Rgh | Med | Smt | Smt | Med | Med | Med | Med | Rgh | Med | Med | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Med | Med | Med | Smt | Med | Rgh | Med | Smt | Med | Med | N |
| run43 | Smt | Med | Smt | Med | Smt | Smt | Smt | Smt | Rgh | Med | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Y |

Window accuracy: **41.7%** (50/120)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.500 | 0.667 | 4 |
| Medium (0.7-1.0) | 0.375 | 0.750 | 0.500 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.625** | **0.500** | **0.500** | |