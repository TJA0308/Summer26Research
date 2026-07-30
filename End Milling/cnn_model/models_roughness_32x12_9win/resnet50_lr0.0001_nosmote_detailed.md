### resnet50_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Med | Med | Rgh | Smt | Smt | Smt | Med | Med | Smt | Med | Smt | Y |
| run22 | Rgh | Med | Med | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Rgh | Smt | Smt | Med | Smt | Smt | Med | Smt | Smt | N |
| run32 | Rgh | Med | Med | Rgh | Smt | Med | Med | Smt | Smt | Smt | Med | Smt | N |
| run34 | Rgh | Med | Med | Smt | Med | Med | Med | Med | Smt | Smt | Med | Med | N |
| run38 | Smt | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Med | Med | Med | Smt | Med | Med | Med | Med | Smt | Med | Med | N |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Med | ~ |

Window accuracy: **41.7%** (45/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.375 | 0.750 | 0.500 | 4 |
| Medium (0.7-1.0) | 0.500 | 0.500 | 0.500 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.292** | **0.417** | **0.333** | |