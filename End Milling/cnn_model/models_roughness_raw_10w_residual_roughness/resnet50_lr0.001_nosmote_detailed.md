### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=raw_10w_residual_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Med | Med | Med | Med | Smt | Med | Med | Smt | Med | Med | Med | Y |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Rgh | Med | Med | N |
| run27 | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | N |
| run28 | Rgh | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run32 | Rgh | Med | Smt | Smt | Med | Smt | Smt | Smt | Med | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Rgh | Med | Rgh | Med | Rgh | Med | Smt | Med | Med | Rgh | Med | Med | N |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Smt | Med | Med | Rgh | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **52.5%** (63/120)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.571 | 1.000 | 0.727 | 4 |
| Medium (0.7-1.0) | 0.400 | 0.500 | 0.444 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.324** | **0.500** | **0.391** | |