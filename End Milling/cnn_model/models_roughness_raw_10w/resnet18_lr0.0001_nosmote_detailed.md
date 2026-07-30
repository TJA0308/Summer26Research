### resnet18_lr0.0001_nosmote  |  target=roughness  |  scalogram=raw_10w  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Med | Smt | Rgh | Smt | Rgh | Smt | Rgh | Smt | Rgh | Med | Smt | Smt | N |
| run22 | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Med | Med | Smt | Smt | Smt | Rgh | Med | Y |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Smt | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Smt | Smt | Med | Med | Med | Smt | Med | Med | Med | Smt | Med | Med | N |
| run34 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Smt | Smt | Rgh | Rgh | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Rgh | Med | Med | Med | Med | Med | Med | Med | Med | Rgh | Med | Med | Y |

Window accuracy: **66.7%** (80/120)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **66.7%** (8/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 1.000 | 0.800 | 4 |
| Medium (0.7-1.0) | 0.500 | 0.500 | 0.500 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.500 | 0.667 | 4 |
| **macro avg** | **0.722** | **0.667** | **0.656** | |