### resnet50_lr0.001_smote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Med | ~ |
| run19 | Med | Rgh | Med | Smt | Med | Med | Rgh | Rgh | Rgh | Smt | Rgh | Med | ~ |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Med | Smt | Smt | Med | Med | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Med | Smt | Smt | Smt | Med | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **63.9%** (69/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **83.3%** (10/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 1.000 | 1.000 | 4 |
| Medium (0.7-1.0) | 0.667 | 1.000 | 0.800 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.889** | **0.833** | **0.822** | |