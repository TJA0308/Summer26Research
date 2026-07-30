### efficientnet_b0_lr0.001_nosmote  |  target=roughness  |  scalogram=32x3_raw3w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Med | Rgh | Med | Med | Y |
| run22 | Rgh | Smt | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Med | Med | Med | Med | N |
| run32 | Rgh | Smt | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Med | Med | Med | Med | Med | N |
| run40 | Smt | Smt | Med | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Rgh | Smt | Med | Rgh | Rgh | N |
| run7 | Med | Smt | Med | Med | Med | Med | Y |

Window accuracy: **52.8%** (19/36)
Run hard-vote accuracy: **58.3%** (7/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.500 | 0.667 | 4 |
| Medium (0.7-1.0) | 0.500 | 1.000 | 0.667 | 4 |
| Rough (Ra>1.0) | 0.500 | 0.250 | 0.333 | 4 |
| **macro avg** | **0.667** | **0.583** | **0.556** | |