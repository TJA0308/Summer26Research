### efficientnet_b0_lr0.001_cascade_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Med | Hi | Med | Med | N |
| run17 | Med | Med | Med | Hi | Med | Hi | Y |
| run21 | Hi | Med | Low | Hi | Med | Med | N |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Low | Low | Med | Low | Low | N |
| run31 | Med | Med | Med | Hi | Med | Med | Y |
| run36 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Med | Low | Med | Med | N |
| run45 | Med | Med | Low | Low | Low | Low | N |
| run5 | Hi | Low | Hi | Med | Low | Low | N |
| run7 | Low | Low | Low | Hi | Low | Low | Y |
| run9 | Med | Low | Low | Low | Low | Low | N |

Window accuracy: **41.7%** (15/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **33.3%** (4/12)