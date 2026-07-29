### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w_residual  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Low | Low | Med | Low | Low | Y |
| run17 | Med | Low | Low | Low | Low | Low | N |
| run21 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Hi | Med | Low | Med | N |
| run31 | Med | Low | Low | Med | Low | Low | N |
| run36 | Hi | Hi | Low | Low | Low | Low | N |
| run37 | Low | Low | Hi | Hi | Hi | Hi | N |
| run45 | Med | Low | Hi | Low | Low | Low | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Med | Med | Med | Med | Med | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **50.0%** (18/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)