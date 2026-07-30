### efficientnet_b0_lr0.0001_smote  |  target=roughness  |  scalogram=band_roughness  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run19 | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run22 | Rgh | Rgh | Med | Med | Med | Med | N |
| run27 | Med | Rgh | Med | Rgh | Rgh | Rgh | N |
| run28 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Med | Rgh | Rgh | Rgh | N |
| run40 | Smt | Rgh | Med | Rgh | Rgh | Rgh | N |
| run43 | Smt | Rgh | Med | Smt | Rgh | Rgh | N |
| run5 | Smt | Rgh | Med | Med | Med | Med | N |
| run7 | Med | Rgh | Med | Rgh | Rgh | Rgh | N |

Window accuracy: **30.6%** (11/36)
Run hard-vote accuracy: **25.0%** (3/12)
Run soft-vote accuracy: **25.0%** (3/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.000 | 0.000 | 0.000 | 4 |
| Medium (0.7-1.0) | 0.000 | 0.000 | 0.000 | 4 |
| Rough (Ra>1.0) | 0.300 | 0.750 | 0.429 | 4 |
| **macro avg** | **0.100** | **0.250** | **0.143** | |