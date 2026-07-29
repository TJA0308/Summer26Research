### efficientnet_b0_lr0.0001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Hi | Hi | Low | Hi | Hi | N |
| run17 | Med | Med | Low | Hi | Med | Med | Y |
| run21 | Hi | Hi | Low | Hi | Hi | Hi | Y |
| run25 | Low | Low | Low | Low | Low | Low | Y |
| run3 | Hi | Med | Low | Hi | Med | Low | N |
| run31 | Med | Med | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Low | Low | Low | Low | N |
| run37 | Low | Low | Med | Low | Low | Low | Y |
| run45 | Med | Low | Low | Low | Low | Low | N |
| run5 | Hi | Low | Med | Med | Med | Med | N |
| run7 | Low | Med | Low | Low | Low | Low | Y |
| run9 | Med | Low | Med | Low | Low | Low | N |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)