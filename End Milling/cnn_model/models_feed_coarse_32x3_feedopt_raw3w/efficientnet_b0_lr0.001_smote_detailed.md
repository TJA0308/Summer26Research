### efficientnet_b0_lr0.001_smote  |  target=feed_coarse  |  scalogram=32x3_feedopt_raw3w  |  arch=efficientnet_b0

| Run | True | w1 | w2 | w3 | Hard | Soft | OK |
|-----|------|----|----|----|------|------|----|
| run13 | Low | Med | Hi | Med | Med | Med | N |
| run17 | Med | Hi | Hi | Med | Hi | Hi | N |
| run21 | Hi | Hi | Med | Hi | Hi | Hi | Y |
| run25 | Low | Med | Med | Hi | Med | Med | N |
| run3 | Hi | Med | Hi | Med | Med | Med | N |
| run31 | Med | Hi | Hi | Hi | Hi | Hi | N |
| run36 | Hi | Low | Hi | Hi | Hi | Hi | Y |
| run37 | Low | Med | Hi | Hi | Hi | Hi | N |
| run45 | Med | Hi | Med | Med | Med | Med | Y |
| run5 | Hi | Hi | Hi | Hi | Hi | Hi | Y |
| run7 | Low | Hi | Hi | Hi | Hi | Hi | N |
| run9 | Med | Med | Med | Med | Med | Med | Y |

Window accuracy: **38.9%** (14/36)
Run hard-vote accuracy: **41.7%** (5/12)
Run soft-vote accuracy: **41.7%** (5/12)