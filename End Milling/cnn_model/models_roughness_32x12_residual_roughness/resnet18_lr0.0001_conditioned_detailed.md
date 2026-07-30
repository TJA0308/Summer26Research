### resnet18_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x12_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Rgh | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Rgh | Med | Med | Med | N |
| run27 | Med | Med | Rgh | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Rgh | Med | Med | Med | N |
| run34 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Rgh | Med | Med | Med | N |
| run40 | Smt | Med | Rgh | Rgh | Rgh | Med | N |
| run43 | Smt | Med | Rgh | Med | Med | Med | N |
| run5 | Smt | Med | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.444 | 1.000 | 0.615 | 4 |
| Rough (Ra>1.0) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.370** | **0.500** | **0.396** | |