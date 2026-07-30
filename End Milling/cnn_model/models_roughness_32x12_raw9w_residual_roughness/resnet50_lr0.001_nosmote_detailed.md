### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Med | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Smt | ~ |
| run40 | Smt | Smt | Rgh | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | Rgh | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **55.6%** (60/108)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **75.0%** (9/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 1.000 | 0.800 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.250 | 0.400 | 4 |
| Rough (Ra>1.0) | 0.800 | 1.000 | 0.889 | 4 |
| **macro avg** | **0.822** | **0.750** | **0.696** | |