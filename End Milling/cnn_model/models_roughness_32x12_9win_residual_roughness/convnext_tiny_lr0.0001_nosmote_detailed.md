### convnext_tiny_lr0.0001_nosmote  |  target=roughness  |  scalogram=32x12_9win_residual_roughness  |  arch=convnext_tiny

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Med | Rgh | Med | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Med | Rgh | Rgh | Med | Med | Smt | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Med | Med | Med | Smt | Med | Med | Med | Med | Rgh | Med | Med | N |
| run32 | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Med | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | ~ |
| run5 | Smt | Smt | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (57/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.750 | 0.750 | 0.750 | 4 |
| Medium (0.7-1.0) | 0.500 | 0.500 | 0.500 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.500 | 0.500 | 4 |
| **macro avg** | **0.583** | **0.583** | **0.583** | |