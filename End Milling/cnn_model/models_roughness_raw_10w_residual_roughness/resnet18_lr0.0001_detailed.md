### resnet18_lr0.0001  |  target=roughness  |  scalogram=raw_10w_residual_roughness  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Med | Smt | Med | Med | Smt | Med | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Med | Rgh | Smt | Med | Med | Smt | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Med | Med | N |
| run27 | Med | Smt | Med | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Smt | Rgh | Rgh | Rgh | Smt | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Med | Smt | Smt | Smt | Med | Rgh | Smt | Med | Med | Rgh | Med | Med | N |
| run38 | Smt | Med | Smt | Rgh | Smt | Rgh | Med | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Med | Med | Smt | Med | Smt | Med | Med | Smt | Smt | Med | ~ |

Window accuracy: **54.2%** (65/120)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 1.000 | 0.800 | 4 |
| Medium (0.7-1.0) | 0.333 | 0.250 | 0.286 | 4 |
| Rough (Ra>1.0) | 0.667 | 0.500 | 0.571 | 4 |
| **macro avg** | **0.556** | **0.583** | **0.552** | |