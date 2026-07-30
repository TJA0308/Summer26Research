### resnet18_lr0.001_smote  |  target=roughness  |  scalogram=raw_10w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Med | Med | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Smt | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Rgh | Med | Med | Smt | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Med | Med | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Smt | Med | Smt | Rgh | Smt | Med | Rgh | Rgh | Smt | Rgh | ~ |
| run34 | Rgh | Med | Rgh | Rgh | Med | Rgh | Med | Smt | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Med | Med | Med | Med | Rgh | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **60.0%** (72/120)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **75.0%** (9/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.750 | 0.857 | 4 |
| Medium (0.7-1.0) | 0.750 | 0.750 | 0.750 | 4 |
| Rough (Ra>1.0) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.783** | **0.750** | **0.758** | |