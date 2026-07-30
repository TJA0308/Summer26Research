### resnet50_lr0.001  |  target=roughness  |  scalogram=32x3_raw3w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run27 | Med | Rgh | Rgh | Med | Rgh | Rgh | N |
| run28 | Rgh | Smt | Smt | Med | Smt | Smt | N |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 0.750 | 0.600 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.250 | 0.400 | 4 |
| Rough (Ra>1.0) | 0.400 | 0.500 | 0.444 | 4 |
| **macro avg** | **0.633** | **0.500** | **0.481** | |