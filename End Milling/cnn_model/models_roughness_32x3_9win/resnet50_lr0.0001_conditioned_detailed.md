### resnet50_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x3_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Smt | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Smt | Med | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | N |
| run32 | Rgh | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Med | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Med | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Med | Med | Med | Med | Smt | Smt | Med | Smt | Med | Med | N |
| run43 | Smt | Smt | Med | Smt | Smt | Smt | Med | Med | Med | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Med | Smt | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Med | Med | Y |

Window accuracy: **44.4%** (48/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.429 | 0.750 | 0.545 | 4 |
| Medium (0.7-1.0) | 0.600 | 0.750 | 0.667 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.343** | **0.500** | **0.404** | |