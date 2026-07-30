### efficientnet_b0_lr0.001_nosmote  |  target=roughness  |  scalogram=raw_10w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | w10 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Rgh | Smt | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | N |
| run19 | Med | Smt | Rgh | Rgh | Smt | Rgh | Smt | Smt | Smt | Smt | Rgh | Smt | Smt | N |
| run22 | Rgh | Rgh | Rgh | Med | Rgh | Med | Rgh | Smt | Med | Smt | Smt | Rgh | Rgh | Y |
| run27 | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Med | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Smt | Rgh | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Y |
| run34 | Rgh | Smt | Smt | Rgh | Rgh | Smt | Rgh | Rgh | Smt | Smt | Rgh | Smt | Rgh | ~ |
| run38 | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Y |
| run40 | Smt | Smt | Smt | Rgh | Smt | Rgh | Smt | Smt | Rgh | Rgh | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Smt | Smt | Smt | Rgh | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run5 | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Smt | Y |
| run7 | Med | Smt | Smt | Med | Med | Med | Med | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **61.7%** (74/120)
Run hard-vote accuracy: **75.0%** (9/12)
Run soft-vote accuracy: **83.3%** (10/12)

Per-class report (run-level, soft-vote):

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Smooth (Ra<0.7) | 0.667 | 1.000 | 0.800 | 4 |
| Medium (0.7-1.0) | 1.000 | 0.500 | 0.667 | 4 |
| Rough (Ra>1.0) | 1.000 | 1.000 | 1.000 | 4 |
| **macro avg** | **0.889** | **0.833** | **0.822** | |