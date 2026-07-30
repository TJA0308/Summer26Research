### convnext_tiny_lr0.001_cascade_smote  |  target=roughness  |  scalogram=32x3_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Rgh | Med | Rgh | ~ |
| run27 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **77.8%** (28/36)
Run hard-vote accuracy: **83.3%** (10/12)
Run soft-vote accuracy: **91.7%** (11/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 1.000 | 1.000 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.750 | 0.857 | 4 |
| Rough (Ra>1.0) | 0.800 | 1.000 | 0.889 | 4 |
| **macro avg** | **0.933** | **0.917** | **0.915** | |