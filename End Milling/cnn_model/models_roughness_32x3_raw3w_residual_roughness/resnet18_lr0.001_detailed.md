### resnet18_lr0.001  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **80.6%** (29/36)
Run hard-vote accuracy: **83.3%** (10/12)
Run soft-vote accuracy: **83.3%** (10/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.750 | 0.857 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.750 | 0.857 | 4 |
| Rough (Ra>1.0) | 0.667 | 1.000 | 0.800 | 4 |
| **macro avg** | **0.889** | **0.833** | **0.838** | |