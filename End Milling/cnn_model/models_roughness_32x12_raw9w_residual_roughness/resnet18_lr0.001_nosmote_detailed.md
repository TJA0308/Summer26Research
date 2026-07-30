### resnet18_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Rgh | Med | Med | Med | Smt | Med | Med | Y |
| run19 | Med | Med | Rgh | Rgh | Rgh | Med | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Rgh | Rgh | Med | Med | Med | Rgh | Med | Rgh | Rgh | N |
| run28 | Rgh | Med | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Med | Med | Rgh | Smt | Med | Rgh | Smt | Smt | N |
| run34 | Rgh | Med | Med | Med | Rgh | Med | Rgh | Med | Med | Rgh | Med | Med | N |
| run38 | Smt | Med | Rgh | Rgh | Rgh | Smt | Smt | Med | Med | Rgh | Rgh | Med | N |
| run40 | Smt | Med | Med | Med | Med | Rgh | Med | Rgh | Med | Med | Med | Med | N |
| run43 | Smt | Rgh | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Med | Smt | Smt | Smt | Smt | Med | Med | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **54.6%** (59/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 0.500 | 0.571 | 4 |
| Medium (0.7-1.0) | 0.400 | 0.500 | 0.444 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.522** | **0.500** | **0.505** | |