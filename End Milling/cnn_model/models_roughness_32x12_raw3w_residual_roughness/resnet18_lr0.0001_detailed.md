### resnet18_lr0.0001  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Smt | Smt | Rgh | Smt | Smt | N |
| run22 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Rgh | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Rgh | Rgh | Smt | ~ |
| run40 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run43 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run5 | Smt | Smt | Rgh | Rgh | Rgh | Smt | ~ |
| run7 | Med | Med | Med | Rgh | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.600 | 0.750 | 0.667 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.500 | 0.667 | 4 |
| Rough (Ra>1.0) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.733** | **0.667** | **0.667** | |