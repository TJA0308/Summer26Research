### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=raw_10w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Med | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Smt | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Med | Med | Med | Med | Rgh | Med | Med | Med | Rgh | Med | Med | N |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Med | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Med | Med | N |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Med | Med | Y |

Window accuracy: **51.7%** (62/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 0.500 | 0.571 | 4 |
| Medium (0.7-1.0) | 0.429 | 0.750 | 0.545 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.698** | **0.583** | **0.595** | |