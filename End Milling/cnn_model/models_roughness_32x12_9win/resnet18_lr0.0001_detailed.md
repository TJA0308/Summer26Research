### resnet18_lr0.0001  |  target=roughness  |  scalogram=32x12_9win  |  arch=resnet18

| Run | True | w1 | w2 | w3 | w4 | w5 | w6 | w7 | w8 | w9 | Hard | Soft | OK |
|-----|------|----|----|----|----|----|----|----|----|----|------|------|----|
| run11 | Med | Rgh | Rgh | Smt | Smt | Smt | Rgh | Med | Med | Med | Rgh | Rgh | N |
| run19 | Med | Rgh | Rgh | Rgh | Smt | Smt | Med | Med | Med | Med | Med | Rgh | Y |
| run22 | Rgh | Rgh | Rgh | Smt | Smt | Smt | Med | Med | Med | Med | Med | Med | N |
| run27 | Med | Med | Rgh | Rgh | Smt | Smt | Med | Med | Med | Med | Med | Med | Y |
| run28 | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Y |
| run32 | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Rgh | Smt | Rgh | ~ |
| run34 | Rgh | Rgh | Rgh | Rgh | Smt | Smt | Med | Smt | Smt | Rgh | Rgh | Rgh | Y |
| run38 | Smt | Rgh | Med | Rgh | Smt | Smt | Med | Med | Med | Med | Med | Smt | ~ |
| run40 | Smt | Rgh | Rgh | Rgh | Smt | Smt | Med | Smt | Smt | Smt | Smt | Smt | Y |
| run43 | Smt | Rgh | Rgh | Rgh | Smt | Smt | Smt | Smt | Smt | Med | Smt | Smt | Y |
| run5 | Smt | Rgh | Rgh | Rgh | Smt | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | Rgh | N |
| run7 | Med | Rgh | Rgh | Smt | Smt | Smt | Med | Rgh | Rgh | Rgh | Rgh | Rgh | N |

Window accuracy: **39.8%** (43/108)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **58.3%** (7/12)