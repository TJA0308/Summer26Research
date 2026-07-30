### resnet18_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12_raw3w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Rgh | Med | Med | Y |
| run19 | Med | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Rgh | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run40 | Smt | Med | Rgh | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run5 | Smt | Rgh | Smt | Rgh | Rgh | Rgh | N |
| run7 | Med | Med | Med | Rgh | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.750 | 0.857 | 4 |
| Rough (Ra>1.0) | 0.444 | 1.000 | 0.615 | 4 |
| **macro avg** | **0.481** | **0.583** | **0.491** | |