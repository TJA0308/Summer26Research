### resnet50_lr0.0001  |  target=roughness  |  scalogram=32x3_raw9w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Med | Med | Rgh | Rgh | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Rgh | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run40 | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run43 | Smt | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run5 | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.400 | 1.000 | 0.571 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.467** | **0.500** | **0.413** | |