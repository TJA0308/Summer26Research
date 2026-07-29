### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Med | Hi | Hi | N |
| run17 | Med | Med | Hi | Med | Med | Med | Y |
| run21 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run25 | Low | Med | Med | Hi | Med | Med | N |
| run3 | Hi | Med | Med | Med | Med | Med | N |
| run31 | Med | Med | Med | Med | Med | Med | Y |
| run36 | Hi | Med | Hi | Hi | Hi | Med | Y |
| run37 | Low | Hi | Hi | Med | Hi | Med | N |
| run45 | Med | Med | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Med | Hi | Hi | Y |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Hi | Hi | Hi | Hi | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **50.0%** (6/12)
Run soft-vote accuracy: **41.7%** (5/12)