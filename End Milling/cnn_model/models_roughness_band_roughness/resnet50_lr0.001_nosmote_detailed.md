### resnet50_lr0.001_nosmote  |  target=roughness  |  scalogram=band_roughness  |  arch=resnet50

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Smt | Smt | Med | Smt | Med | ~ |
| run19 | Med | Smt | Smt | Med | Smt | Med | ~ |
| run22 | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run27 | Med | Smt | Smt | Med | Smt | Med | ~ |
| run28 | Rgh | Smt | Smt | Rgh | Smt | Smt | N |
| run32 | Rgh | Smt | Smt | Med | Smt | Med | N |
| run34 | Rgh | Smt | Smt | Med | Smt | Med | N |
| run38 | Smt | Smt | Smt | Med | Smt | Med | Y |
| run40 | Smt | Smt | Smt | Med | Smt | Med | Y |
| run43 | Smt | Smt | Smt | Med | Smt | Med | Y |
| run5 | Smt | Smt | Smt | Med | Smt | Med | Y |
| run7 | Med | Smt | Smt | Smt | Smt | Smt | N |

Window accuracy: **33.3%** (12/36)
Run hard-vote accuracy: **33.3%** (4/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.333 | 0.750 | 0.462 | 4 |
| Rough (Ra>1.0) | 0.000 | 0.000 | 0.000 | 4 |
| **macro avg** | **0.111** | **0.250** | **0.154** | |