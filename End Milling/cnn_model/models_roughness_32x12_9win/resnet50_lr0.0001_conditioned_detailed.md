### resnet50_lr0.0001_conditioned  |  target=roughness  |  scalogram=32x12_9win  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Med | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run19 | Med | Med | Smt | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run22 | Rgh | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Smt | Med | Med | Med | Med | Smt | Smt | Smt | Smt | Smt | Med | N |
| run32 | Rgh | Med | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run34 | Rgh | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | N |
| run38 | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | ~ |
| run40 | Smt | Med | Smt | Med | Med | Med | Med | Med | Med | Smt | Med | Med | N |
| run43 | Smt | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Smt | ~ |
| run5 | Smt | Med | Med | Smt | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **43.5%** (47/108)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 1.000 | 0.750 | 0.857 | 4 |
| Medium (0.7-1.0) | 0.444 | 1.000 | 0.615 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.481** | **0.583** | **0.491** | |