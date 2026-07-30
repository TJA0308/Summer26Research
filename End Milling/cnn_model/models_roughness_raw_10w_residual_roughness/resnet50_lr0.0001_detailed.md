### resnet50_lr0.0001  |  target=roughness  |  scalogram=raw_10w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Med | Rgh | Med | Rgh | Rgh | Rgh | Med | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Smt | Med | Smt | Smt | Med | Med | N |
| run27 | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Med | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Rgh | Med | Med | N |
| run38 | Smt | Rgh | Smt | Rgh | Med | Med | Rgh | Rgh | Smt | Med | Smt | Rgh | Rgh | N |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run43 | Smt | Rgh | Smt | Rgh | Med | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | N |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **56.7%** (68/120)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 0.500 | 0.571 | 4 |
| Medium (0.7-1.0) | 0.600 | 0.750 | 0.667 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.589** | **0.583** | **0.579** | |