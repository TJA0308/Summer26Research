### efficientnet_b0_lr0.001_conditioned  |  target=roughness  |  scalogram=32x3  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run19 | Med | Rgh | Rgh | Smt | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Med | Smt | Smt | Smt | Med | ~ |
| run28 | Rgh | Smt | Med | Rgh | Smt | Rgh | ~ |
| run32 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Med | Smt | Rgh | Med | Rgh | N |
| run7 | Med | Smt | Rgh | Smt | Smt | Smt | N |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.750 | 0.750 | 0.750 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.250 | 0.400 | 4 |
| Rough (Ra>1.0) | 0.571 | 1.000 | 0.727 | 4 |
| **macro avg** | **0.774** | **0.667** | **0.626** | |