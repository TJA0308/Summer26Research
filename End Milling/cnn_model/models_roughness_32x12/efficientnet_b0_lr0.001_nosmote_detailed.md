### efficientnet_b0_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Med | Med | Med | Med | Y |
| run19 | Med | Rgh | Smt | Med | Rgh | Smt | N |
| run22 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Smt | Med | Rgh | Smt | N |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Med | Y |
| run32 | Rgh | Rgh | Med | Med | Med | Med | N |
| run34 | Rgh | Rgh | Med | Med | Med | Med | N |
| run38 | Smt | Rgh | Smt | Rgh | Rgh | Smt | ~ |
| run40 | Smt | Rgh | Smt | Med | Rgh | Smt | ~ |
| run43 | Smt | Rgh | Med | Rgh | Rgh | Med | N |
| run5 | Smt | Rgh | Med | Rgh | Rgh | Med | N |
| run7 | Med | Rgh | Med | Med | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **41.7%** (5/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 0.500 | 0.500 | 4 |
| Medium (0.7-1.0) | 0.286 | 0.500 | 0.364 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.595** | **0.417** | **0.421** | |