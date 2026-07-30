### efficientnet_b0_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x12  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Med | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Smt | Smt | Smt | Smt | N |
| run28 | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Rgh | Med | Smt | Smt | N |
| run34 | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Rgh | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run5 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Med | Smt | Smt | Smt | N |

Window accuracy: **44.4%** (16/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **50.0%** (6/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.429 | 0.750 | 0.545 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.600 | 0.750 | 0.667 | 4 |
| **macro avg** | **0.343** | **0.500** | **0.404** | |