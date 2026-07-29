### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x12_feedopt_raw3w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run17 | Med | Hi | Med | Hi | Hi | Hi | N |
| run21 | Hi | Hi | Hi | Low | Hi | Hi | Y |
| run25 | Low | Hi | Hi | Low | Hi | Hi | N |
| run3 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Hi | Hi | Med | Hi | Hi | N |
| run45 | Med | Hi | Hi | Low | Hi | Hi | N |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Low | Low | Low | Low | Low | Y |
| run9 | Med | Med | Hi | Hi | Hi | Hi | N |

Window accuracy: **47.2%** (17/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)