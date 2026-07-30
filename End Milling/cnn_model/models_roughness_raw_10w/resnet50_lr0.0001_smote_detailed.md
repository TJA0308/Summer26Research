### resnet50_lr0.0001_smote  |  target=roughness  |  scalogram=raw_10w  |  arch=resnet50

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Smt | Med | Rgh | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Smt | Med | Rgh | Rgh | Smt | N |
| run22 | Rgh | Med | Med | Med | Rgh | Med | Med | Med | Med | Smt | Smt | Med | Med | N |
| run27 | Med | Med | Med | Med | Smt | Smt | Rgh | Med | Med | Med | Smt | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run34 | Rgh | Smt | Rgh | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | N |
| run38 | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Rgh | Rgh | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Med | Med | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Smt | Med | Med | Smt | Med | Med | Smt | Med | Smt | Med | ~ |

Window accuracy: **53.3%** (64/120)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.500 | 1.000 | 0.667 | 4 |
| Medium (0.7-1.0) | 0.667 | 0.500 | 0.571 | 4 |
| Rough (Ra>1.0) | 1.000 | 0.250 | 0.400 | 4 |
| **macro avg** | **0.722** | **0.583** | **0.546** | |