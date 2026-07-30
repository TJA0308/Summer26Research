### resnet18_lr0.001_nosmote  |  target=roughness  |  scalogram=raw_10w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Med | Med | Smt | Med | Med | Med | Smt | Smt | Med | ~ |
| run19 | Med | Rgh | Smt | Smt | Smt | Rgh | Smt | Med | Med | Rgh | Smt | Smt | Smt | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Smt | Smt | Smt | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Med | Med | Smt | Med | Med | Smt | Rgh | Med | Med | Med | N |
| run34 | Rgh | Rgh | Med | Smt | Med | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Med | Smt | Smt | Med | Med | Med | Med | Rgh | Med | Med | Med | Y |

Window accuracy: **64.2%** (77/120)
Run hard-vote accuracy: **66.7%** (8/12)
Run soft-vote accuracy: **75.0%** (9/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.800 | 1.000 | 0.889 | 4 |
| Medium (0.7-1.0) | 0.600 | 0.750 | 0.667 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.800** | **0.750** | **0.741** | |