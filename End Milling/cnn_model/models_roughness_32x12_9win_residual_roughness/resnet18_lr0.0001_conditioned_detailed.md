### resnet18_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Med | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Med | Rgh | Rgh | Rgh | Smt | Smt | Smt | Rgh | Rgh | Rgh | N |
| run40 | Smt | Rgh | Med | Rgh | Rgh | Rgh | Smt | Smt | Smt | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Med | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run5 | Smt | Smt | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Smt | Rgh | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |

Window accuracy: **43.5%** (47/108)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **33.3%** (4/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.364 | 1.000 | 0.533 | 4 |
| **macro avg** | **0.121** | **0.333** | **0.178** | |