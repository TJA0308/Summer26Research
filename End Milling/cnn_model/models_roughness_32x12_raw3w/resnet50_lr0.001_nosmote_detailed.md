### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=32x12_raw3w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Rgh | Rgh | Rgh | Smt | N |
| run22 | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Y |
| run27 | Med | Rgh | Rgh | Med | Rgh | Med | ~ |
| run28 | Rgh | Rgh | Med | Med | Med | Rgh | ~ |
| run32 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run34 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run38 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Rgh | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **55.6%** (20/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 1.000 | 0.667 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.500 | 0.667 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.833** | **0.667** | **0.667** | |