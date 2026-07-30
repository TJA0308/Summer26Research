### resnet50_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_raw9w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Med | Rgh | Rgh | Med | Rgh | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Smt | Smt | Med | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Smt | Smt | Med | Med | Smt | Smt | Med | Med | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Smt | Med | Smt | Smt | Med | Med | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Med | Smt | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **47.2%** (51/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.444 | 1.000 | 0.615 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.250 | 0.400 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.648** | **0.500** | **0.450** | |